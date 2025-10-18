# 🎯 คู่มือติดตั้งระบบแบบครบถ้วน - Project Scoring System v4.1

## 📋 สรุป Features ใหม่

### ✨ **Version 4.1 - Email & Approval System**

1. ✅ **Email Validation** - ต้องใช้ @g-able.com
2. ✅ **Approval System** - รอ admin อนุมัติก่อนใช้งาน
3. ✅ **User Management** - Admin จัดการ users ได้
4. ✅ **Custom Scrollbar** - UI สวยงามขึ้น
5. ✅ **Security Enhanced** - ไม่แสดง credentials บนหน้าเว็บ
6. ✅ **Docker Support** - รัน Docker ได้
7. ✅ **Railway Support** - Deploy บน Railway.app ได้

---

## 🚀 Quick Start (3 ขั้นตอน)

### สำหรับ Database ใหม่:

```bash
# 1. สร้าง database
python clear_database.py
# พิมพ์: yes

# 2. รัน app
python app.py

# 3. เปิดเว็บ
http://localhost:5000
```

### สำหรับ Database เก่า (Migration):

```bash
# 1. Migrate database
python migrate_database.py
# เลือก: 1 (Migrate)
# พิมพ์: yes

# 2. รัน app  
python app.py

# 3. เปิดเว็บ
http://localhost:5000
```

---

## 📦 ไฟล์สำคัญทั้งหมด:

### **Core Files:**
- `app.py` - Flask backend (1,100+ บรรทัด)
- `templates/` - HTML templates
  - `login.html` - หน้า Login
  - `register.html` - หน้าสมัครสมาชิก (มีช่อง Email)
  - `dashboard.html` - หน้า User Dashboard
  - `admin.html` - หน้า Admin Dashboard
- `requirements.txt` - Python dependencies

### **Database:**
- `project_scoring.db` - SQLite database
- `clear_database.py` - สร้าง database ใหม่
- `migrate_database.py` - Migrate database เก่า

### **Security:**
- `ADMIN_CREDENTIALS.txt` - ข้อมูล login (confidential)
- `change_admin_password.py` - เปลี่ยนรหัสผ่าน
- `SECURITY_GUIDE.md` - คู่มือความปลอดภัย

### **Docker:**
- `Dockerfile` - Docker configuration
- `docker-compose.yml` - Docker Compose config
- `.dockerignore` - ไฟล์ที่ไม่ copy
- `DOCKER_GUIDE.md` - คู่มือ Docker

### **Railway:**
- `nixpacks.toml` - ⭐ สำคัญ! แก้ SQLite error
- `railway.json` - Railway config
- `Procfile` - Start command
- `runtime.txt` - Python version
- `RAILWAY_DEPLOY_GUIDE.md` - คู่มือ Deploy

### **Documentation:**
- `README.md` - คู่มือหลัก
- `QUICK_START.md` - เริ่มต้นใช้งานเร็ว
- `CHANGE_PASSWORD_GUIDE.md` - เปลี่ยนรหัสผ่าน
- `HOW_TO_ADD_USER_MANAGEMENT.md` - เพิ่ม User Management
- `COMPLETE_SETUP_GUIDE.md` - ไฟล์นี้

---

## 🔧 การติดตั้งแบบละเอียด:

### **ขั้นตอนที่ 1: เตรียม Environment**

```bash
# Clone หรือ Download code
cd C:\Users\User\project-scoring-system

# สร้าง Virtual Environment (แนะนำ)
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# ติดตั้ง dependencies
pip install -r requirements.txt
```

---

### **ขั้นตอนที่ 2: ตั้งค่า Database**

#### **สำหรับ Database ใหม่:**
```bash
python clear_database.py
# พิมพ์: yes
```

ผลลัพธ์:
```
✅ สร้าง admin user
✅ สร้าง demo users (3 คน)
   - user1 (EMP001)
   - user2 (EMP002)  
   - user3 (EMP003)
```

#### **สำหรับ Database เก่า:**
```bash
python migrate_database.py
# เลือก: 1 (Migrate)
# พิมพ์: yes
```

ผลลัพธ์:
```
✅ Backup: project_scoring.db.backup_20251018_143000
✅ เพิ่ม email column
✅ เพิ่ม approved column
✅ เพิ่ม project_year column
```

---

### **ขั้นตอนที่ 3: รัน Application**

```bash
python app.py
```

เปิดเว็บ: **http://localhost:5000**

---

### **ขั้นตอนที่ 4: Login และตั้งค่า**

1. **ดูข้อมูล Login:**
   - เปิดไฟล์ `ADMIN_CREDENTIALS.txt`
   - ดู admin username และ password

2. **Login:**
   - ไปที่ http://localhost:5000
   - Login ด้วย admin credentials

3. **เปลี่ยนรหัสผ่าน:**
   ```bash
   python change_admin_password.py
   ```

---

### **ขั้นตอนที่ 5: เพิ่ม User Management UI (ถ้าต้องการ)**

1. **เปิดไฟล์:**
   - `ADMIN_USER_MANAGEMENT_SNIPPET.html`
   - `templates/admin.html`

2. **Copy code** จาก snippet file

3. **Paste** ใน admin.html (ก่อน Projects List Section)

4. **Save** และ refresh เว็บ

5. **ทดสอบ:**
   - Login เป็น admin
   - ควรเห็น Section "จัดการผู้ใช้งาน"
   - สมัครสมาชิกใหม่เพื่อทดสอบ
   - ทดสอบ approve/reject

📖 **อ่านเพิ่มเติม:** `HOW_TO_ADD_USER_MANAGEMENT.md`

---

## 📊 Database Schema:

### **Users Table:**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    employee_id TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,          -- ใหม่!
    role TEXT DEFAULT 'employee',
    approved INTEGER DEFAULT 0,          -- ใหม่!
    created_date TEXT NOT NULL
)
```

### **Projects Table:**
```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
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
    project_year INTEGER,               -- ใหม่!
    difficulty TEXT,
    customer_type TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
```

---

## 🔐 Security Features:

### ✅ **Email Validation:**
- ต้องเป็น @g-able.com เท่านั้น
- ตรวจสอบทั้ง Frontend และ Backend

### ✅ **Approval System:**
- User ใหม่ `approved = 0` (รออนุมัติ)
- ไม่สามารถ login จนกว่า admin จะอนุมัติ
- Admin `approved = 1` โดยอัตโนมัติ

### ✅ **No Credentials on Web:**
- ลบ admin/password ออกจากหน้า login
- เก็บไว้ใน `ADMIN_CREDENTIALS.txt`
- ไฟล์นี้ไม่ถูก commit ใน Git

### ✅ **Password Management:**
- Script เปลี่ยนรหัสผ่านใช้งานง่าย
- รองรับ Local, Railway, Docker

---

## 🌐 Deployment:

### **Local Development:**
```bash
python app.py
# http://localhost:5000
```

### **Docker:**
```bash
docker-compose up
# http://localhost:5000
```

### **Railway.app:**
```bash
# Push to GitHub
git push origin main

# Railway auto-deploy
# https://your-app.up.railway.app
```

---

## 📞 Troubleshooting:

### ปัญหา: "No module named 'dotenv'"
```bash
pip install python-dotenv
```

### ปัญหา: "NOT NULL constraint failed: users.email"
```bash
# ใช้ migration script
python migrate_database.py
```

### ปัญหา: "Database is locked"
```bash
# ปิด Flask app
taskkill /F /IM python.exe

# รันใหม่
python app.py
```

### ปัญหา: ไม่สามารถสมัครสมาชิกได้
```bash
# ตรวจสอบ console logs
# F12 → Console tab

# ตรวจสอบว่า email เป็น @g-able.com
```

### ปัญหา: Login แล้วแสดง "รออนุมัติ"
```bash
# ปกติ - ต้องรอ admin อนุมัติ
# หรือ อนุมัติด้วยตนเอง:
python
>>> import sqlite3
>>> conn = sqlite3.connect('project_scoring.db')
>>> cursor = conn.cursor()
>>> cursor.execute("UPDATE users SET approved = 1 WHERE username = 'YOUR_USERNAME'")
>>> conn.commit()
>>> conn.close()
```

---

## 📚 คู่มือทั้งหมด:

| คู่มือ | วัตถุประสงค์ |
|-------|------------|
| [README.md](README.md) | คู่มือหลัก |
| [QUICK_START.md](QUICK_START.md) | เริ่มต้นใช้งานเร็ว |
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | Deploy บน Cloud |
| [RAILWAY_DEPLOY_GUIDE.md](RAILWAY_DEPLOY_GUIDE.md) | Deploy บน Railway |
| [DOCKER_GUIDE.md](DOCKER_GUIDE.md) | รัน Docker |
| [SECURITY_GUIDE.md](SECURITY_GUIDE.md) | ความปลอดภัย |
| [CHANGE_PASSWORD_GUIDE.md](CHANGE_PASSWORD_GUIDE.md) | เปลี่ยนรหัสผ่าน |
| [HOW_TO_ADD_USER_MANAGEMENT.md](HOW_TO_ADD_USER_MANAGEMENT.md) | เพิ่ม User Management UI |
| [COMPLETE_SETUP_GUIDE.md](COMPLETE_SETUP_GUIDE.md) | ไฟล์นี้ - คู่มือครบถ้วน |

---

## ✅ Checklist ก่อนใช้งาน Production:

- [ ] ติดตั้ง dependencies ครบ (`pip install -r requirements.txt`)
- [ ] สร้าง/Migrate database แล้ว
- [ ] ทดสอบ login ได้
- [ ] ทดสอบสมัครสมาชิกได้ (email @g-able.com)
- [ ] ทดสอบ approval system ทำงาน
- [ ] เปลี่ยนรหัสผ่าน admin แล้ว
- [ ] ตั้งค่า SECRET_KEY (สำหรับ Production)
- [ ] ทดสอบ Export PDF ได้
- [ ] ลบ demo users (ถ้าไม่ต้องการ)
- [ ] Backup database

---

## 🎓 Flow การใช้งาน:

### **User Registration Flow:**
```
1. User เปิดหน้า /register
2. กรอกข้อมูล (ต้องมี email @g-able.com)
3. ระบบตรวจสอบ email domain
4. สร้าง user ด้วย approved = 0
5. แสดงข้อความ "รอการอนุมัติ"
6. User ไม่สามารถ login ได้
```

### **Admin Approval Flow:**
```
1. Admin login เข้าระบบ
2. ไปหน้า Admin Dashboard
3. เห็น Section "จัดการผู้ใช้งาน"
4. เห็นรายการ users ที่รออนุมัติ
5. คลิก "อนุมัติ" หรือ "ปฏิเสธ"
6. ยืนยันการกระทำ
7. User ที่ approved สามารถ login ได้
```

### **User Login Flow:**
```
1. User ที่ approved แล้ว login
2. ระบบตรวจสอบ approved = 1
3. Login สำเร็จ → Dashboard
```

```
1. User ที่ยัง pending login
2. ระบบตรวจสอบ approved = 0  
3. แสดง error: "รอการอนุมัติจากผู้ดูแลระบบ"
```

---

## 🔑 Default Accounts:

**ดูข้อมูลใน:** `ADMIN_CREDENTIALS.txt`

**Accounts ที่มี:**
- ✅ Admin (approved = 1)
- ✅ Demo User 1-3 (approved = 1)

---

## 🌐 URLs:

| Page | URL | Access |
|------|-----|--------|
| Login | `/login` | Public |
| Register | `/register` | Public |
| User Dashboard | `/dashboard` | User (approved) |
| Admin Dashboard | `/admin` | Admin only |

---

## 🔐 การเปลี่ยนรหัสผ่าน:

### Quick Reference:

```bash
# Local
python change_admin_password.py

# Railway
railway shell
python change_admin_password.py

# Docker
docker exec -it project-scoring python change_admin_password.py
```

📖 **คู่มือเต็ม:** [CHANGE_PASSWORD_GUIDE.md](CHANGE_PASSWORD_GUIDE.md)

---

## 📤 การ Deploy:

### **Docker:**
```bash
.\build_docker.bat
docker-compose up
```
📖 [DOCKER_GUIDE.md](DOCKER_GUIDE.md)

### **Railway:**
```bash
# 1. Push to GitHub
git push origin main

# 2. Deploy on Railway
# Auto-deploy enabled
```
📖 [RAILWAY_DEPLOY_GUIDE.md](RAILWAY_DEPLOY_GUIDE.md)

---

## 🆘 Support:

### หากมีปัญหา:

1. **ตรวจสอบ Console Logs**
   - Browser: F12 → Console
   - Server: Terminal output

2. **อ่านคู่มือที่เกี่ยวข้อง**
   - ดูสารบัญด้านบน

3. **ตรวจสอบ Error Messages**
   - Email validation?
   - Approval pending?
   - Database error?

4. **ติดต่อ IT Support**
   - Email: it-support@g-able.com
   - Teams: IT Support Channel

---

## 🏆 Version History:

- **v4.1** (Oct 2025) - Email validation + Approval system
- **v4.0** (Oct 2025) - Modern UI + PDF Export
- **v3.0** (Oct 2025) - Admin Dashboard
- **v2.0** (Oct 2025) - Multi-user support
- **v1.0** (Oct 2025) - Initial release

---

## 📝 Next Steps (Optional):

### เพิ่มฟีเจอร์ในอนาคต:

- [ ] Email notification เมื่อได้รับการอนุมัติ
- [ ] 2FA (Two-Factor Authentication)
- [ ] Audit logs
- [ ] User profile edit
- [ ] Password reset via email
- [ ] Advanced search และ filters
- [ ] Dashboard analytics
- [ ] Export Excel
- [ ] API documentation

---

**System Ready! 🎉**

**พัฒนาโดย:** G-Able IT Team  
**Version:** 4.1  
**Last Updated:** October 2025

---

**Happy Coding! 💻✨**

