from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file, make_response
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
from functools import wraps
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production-12345')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)  # Session timeout 1 ชั่วโมง

# Database configuration
DATABASE = os.environ.get('DATABASE_PATH', 'project_scoring.db')

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized', 'redirect': '/login'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        if session.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function


class ProjectScoringSystem:
    """ระบบคำนวณและจัดเก็บคะแนนโครงการ"""
    
    # Difficulty Customer (ความยากของลูกค้า)
    DIFFICULTY_CUSTOMER = {
        'Government': 5,  # แก้จาก Governance
        'State Enterprise': 5,
        'Banking': 4,
        'Telco': 4,
        'Other': 3
    }
    
    # Difficulty Type of Project (ความยากของงาน)
    DIFFICULTY_PROJECT = {
        # Complexity level : High
        'New Business': 2,
        '(Application or Custom SW) + Infrastructure': 1.8,
        # Complexity level : Medium
        'Application': 1.7,
        'Custom software package': 1.6,
        'Rollout': 1.5,
        'SW infra': 1.4,
        'Infrastructure integration': 1.3,
        # Complexity level : Normal
        'Service': 1.2,
        'Hardware/Software delivery': 1
    }
    
    # Challenge Topup
    CHALLENGE_TOPUP = {
        'None': 0,
        'Soft Recovery Project': 8,
        'Recovery Fail Project': 15
    }
    
    @staticmethod
    def get_db():
        """เชื่อมต่อฐานข้อมูล"""
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn
    
    @staticmethod
    def init_database():
        """สร้างตารางฐานข้อมูล"""
        conn = ProjectScoringSystem.get_db()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                employee_id TEXT UNIQUE NOT NULL,
                role TEXT NOT NULL DEFAULT 'employee',
                created_date TEXT NOT NULL
            )
        ''')
        
        # Projects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                project_name TEXT NOT NULL,
                contract_no TEXT,
                difficulty_customer TEXT NOT NULL,
                difficulty_project TEXT NOT NULL,
                progress REAL NOT NULL,
                baseline_pm_effort REAL NOT NULL,
                project_duration REAL NOT NULL,
                challenge_type TEXT NOT NULL,
                score REAL NOT NULL,
                baseline_manday REAL NOT NULL,
                created_date TEXT NOT NULL,
                updated_date TEXT NOT NULL,
                notes TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create default admin if not exists
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        if not cursor.fetchone():
            admin_password = generate_password_hash('admin123')
            cursor.execute('''
                INSERT INTO users (username, password, first_name, last_name, 
                                 employee_id, role, created_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', ('admin', admin_password, 'Admin', 'System', 'ADMIN001', 
                  'admin', datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def calculate_score(difficulty_customer: str, difficulty_project: str, progress: float, 
                       baseline_pm_effort: float, project_duration: float, challenge_type: str) -> float:
        """
        คำนวณคะแนนโครงการตามสูตร: B2*((SUM(C2:C2)*(D2/E2))*G2/100)+F2
        
        B2 = Difficulty Type of Project (project_weight)
        C2 = Difficulty Customer (customer_weight) 
        D2 = Baseline PM Effort (baseline_pm_effort)
        E2 = Duration (project_duration) - หน่วยเป็นปี
        G2 = Progress (progress)
        F2 = Challenge topup (challenge_topup)
        """
        customer_weight = ProjectScoringSystem.DIFFICULTY_CUSTOMER.get(difficulty_customer, 3)
        project_weight = ProjectScoringSystem.DIFFICULTY_PROJECT.get(difficulty_project, 1)
        challenge_topup = ProjectScoringSystem.CHALLENGE_TOPUP.get(challenge_type, 0)
        
        # สูตร: B2*((SUM(C2:C2)*(D2/E2))*G2/100)+F2
        # = project_weight * ((customer_weight * (baseline_pm_effort / project_duration)) * progress / 100) + challenge_topup
        # project_duration เป็นปีแล้ว ไม่ต้องแปลง
        
        if project_duration <= 0:
            project_duration = 1  # ป้องกันการหารด้วยศูนย์
            
        inner_calculation = customer_weight * (baseline_pm_effort / project_duration)
        score = project_weight * (inner_calculation * progress / 100) + challenge_topup
        
        return round(score, 2)
    
    @staticmethod
    def calculate_baseline_manday(difficulty_project: str, baseline_pm_effort: float, 
                                  project_duration: float, challenge_type: str, progress: float) -> float:
        """
        คำนวณ Baseline Manday (แก้ไขให้รวม Progress)
        
        สูตร: ความยากของโครงการ × (
            (ความยากโครงการ × (baseline_pm_effort / ระยะเวลา) × ระยะเวลา × (Progress/100) / 100)
            + Challenge_topup
        )
        ระยะเวลาเป็นปี
        """
        project_weight = ProjectScoringSystem.DIFFICULTY_PROJECT.get(difficulty_project, 1)
        challenge_topup = ProjectScoringSystem.CHALLENGE_TOPUP.get(challenge_type, 0)
        
        # คำนวณส่วนใน parentheses (เพิ่ม Progress)
        # project_duration เป็นปีแล้ว ไม่ต้องแปลง
        if project_duration > 0:
            inner_calculation = (project_weight * (baseline_pm_effort / project_duration) * project_duration * (progress / 100)) / 100
        else:
            inner_calculation = 0
        
        # คำนวณ Baseline Manday
        baseline_manday = project_weight * (inner_calculation + challenge_topup)
        
        return round(baseline_manday, 2)
    
    @staticmethod
    def create_user(username: str, password: str, first_name: str, 
                   last_name: str, employee_id: str, role: str = 'employee') -> int:
        """สร้าง user ใหม่"""
        conn = ProjectScoringSystem.get_db()
        cursor = conn.cursor()
        
        hashed_password = generate_password_hash(password)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            cursor.execute('''
                INSERT INTO users (username, password, first_name, last_name, 
                                 employee_id, role, created_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (username, hashed_password, first_name, last_name, 
                  employee_id, role, current_time))
            
            user_id = cursor.lastrowid
            conn.commit()
            return user_id
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    @staticmethod
    def verify_user(username: str, password: str) -> Optional[Dict]:
        """ตรวจสอบ login"""
        conn = ProjectScoringSystem.get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            return dict(user)
        return None
    
    @staticmethod
    def get_user(user_id: int) -> Optional[Dict]:
        """ดึงข้อมูล user"""
        conn = ProjectScoringSystem.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None
    
    @staticmethod
    def add_project(user_id: int, project_name: str, contract_no: str, difficulty_customer: str, 
                   difficulty_project: str, progress: float, baseline_pm_effort: float, 
                   project_duration: float, challenge_type: str, notes: str = "", project_year: int = None) -> int:
        """เพิ่มโครงการใหม่"""
        score = ProjectScoringSystem.calculate_score(difficulty_customer, difficulty_project, progress,
                                                   baseline_pm_effort, project_duration, challenge_type)
        baseline_manday = ProjectScoringSystem.calculate_baseline_manday(
            difficulty_project, baseline_pm_effort, project_duration, challenge_type, progress
        )
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if project_year is None:
            project_year = datetime.now().year
        
        conn = ProjectScoringSystem.get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO projects (user_id, project_name, contract_no, difficulty_customer, 
                                difficulty_project, progress, baseline_pm_effort, 
                                project_duration, challenge_type, score, baseline_manday, 
                                created_date, updated_date, notes, difficulty, customer_type, project_year)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, project_name, contract_no, difficulty_customer, difficulty_project, progress,
              baseline_pm_effort, project_duration, challenge_type, score, baseline_manday,
              current_time, current_time, notes, difficulty_project, difficulty_customer, project_year))
        
        project_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return project_id
    
    @staticmethod
    def update_project(project_id: int, user_id: int, project_name: str, contract_no: str,
                      difficulty_customer: str, difficulty_project: str, progress: float,
                      baseline_pm_effort: float, project_duration: float,
                      challenge_type: str, notes: str = "", project_year: int = None) -> bool:
        """อัปเดตโครงการ"""
        score = ProjectScoringSystem.calculate_score(difficulty_customer, difficulty_project, progress,
                                                   baseline_pm_effort, project_duration, challenge_type)
        baseline_manday = ProjectScoringSystem.calculate_baseline_manday(
            difficulty_project, baseline_pm_effort, project_duration, challenge_type, progress
        )
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if project_year is None:
            project_year = datetime.now().year
        
        conn = ProjectScoringSystem.get_db()
        cursor = conn.cursor()
        
        # ตรวจสอบว่าเป็นของ user หรือเป็น admin
        cursor.execute('SELECT user_id FROM projects WHERE id = ?', (project_id,))
        project = cursor.fetchone()
        
        if not project:
            conn.close()
            return False
        
        cursor.execute('''
            UPDATE projects 
            SET project_name = ?, contract_no = ?, difficulty_customer = ?, difficulty_project = ?, 
                progress = ?, baseline_pm_effort = ?, project_duration = ?, 
                challenge_type = ?, score = ?, baseline_manday = ?, 
                updated_date = ?, notes = ?, difficulty = ?, customer_type = ?, project_year = ?
            WHERE id = ? AND user_id = ?
        ''', (project_name, contract_no, difficulty_customer, difficulty_project, progress,
              baseline_pm_effort, project_duration, challenge_type, score, 
              baseline_manday, current_time, notes, difficulty_project, difficulty_customer, project_year,
              project_id, user_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    @staticmethod
    def delete_project(project_id: int, user_id: int) -> bool:
        """ลบโครงการ"""
        conn = ProjectScoringSystem.get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM projects WHERE id = ? AND user_id = ?', 
                      (project_id, user_id))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    @staticmethod
    def get_project(project_id: int) -> Optional[Dict]:
        """ดึงข้อมูลโครงการ"""
        conn = ProjectScoringSystem.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    @staticmethod
    def get_user_projects(user_id: int) -> List[Dict]:
        """ดึงโครงการของ user"""
        conn = ProjectScoringSystem.get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM projects 
            WHERE user_id = ? 
            ORDER BY score DESC, updated_date DESC
        ''', (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    @staticmethod
    def get_all_projects_admin() -> List[Dict]:
        """ดึงโครงการทั้งหมด (สำหรับ admin)"""
        conn = ProjectScoringSystem.get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.*, u.first_name, u.last_name, u.employee_id, u.username
            FROM projects p
            JOIN users u ON p.user_id = u.id
            ORDER BY p.score DESC, p.updated_date DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    @staticmethod
    def get_statistics(user_id: int = None) -> Dict:
        """สถิติโครงการ"""
        conn = ProjectScoringSystem.get_db()
        cursor = conn.cursor()
        
        if user_id:
            # สถิติของ user
            cursor.execute('''
                SELECT COUNT(*), SUM(score), AVG(score), MAX(score), MIN(score), 
                       SUM(baseline_manday), AVG(baseline_manday)
                FROM projects WHERE user_id = ?
            ''', (user_id,))
            stats = cursor.fetchone()
            
            cursor.execute('SELECT AVG(progress) FROM projects WHERE user_id = ?', (user_id,))
            avg_progress = cursor.fetchone()[0]
            
            # Count employees (for user it's always 1)
            total_employees = 1
        else:
            # สถิติทั้งหมด (admin)
            cursor.execute('''
                SELECT COUNT(*), SUM(score), AVG(score), MAX(score), MIN(score), 
                       SUM(baseline_manday), AVG(baseline_manday)
                FROM projects
            ''')
            stats = cursor.fetchone()
            
            cursor.execute('SELECT AVG(progress) FROM projects')
            avg_progress = cursor.fetchone()[0]
            
            # Count distinct employees
            cursor.execute('SELECT COUNT(DISTINCT user_id) FROM projects')
            total_employees = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total_projects': stats[0] or 0,
            'total_score': round(stats[1] or 0, 2),
            'avg_score': round(stats[2] or 0, 2),
            'highest_score': stats[3] or 0,
            'lowest_score': stats[4] or 0,
            'total_manday': round(stats[5] or 0, 2),
            'average_baseline_manday': round(stats[6] or 0, 2),
            'average_progress': round(avg_progress or 0, 2),
            'avg_progress': round(avg_progress or 0, 2),
            'total_employees': total_employees
        }


# Initialize database
ProjectScoringSystem.init_database()


# Routes
@app.route('/')
def index():
    """หน้าหลัก - redirect ไป login"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login')
def login():
    """หน้า login"""
    return render_template('login.html')


@app.route('/register')
def register():
    """หน้าสมัครสมาชิก"""
    return render_template('register.html')


@app.route('/dashboard')
@login_required
def dashboard():
    """หน้า dashboard"""
    return render_template('dashboard.html')


@app.route('/admin')
@admin_required
def admin_dashboard():
    """หน้า admin"""
    return render_template('admin.html')


@app.route('/api/login', methods=['POST'])
def api_login():
    """API login"""
    data = request.json
    user = ProjectScoringSystem.verify_user(data['username'], data['password'])
    
    if user:
        session.permanent = True  # ใช้ PERMANENT_SESSION_LIFETIME
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role'] = user['role']
        session['first_name'] = user['first_name']
        session['last_name'] = user['last_name']
        session['employee_id'] = user['employee_id']
        
        return jsonify({
            'success': True,
            'role': user['role'],
            'redirect': '/admin' if user['role'] == 'admin' else '/dashboard'
        })
    
    return jsonify({'success': False, 'error': 'Invalid username or password'}), 401


@app.route('/api/register', methods=['POST'])
def api_register():
    """API สมัครสมาชิก"""
    data = request.json
    
    user_id = ProjectScoringSystem.create_user(
        data['username'],
        data['password'],
        data['first_name'],
        data['last_name'],
        data['employee_id']
    )
    
    if user_id:
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': 'Username or Employee ID already exists'}), 400


@app.route('/api/logout', methods=['POST'])
def api_logout():
    """API logout"""
    session.clear()
    return jsonify({'success': True})


@app.route('/api/user/info', methods=['GET'])
@login_required
def get_user_info():
    """ดึงข้อมูล user ปัจจุบัน"""
    return jsonify({
        'id': session['user_id'],
        'username': session['username'],
        'first_name': session['first_name'],
        'last_name': session['last_name'],
        'employee_id': session['employee_id'],
        'role': session['role']
    })


@app.route('/api/calculate', methods=['POST'])
@login_required
def calculate_score():
    """API คำนวณคะแนนและ baseline manday"""
    data = request.json
    
    score = ProjectScoringSystem.calculate_score(
        data['difficulty_customer'],
        data['difficulty_project'],
        float(data['progress']),
        float(data.get('baseline_pm_effort', 0)),
        float(data.get('project_duration', 1)),
        data.get('challenge_type', 'None')
    )
    
    baseline_manday = ProjectScoringSystem.calculate_baseline_manday(
        data['difficulty_project'],
        float(data.get('baseline_pm_effort', 0)),
        float(data.get('project_duration', 1)),
        data.get('challenge_type', 'None'),
        float(data['progress'])
    )
    
    return jsonify({
        'score': score,
        'baseline_manday': baseline_manday
    })


@app.route('/api/projects', methods=['GET'])
@login_required
def get_projects():
    """API ดึงรายการโครงการ"""
    if session.get('role') == 'admin':
        projects = ProjectScoringSystem.get_all_projects_admin()
    else:
        projects = ProjectScoringSystem.get_user_projects(session['user_id'])
    
    return jsonify(projects)


@app.route('/api/projects', methods=['POST'])
@login_required
def add_project():
    """API เพิ่มโครงการ"""
    data = request.json
    
    try:
        project_id = ProjectScoringSystem.add_project(
            session['user_id'],
            data['project_name'],
            data.get('contract_no', ''),
            data['difficulty_customer'],
            data['difficulty_project'],
            float(data['progress']),
            float(data['baseline_pm_effort']),
            float(data['project_duration']),
            data['challenge_type'],
            data.get('notes', ''),
            int(data.get('project_year', datetime.now().year))
        )
        return jsonify({'success': True, 'project_id': project_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/projects/<int:project_id>', methods=['PUT'])
@login_required
def update_project(project_id):
    """API อัปเดตโครงการ"""
    data = request.json
    
    try:
        success = ProjectScoringSystem.update_project(
            project_id,
            session['user_id'],
            data['project_name'],
            data.get('contract_no', ''),
            data['difficulty_customer'],
            data['difficulty_project'],
            float(data['progress']),
            float(data['baseline_pm_effort']),
            float(data['project_duration']),
            data['challenge_type'],
            data.get('notes', ''),
            int(data.get('project_year', datetime.now().year))
        )
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
@login_required
def delete_project(project_id):
    """API ลบโครงการ"""
    try:
        success = ProjectScoringSystem.delete_project(project_id, session['user_id'])
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/statistics', methods=['GET'])
@login_required
def get_statistics():
    """API ดึงสถิติ"""
    if session.get('role') == 'admin':
        stats = ProjectScoringSystem.get_statistics()
    else:
        stats = ProjectScoringSystem.get_statistics(session['user_id'])
    
    return jsonify(stats)


@app.route('/api/users', methods=['GET'])
@admin_required
def get_users():
    """API ดึงรายชื่อพนักงานทั้งหมด (สำหรับ Admin)"""
    try:
        conn = ProjectScoringSystem.get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, username, first_name, last_name, employee_id, role
            FROM users
            WHERE role = 'employee'
            ORDER BY first_name, last_name
        ''')
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(users)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/export/pdf', methods=['GET'])
@login_required
def export_user_pdf():
    """Export PDF สำหรับ User พร้อม Summary"""
    try:
        user_id = session['user_id']
        user = ProjectScoringSystem.get_user(user_id)
        projects = ProjectScoringSystem.get_user_projects(user_id)
        stats = ProjectScoringSystem.get_statistics(user_id)
        
        # สร้าง PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4),
                              rightMargin=30, leftMargin=30,
                              topMargin=30, bottomMargin=30)
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#3b82f6'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        elements.append(Paragraph('Project Scoring Report', title_style))
        elements.append(Spacer(1, 12))
        
        # User Info
        user_info_style = ParagraphStyle('UserInfo', parent=styles['Normal'], fontSize=12)
        elements.append(Paragraph(f"<b>Employee:</b> {user['first_name']} {user['last_name']}", user_info_style))
        elements.append(Paragraph(f"<b>Employee ID:</b> {user['employee_id']}", user_info_style))
        elements.append(Paragraph(f"<b>Report Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}", user_info_style))
        elements.append(Spacer(1, 20))
        
        # Summary Section
        summary_title = ParagraphStyle('SummaryTitle', parent=styles['Heading2'],
                                      fontSize=16, textColor=colors.HexColor('#1e40af'),
                                      spaceAfter=10)
        elements.append(Paragraph('Summary', summary_title))
        
        summary_data = [
            ['Metric', 'Value'],
            ['Total Projects', str(stats['total_projects'])],
            ['Total Score', f"{stats['total_score']:.2f}"],
            ['Average Score', f"{stats['avg_score']:.2f}"],
            ['Total Manday', f"{stats['total_manday']:.2f}"],
            ['Average Progress', f"{stats['avg_progress']:.1f}%"]
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
        
        # Projects Table
        projects_title = ParagraphStyle('ProjectsTitle', parent=styles['Heading2'],
                                       fontSize=16, textColor=colors.HexColor('#1e40af'),
                                       spaceAfter=10)
        elements.append(Paragraph('Project Details', projects_title))
        
        # Table data
        table_data = [['No.', 'Project Name', 'Year', 'Customer', 'Project Type', 
                      'PM Effort', 'Duration', 'Progress', 'Score', 'Manday']]
        
        for idx, project in enumerate(projects, 1):
            table_data.append([
                str(idx),
                project['project_name'][:30],
                str(project.get('project_year', '-')),
                project['difficulty_customer'][:15],
                project['difficulty_project'][:20],
                str(project['baseline_pm_effort']),
                f"{project['project_duration']} Y",
                f"{project['progress']:.0f}%",
                f"{project['score']:.2f}",
                f"{project['baseline_manday']:.2f}"
            ])
        
        # Create table
        projects_table = Table(table_data, colWidths=[0.4*inch, 1.8*inch, 0.6*inch, 1.2*inch, 
                                                      1.5*inch, 0.8*inch, 0.8*inch, 0.8*inch, 
                                                      0.8*inch, 0.9*inch])
        
        projects_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        elements.append(projects_table)
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        filename = f"Project_Report_{user['employee_id']}_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print("=" * 50)
        print("ERROR in export_user_pdf:")
        print(error_detail)
        print("=" * 50)
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/export/pdf/admin', methods=['GET'])
@admin_required
def export_admin_pdf():
    """Export PDF สำหรับ Admin พร้อม Summary ภาพรวม"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        if user_id:
            # Export สำหรับพนักงานคนใด คนหนึ่ง
            user = ProjectScoringSystem.get_user(user_id)
            projects = ProjectScoringSystem.get_user_projects(user_id)
            stats = ProjectScoringSystem.get_statistics(user_id)
            title_text = f'Project Report - {user["first_name"]} {user["last_name"]}'
            filename_prefix = user['employee_id']
        else:
            # Export ภาพรวมทั้งหมด
            projects = ProjectScoringSystem.get_all_projects_admin()
            stats = ProjectScoringSystem.get_statistics()
            title_text = 'Project Scoring - Overview Report'
            filename_prefix = 'All'
            user = None
        
        # สร้าง PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4),
                              rightMargin=30, leftMargin=30,
                              topMargin=30, bottomMargin=30)
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#9333ea'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        elements.append(Paragraph(title_text, title_style))
        elements.append(Spacer(1, 12))
        
        # Report Info
        info_style = ParagraphStyle('Info', parent=styles['Normal'], fontSize=12)
        if user:
            elements.append(Paragraph(f"<b>Employee:</b> {user['first_name']} {user['last_name']}", info_style))
            elements.append(Paragraph(f"<b>Employee ID:</b> {user['employee_id']}", info_style))
        else:
            elements.append(Paragraph(f"<b>Report Type:</b> All Employees Summary", info_style))
        elements.append(Paragraph(f"<b>Report Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}", info_style))
        elements.append(Paragraph(f"<b>Generated By:</b> {session['first_name']} {session['last_name']} (Admin)", info_style))
        elements.append(Spacer(1, 20))
        
        # Summary Section
        summary_title = ParagraphStyle('SummaryTitle', parent=styles['Heading2'],
                                      fontSize=16, textColor=colors.HexColor('#7c3aed'),
                                      spaceAfter=10)
        elements.append(Paragraph('Overall Summary', summary_title))
        
        summary_data = [
            ['Metric', 'Value'],
            ['Total Projects', str(stats['total_projects'])],
            ['Total Employees' if not user else 'Total Projects', 
             str(stats.get('total_employees', stats['total_projects']))],
            ['Total Score', f"{stats['total_score']:.2f}"],
            ['Average Score', f"{stats['avg_score']:.2f}"],
            ['Total Manday', f"{stats['total_manday']:.2f}"],
            ['Average Progress', f"{stats['avg_progress']:.1f}%"]
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9333ea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lavender),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
        
        # Projects Table
        projects_title = ParagraphStyle('ProjectsTitle', parent=styles['Heading2'],
                                       fontSize=16, textColor=colors.HexColor('#7c3aed'),
                                       spaceAfter=10)
        elements.append(Paragraph('Project Details', projects_title))
        
        # Table headers
        if user:
            table_data = [['No.', 'Project', 'Year', 'Customer', 'Type', 
                          'PM', 'Dur.', 'Progress', 'Score', 'Manday']]
        else:
            table_data = [['No.', 'Project', 'Employee', 'Year', 'Customer', 
                          'PM', 'Dur.', 'Progress', 'Score', 'Manday']]
        
        for idx, project in enumerate(projects, 1):
            if user:
                table_data.append([
                    str(idx),
                    project['project_name'][:25],
                    str(project.get('project_year', '-')),
                    project['difficulty_customer'][:12],
                    project['difficulty_project'][:15],
                    str(project['baseline_pm_effort']),
                    f"{project['project_duration']}Y",
                    f"{project['progress']:.0f}%",
                    f"{project['score']:.2f}",
                    f"{project['baseline_manday']:.2f}"
                ])
            else:
                table_data.append([
                    str(idx),
                    project['project_name'][:20],
                    f"{project['first_name']} {project['last_name']}"[:15],
                    str(project.get('project_year', '-')),
                    project['difficulty_customer'][:10],
                    str(project['baseline_pm_effort']),
                    f"{project['project_duration']}Y",
                    f"{project['progress']:.0f}%",
                    f"{project['score']:.2f}",
                    f"{project['baseline_manday']:.2f}"
                ])
        
        # Create table with appropriate column widths
        if user:
            col_widths = [0.4*inch, 1.8*inch, 0.6*inch, 1*inch, 1.2*inch, 
                         0.6*inch, 0.6*inch, 0.8*inch, 0.8*inch, 0.9*inch]
        else:
            col_widths = [0.4*inch, 1.5*inch, 1.2*inch, 0.6*inch, 0.9*inch,
                         0.6*inch, 0.6*inch, 0.8*inch, 0.8*inch, 0.9*inch]
        
        projects_table = Table(table_data, colWidths=col_widths)
        
        projects_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9333ea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('TOPPADDING', (0, 1), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        elements.append(projects_table)
        
        # Footer
        elements.append(Spacer(1, 20))
        footer_style = ParagraphStyle('Footer', parent=styles['Normal'], 
                                     fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
        elements.append(Paragraph(
            f'Generated by Project Scoring System | {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            footer_style
        ))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        filename = f"Project_Report_{filename_prefix}_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print("=" * 50)
        print("ERROR in export_admin_pdf:")
        print(error_detail)
        print("=" * 50)
        return jsonify({'success': False, 'error': str(e)}), 400


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
