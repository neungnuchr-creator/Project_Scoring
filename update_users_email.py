"""
อัพเดท users ที่มีอยู่ให้มี email และ username เป็น email
"""

import sqlite3
from datetime import datetime

DATABASE = 'project_scoring.db'

def update_users():
    print("=" * 60)
    print("  Update Users - Set Email as Username")
    print("=" * 60)
    print()
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # ดึง users ทั้งหมด
    cursor.execute("SELECT id, username, email FROM users")
    users = cursor.fetchall()
    
    print(f"Found {len(users)} users")
    print()
    
    for user_id, username, email in users:
        if email:
            print(f"User {user_id}: {username} -> Email: {email} (OK)")
        else:
            # ถ้าไม่มี email ให้สร้างจาก username
            new_email = f"{username}@g-able.com"
            cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
            print(f"User {user_id}: {username} -> Created email: {new_email}")
    
    conn.commit()
    conn.close()
    
    print()
    print("=" * 60)
    print("  Done!")
    print("=" * 60)

if __name__ == '__main__':
    update_users()

