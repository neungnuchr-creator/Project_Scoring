"""
สคริปต์สำหรับล้าง Database และสร้างใหม่
ใช้สำหรับ Demo หรือ Testing
"""

import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

DATABASE = 'project_scoring.db'

def clear_and_init_database():
    """ลบและสร้าง Database ใหม่"""
    
    # ลบ database เก่า
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
        print(f"✅ ลบ database เก่า: {DATABASE}")
    
    # สร้างการเชื่อมต่อใหม่
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("🔨 กำลังสร้าง tables...")
    
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
    print("✅ สร้าง users table")
    
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
            project_year INTEGER,
            difficulty TEXT,
            customer_type TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    print("✅ สร้าง projects table")
    
    # สร้าง default admin user
    admin_password = generate_password_hash('admin123')
    cursor.execute('''
        INSERT INTO users (username, password, first_name, last_name, employee_id, role, created_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', ('admin', admin_password, 'Admin', 'System', 'ADMIN001', 
          'admin', datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    print("✅ สร้าง admin user (username: admin, password: admin123)")
    
    # สร้าง demo users
    demo_users = [
        ('user1', 'user123', 'สมชาย', 'ใจดี', 'EMP001', 'employee'),
        ('user2', 'user123', 'สมหญิง', 'รักสวย', 'EMP002', 'employee'),
        ('user3', 'user123', 'วิชัย', 'มั่นคง', 'EMP003', 'employee'),
    ]
    
    for username, password, first_name, last_name, emp_id, role in demo_users:
        hashed_password = generate_password_hash(password)
        cursor.execute('''
            INSERT INTO users (username, password, first_name, last_name, employee_id, role, created_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (username, hashed_password, first_name, last_name, emp_id, 
              role, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    print(f"✅ สร้าง demo users ({len(demo_users)} คน)")
    print("   - user1/user123 (สมชาย ใจดี - EMP001)")
    print("   - user2/user123 (สมหญิง รักสวย - EMP002)")
    print("   - user3/user123 (วิชัย มั่นคง - EMP003)")
    
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 50)
    print("✅ Database สร้างเสร็จแล้ว!")
    print("=" * 50)
    print("\n📝 ข้อมูล Login:")
    print("   ✅ Admin user ถูกสร้างแล้ว")
    print("   ✅ Demo users ถูกสร้างแล้ว (3 คน)")
    print("\n⚠️  สำคัญ:")
    print("   - เปลี่ยนรหัสผ่าน admin ทันทีหลัง login ครั้งแรก")
    print("   - ข้อมูล login เก็บไว้ในเอกสารที่ปลอดภัย")
    print("\n🚀 พร้อมใช้งานแล้ว!")

if __name__ == '__main__':
    confirm = input("\n⚠️  คำเตือน: คุณต้องการลบ database และสร้างใหม่? (yes/no): ")
    if confirm.lower() in ['yes', 'y']:
        clear_and_init_database()
    else:
        print("❌ ยกเลิกการล้าง database")

