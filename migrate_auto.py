"""
Auto Migration Script - เพิ่ม email และ approved columns
รันอัตโนมัติโดยไม่ต้องรอ input
"""

import sqlite3
import os
from datetime import datetime
import shutil

DATABASE = 'project_scoring.db'

def check_column_exists(cursor, table, column):
    """ตรวจสอบว่า column มีอยู่หรือไม่"""
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [row[1] for row in cursor.fetchall()]
    return column in columns

def migrate_database():
    """Migration: เพิ่ม email และ approved columns อัตโนมัติ"""
    
    print("=" * 60)
    print("  Auto Migration - Add Email & Approval System")
    print("=" * 60)
    print()
    
    # ตรวจสอบว่ามี database หรือไม่
    if not os.path.exists(DATABASE):
        print(f"❌ Error: ไม่พบ database '{DATABASE}'")
        return False
    
    # Backup database ก่อน
    backup_file = f"{DATABASE}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(DATABASE, backup_file)
    print(f"✅ สำรองข้อมูล: {backup_file}")
    print()
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        changes_made = False
        
        # เพิ่ม email column
        if not check_column_exists(cursor, 'users', 'email'):
            print("📝 เพิ่ม column 'email'...")
            cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")
            
            # อัพเดท email สำหรับ users ที่มีอยู่
            cursor.execute("SELECT id, username, employee_id FROM users")
            users = cursor.fetchall()
            
            for user_id, username, emp_id in users:
                email = f"{username}@g-able.com"
                cursor.execute("UPDATE users SET email = ? WHERE id = ?", (email, user_id))
            
            print(f"   ✅ เพิ่มและอัพเดท {len(users)} users")
            changes_made = True
        else:
            print("✅ column 'email' มีอยู่แล้ว")
        
        # เพิ่ม approved column
        if not check_column_exists(cursor, 'users', 'approved'):
            print("📝 เพิ่ม column 'approved'...")
            cursor.execute("ALTER TABLE users ADD COLUMN approved INTEGER NOT NULL DEFAULT 1")
            cursor.execute("UPDATE users SET approved = 1")
            
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            print(f"   ✅ อนุมัติ {count} users ที่มีอยู่")
            changes_made = True
        else:
            print("✅ column 'approved' มีอยู่แล้ว")
        
        # เพิ่ม project_year column
        if not check_column_exists(cursor, 'projects', 'project_year'):
            print("📝 เพิ่ม column 'project_year'...")
            cursor.execute("ALTER TABLE projects ADD COLUMN project_year INTEGER")
            
            current_year = datetime.now().year
            cursor.execute("UPDATE projects SET project_year = ? WHERE project_year IS NULL", (current_year,))
            print(f"   ✅ ตั้งค่า default: {current_year}")
            changes_made = True
        else:
            print("✅ column 'project_year' มีอยู่แล้ว")
        
        if changes_made:
            conn.commit()
            print()
            print("=" * 60)
            print("  ✅ Migration สำเร็จ!")
            print("=" * 60)
            print()
            print("💾 Backup:", backup_file)
        else:
            print()
            print("=" * 60)
            print("  ℹ️  Database อัพเดทล่าสุดอยู่แล้ว - ไม่ต้อง migrate")
            print("=" * 60)
            print()
            # ลบ backup ถ้าไม่ได้เปลี่ยนอะไร
            os.remove(backup_file)
        
        conn.close()
        return True
        
    except Exception as e:
        print()
        print("=" * 60)
        print("  ❌ Migration ไม่สำเร็จ!")
        print("=" * 60)
        print(f"Error: {e}")
        print()
        print("💡 Restore จาก backup:")
        print(f"   copy {backup_file} {DATABASE}")
        return False

if __name__ == '__main__':
    migrate_database()

