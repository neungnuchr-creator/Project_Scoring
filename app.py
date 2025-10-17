from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production-12345'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)  # Session timeout 1 ชั่วโมง

# Database configuration
DATABASE = 'project_scoring.db'

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
                SELECT COUNT(*), SUM(score), MAX(score), MIN(score), AVG(baseline_manday)
                FROM projects WHERE user_id = ?
            ''', (user_id,))
            stats = cursor.fetchone()
            
            cursor.execute('SELECT AVG(progress) FROM projects WHERE user_id = ?', (user_id,))
            avg_progress = cursor.fetchone()[0]
        else:
            # สถิติทั้งหมด (admin)
            cursor.execute('''
                SELECT COUNT(*), SUM(score), MAX(score), MIN(score), AVG(baseline_manday)
                FROM projects
            ''')
            stats = cursor.fetchone()
            
            cursor.execute('SELECT AVG(progress) FROM projects')
            avg_progress = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_projects': stats[0] or 0,
            'total_score': round(stats[1] or 0, 2),  # เปลี่ยนจาก average เป็น total
            'highest_score': stats[2] or 0,
            'lowest_score': stats[3] or 0,
            'average_progress': round(avg_progress or 0, 2),
            'average_baseline_manday': round(stats[4] or 0, 2)
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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
