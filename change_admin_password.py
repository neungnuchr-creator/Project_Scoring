"""
Script สำหรับเปลี่ยนรหัสผ่าน Admin
ใช้เมื่อต้องการเปลี่ยนรหัสผ่าน admin โดยไม่ผ่านหน้าเว็บ
"""

import sqlite3
from werkzeug.security import generate_password_hash
import getpass

DATABASE = 'project_scoring.db'

def change_admin_password():
    """เปลี่ยนรหัสผ่าน admin"""
    
    print("=" * 60)
    print("  🔐 เปลี่ยนรหัสผ่าน Admin - Project Scoring System")
    print("=" * 60)
    print()
    
    # ตรวจสอบว่ามี database หรือไม่
    import os
    if not os.path.exists(DATABASE):
        print(f"❌ Error: ไม่พบ database '{DATABASE}'")
        print("   กรุณาสร้าง database ก่อนด้วย: python clear_database.py")
        return
    
    # เชื่อมต่อ database
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # ตรวจสอบว่ามี admin user หรือไม่
        cursor.execute("SELECT id, username FROM users WHERE username = 'admin'")
        admin = cursor.fetchone()
        
        if not admin:
            print("❌ Error: ไม่พบ admin user ในระบบ")
            conn.close()
            return
        
        print(f"✅ พบ admin user: {admin[1]} (ID: {admin[0]})")
        print()
        
        # รับรหัสผ่านใหม่
        print("📝 กรอกรหัสผ่านใหม่:")
        print("   - ความยาวอย่างน้อย 8 ตัวอักษร")
        print("   - ควรมีตัวพิมพ์ใหญ่, ตัวพิมพ์เล็ก, ตัวเลข, และสัญลักษณ์")
        print()
        
        while True:
            new_password = getpass.getpass("รหัสผ่านใหม่: ")
            
            if len(new_password) < 8:
                print("❌ รหัสผ่านสั้นเกินไป (ต้องมีอย่างน้อย 8 ตัวอักษร)")
                continue
            
            confirm_password = getpass.getpass("ยืนยันรหัสผ่าน: ")
            
            if new_password != confirm_password:
                print("❌ รหัสผ่านไม่ตรงกัน กรุณาลองใหม่")
                print()
                continue
            
            break
        
        # Hash password
        hashed_password = generate_password_hash(new_password)
        
        # Update database
        cursor.execute("UPDATE users SET password = ? WHERE username = 'admin'", (hashed_password,))
        conn.commit()
        conn.close()
        
        print()
        print("=" * 60)
        print("  ✅ เปลี่ยนรหัสผ่านสำเร็จ!")
        print("=" * 60)
        print()
        print("📝 รายละเอียด:")
        print(f"   - Username: admin")
        print(f"   - รหัสผ่านใหม่: {'*' * len(new_password)}")
        print()
        print("⚠️  หมายเหตุ:")
        print("   - เก็บรหัสผ่านใหม่ให้ดี")
        print("   - ไม่สามารถกู้คืนรหัสผ่านได้")
        print("   - ถ้าลืมรหัสผ่าน ต้องใช้ script นี้เปลี่ยนใหม่")
        print()
        print("🚀 สามารถ login ด้วยรหัสผ่านใหม่ได้เลย!")
        print()
        
    except sqlite3.Error as e:
        print(f"❌ Database Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    try:
        change_admin_password()
    except KeyboardInterrupt:
        print("\n\n❌ ยกเลิกการเปลี่ยนรหัสผ่าน")
    except Exception as e:
        print(f"\n❌ Error: {e}")

