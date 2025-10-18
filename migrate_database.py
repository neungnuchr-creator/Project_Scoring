"""
Migration Script - เพิ่ม email และ approved columns
สำหรับ database เก่าที่ไม่มี columns เหล่านี้
"""

import sqlite3
import os
from datetime import datetime

DATABASE = 'project_scoring.db'

def check_column_exists(cursor, table, column):
    """ตรวจสอบว่า column มีอยู่หรือไม่"""
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [row[1] for row in cursor.fetchall()]
    return column in columns

def migrate_database():
    """Migration: เพิ่ม email และ approved columns"""
    
    print("=" * 60)
    print("  🔄 Database Migration - Add Email & Approval System")
    print("=" * 60)
    print()
    
    # ตรวจสอบว่ามี database หรือไม่
    if not os.path.exists(DATABASE):
        print(f"❌ Error: ไม่พบ database '{DATABASE}'")
        print("   กรุณาสร้าง database ก่อนหรือใช้ clear_database.py")
        return False
    
    # Backup database ก่อน
    backup_file = f"{DATABASE}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    import shutil
    shutil.copy2(DATABASE, backup_file)
    print(f"✅ สำรองข้อมูลแล้ว: {backup_file}")
    print()
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        print("🔍 ตรวจสอบ database schema...")
        print()
        
        # ตรวจสอบและเพิ่ม email column
        if not check_column_exists(cursor, 'users', 'email'):
            print("📝 กำลังเพิ่ม column 'email' ใน users table...")
            cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")
            
            # อัพเดท email สำหรับ users ที่มีอยู่แล้ว
            cursor.execute("SELECT id, employee_id FROM users")
            users = cursor.fetchall()
            
            for user_id, emp_id in users:
                # สร้าง email จาก employee_id
                email = f"{emp_id.lower()}@g-able.com"
                cursor.execute("UPDATE users SET email = ? WHERE id = ?", (email, user_id))
            
            print(f"   ✅ เพิ่ม email column และอัพเดท {len(users)} users")
        else:
            print("   ✅ column 'email' มีอยู่แล้ว")
        
        # ตรวจสอบและเพิ่ม approved column
        if not check_column_exists(cursor, 'users', 'approved'):
            print("📝 กำลังเพิ่ม column 'approved' ใน users table...")
            cursor.execute("ALTER TABLE users ADD COLUMN approved INTEGER NOT NULL DEFAULT 1")
            
            # ตั้ง admin และ users ที่มีอยู่ให้ approved = 1
            cursor.execute("UPDATE users SET approved = 1")
            
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            print(f"   ✅ เพิ่ม approved column และอนุมัติ {count} users ที่มีอยู่แล้ว")
        else:
            print("   ✅ column 'approved' มีอยู่แล้ว")
        
        # ตรวจสอบและเพิ่ม project_year column
        if not check_column_exists(cursor, 'projects', 'project_year'):
            print("📝 กำลังเพิ่ม column 'project_year' ใน projects table...")
            cursor.execute("ALTER TABLE projects ADD COLUMN project_year INTEGER")
            
            # ตั้งค่า default เป็นปีปัจจุบัน
            current_year = datetime.now().year
            cursor.execute("UPDATE projects SET project_year = ? WHERE project_year IS NULL", (current_year,))
            print(f"   ✅ เพิ่ม project_year column (default: {current_year})")
        else:
            print("   ✅ column 'project_year' มีอยู่แล้ว")
        
        # Commit changes
        conn.commit()
        conn.close()
        
        print()
        print("=" * 60)
        print("  ✅ Migration สำเร็จ!")
        print("=" * 60)
        print()
        print("📝 สรุปการเปลี่ยนแปลง:")
        print("   ✅ users.email - เพิ่มแล้ว")
        print("   ✅ users.approved - เพิ่มแล้ว")
        print("   ✅ projects.project_year - เพิ่มแล้ว")
        print()
        print("💾 Backup file:", backup_file)
        print()
        print("🚀 พร้อมใช้งานระบบใหม่แล้ว!")
        print("   - Email validation (@g-able.com)")
        print("   - Approval system")
        print("   - User management for admin")
        print()
        
        return True
        
    except Exception as e:
        print()
        print("=" * 60)
        print("  ❌ Migration ไม่สำเร็จ!")
        print("=" * 60)
        print(f"Error: {e}")
        print()
        print("💡 คุณสามารถ restore จาก backup:")
        print(f"   1. ลบไฟล์ {DATABASE}")
        print(f"   2. เปลี่ยนชื่อ {backup_file} เป็น {DATABASE}")
        print()
        return False

def rollback_migration():
    """Rollback migration - กู้คืนจาก backup ล่าสุด"""
    import glob
    
    backups = glob.glob(f"{DATABASE}.backup_*")
    if not backups:
        print("❌ ไม่พบไฟล์ backup")
        return
    
    # ใช้ backup ล่าสุด
    latest_backup = max(backups)
    
    print(f"🔄 Rollback from: {latest_backup}")
    confirm = input("ยืนยันการ rollback? (yes/no): ")
    
    if confirm.lower() in ['yes', 'y']:
        if os.exists(DATABASE):
            os.remove(DATABASE)
        
        import shutil
        shutil.copy2(latest_backup, DATABASE)
        
        print("✅ Rollback สำเร็จ!")
        print(f"   Database กลับไปเป็น: {latest_backup}")
    else:
        print("❌ ยกเลิก rollback")

if __name__ == '__main__':
    print()
    print("=" * 60)
    print("  Database Migration Tool")
    print("=" * 60)
    print()
    print("เลือกคำสั่ง:")
    print("  1. Migrate (เพิ่ม email และ approved columns)")
    print("  2. Rollback (กู้คืนจาก backup)")
    print("  3. ยกเลิก")
    print()
    
    choice = input("เลือก (1-3): ")
    
    if choice == '1':
        print()
        confirm = input("⚠️  ยืนยันการ migrate database? (yes/no): ")
        if confirm.lower() in ['yes', 'y']:
            success = migrate_database()
            if not success:
                print()
                print("💡 Tip: ตรวจสอบว่า Flask app ไม่ได้รันอยู่ (database อาจถูกล็อก)")
        else:
            print("❌ ยกเลิก migration")
    elif choice == '2':
        rollback_migration()
    else:
        print("❌ ยกเลิก")

