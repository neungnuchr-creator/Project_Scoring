# 🔐 Security Guide - Project Scoring System

## 📋 สารบัญ
1. [การเข้าถึงระบบ](#การเข้าถึงระบบ)
2. [การเปลี่ยนรหัสผ่าน](#การเปลี่ยนรหัสผ่าน)
3. [Best Practices](#best-practices)
4. [Troubleshooting](#troubleshooting)

---

## 🔑 การเข้าถึงระบบ

### Admin Account

**สำหรับผู้ดูแลระบบ:**
- ข้อมูล login เก็บไว้ในไฟล์ `ADMIN_CREDENTIALS.txt`
- **⚠️ ไฟล์นี้ไม่ควร commit ไปใน GitHub!**
- เปิดไฟล์เพื่อดูข้อมูล login ครั้งแรก
- **เปลี่ยนรหัสผ่านทันทีหลัง login ครั้งแรก!**

### User Accounts

**สำหรับพนักงาน:**
- สมัครผ่านหน้า Register
- Email ต้องเป็น `@g-able.com` เท่านั้น
- รอ Admin อนุมัติก่อนใช้งาน

---

## 🔄 การเปลี่ยนรหัสผ่าน

### วิธีที่ 1: ใช้ Script (แนะนำ)

```bash
python change_admin_password.py
```

**ขั้นตอน:**
1. รันคำสั่งด้านบน
2. กรอกรหัสผ่านใหม่ (อย่างน้อย 8 ตัวอักษร)
3. ยืนยันรหัสผ่าน
4. เสร็จสิ้น!

**ข้อกำหนดรหัสผ่าน:**
- ✅ ความยาวอย่างน้อย 8 ตัวอักษร
- ✅ ควรมีตัวพิมพ์ใหญ่-เล็ก
- ✅ ควรมีตัวเลข
- ✅ ควรมีสัญลักษณ์พิเศษ

**ตัวอย่างรหัสผ่านที่ดี:**
```
MyP@ssw0rd2025!
Sec

ure#Pass123
G-able@2025Strong
```

---

### วิธีที่ 2: ผ่าน Python (Manual)

```python
from werkzeug.security import generate_password_hash
import sqlite3

# กำหนดรหัสผ่านใหม่
new_password = "YOUR_NEW_STRONG_PASSWORD"

# Hash password
hashed = generate_password_hash(new_password)

# Update database
conn = sqlite3.connect('project_scoring.db')
cursor = conn.cursor()
cursor.execute("UPDATE users SET password = ? WHERE username = 'admin'", (hashed,))
conn.commit()
conn.close()

print("✅ Password changed successfully!")
```

---

## 🛡️ Best Practices

### ✅ ควรทำ:

1. **เปลี่ยนรหัสผ่าน Default ทันที**
   - อย่าใช้ admin123 ใน Production
   - เปลี่ยนทันทีหลังติดตั้ง

2. **ใช้รหัสผ่านที่แข็งแรง**
   - อย่างน้อย 12+ ตัวอักษร
   - ผสมตัวพิมพ์ใหญ่-เล็ก, ตัวเลข, สัญลักษณ์
   - ไม่ใช้คำง่ายๆ หรือข้อมูลส่วนตัว

3. **เก็บรหัสผ่านให้ปลอดภัย**
   - ใช้ Password Manager
   - ไม่แชร์กับผู้อื่น
   - ไม่บันทึกใน plain text

4. **จำกัดการเข้าถึง**
   - ใช้ HTTPS ใน Production
   - ตั้งค่า Firewall
   - ใช้ VPN ถ้าเข้าจากภายนอก

5. **สำรองข้อมูล**
   - Backup database เป็นประจำ
   - เก็บ backup ในที่ปลอดภัย

6. **ตรวจสอบเป็นประจำ**
   - ดู logs การเข้าใช้งาน
   - ตรวจสอบ user ที่ไม่ได้ใช้งาน
   - Review permissions

---

### ❌ ไม่ควรทำ:

1. **ไม่แชร์รหัสผ่าน**
   - แม้กับเพื่อนร่วมงาน
   - ใช้ Role-Based Access แทน

2. **ไม่ใช้รหัสผ่านง่ายๆ**
   - ❌ admin, password, 12345678
   - ❌ ชื่อบริษัท, วันเกิด

3. **ไม่ commit credentials**
   - ❌ อย่า push ADMIN_CREDENTIALS.txt
   - ❌ อย่า commit .env files
   - ใช้ .gitignore

4. **ไม่ใช้ HTTP ใน Production**
   - ต้องใช้ HTTPS เสมอ
   - Password จะถูกเข้ารหัส

5. **ไม่ทิ้ง Default Accounts**
   - ลบหรือปิดการใช้งาน demo users
   - เก็บเฉพาะ accounts ที่จำเป็น

---

## 🔒 การจัดการ User Accounts

### สำหรับ Admin:

**อนุมัติ User ใหม่:**
1. Login เข้า Admin Dashboard
2. ไปที่หน้า "User Management" (กำลังพัฒนา)
3. ดู users ที่รออนุมัติ
4. คลิก "Approve" หรือ "Reject"

**ลบ User:**
```sql
-- ลบ user และโครงการทั้งหมด
DELETE FROM projects WHERE user_id = [USER_ID];
DELETE FROM users WHERE id = [USER_ID];
```

**Reset Password User:**
```python
# ใช้ script change_admin_password.py แต่แก้ username
```

---

## 🚨 Incident Response

### ถ้ารหัสผ่าน Admin รั่วไหล:

1. **เปลี่ยนรหัสผ่านทันที**
   ```bash
   python change_admin_password.py
   ```

2. **ตรวจสอบ Logs**
   - ดู login attempts
   - ตรวจสอบการเปลี่ยนแปลงข้อมูล

3. **แจ้ง Team**
   - แจ้งผู้เกี่ยวข้อง
   - Review security procedures

4. **Backup Database**
   - Backup ทันที
   - เก็บ backup ก่อนแก้ไข

---

## 🔐 Environment Variables

### สำหรับ Production:

**ตั้งค่าใน Railway/Heroku:**
```bash
SECRET_KEY=<สุ่มค่าใหม่ 64 ตัวอักษร>
DATABASE_PATH=project_scoring.db
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**ห้าม:**
- ❌ Commit .env files
- ❌ ใช้ค่า default ใน Production
- ❌ แชร์ SECRET_KEY

---

## 📊 Audit Log (Future Feature)

**จะมีในเวอร์ชันถัดไป:**
- ✅ Log การ login/logout
- ✅ Log การเปลี่ยนแปลงข้อมูล
- ✅ Log การอนุมัติ users
- ✅ Export logs เป็น CSV/PDF

---

## 🆘 Troubleshooting

### ลืมรหัสผ่าน Admin:

**วิธีแก้:**
```bash
python change_admin_password.py
```

---

### ไม่สามารถเข้า Admin Dashboard:

**ตรวจสอบ:**
1. Username และ Password ถูกต้องหรือไม่?
2. Account เป็น role 'admin' หรือไม่?
3. Database มีปัญหาหรือไม่?

**แก้ไข:**
```python
import sqlite3

conn = sqlite3.connect('project_scoring.db')
cursor = conn.cursor()

# ตรวจสอบ admin user
cursor.execute("SELECT username, role FROM users WHERE username = 'admin'")
print(cursor.fetchone())

# ถ้า role ไม่ใช่ admin
cursor.execute("UPDATE users SET role = 'admin' WHERE username = 'admin'")
conn.commit()
conn.close()
```

---

### Database Locked:

**วิธีแก้:**
```bash
# ปิด processes ที่ใช้งาน database
# Windows:
taskkill /F /IM python.exe

# รัน app ใหม่
python app.py
```

---

## 📞 ติดต่อ

**หากพบปัญหาด้านความปลอดภัย:**
1. แจ้งทีม IT Security ทันที
2. ส่ง email: security@g-able.com
3. อย่าแชร์รายละเอียดในที่สาธารณะ

---

## 📚 เอกสารเพิ่มเติม

- `ADMIN_CREDENTIALS.txt` - ข้อมูล login (confidential)
- `change_admin_password.py` - Script เปลี่ยนรหัสผ่าน
- `.env.example` - ตัวอย่าง environment variables
- `RAILWAY_DEPLOY_GUIDE.md` - คู่มือ deploy

---

**อัพเดทล่าสุด:** October 2025  
**Version:** 4.1  
**ผู้ดูแล:** IT Security Team

