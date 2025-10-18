# 🚂 Railway.app Deployment Guide

## 🎯 ภาพรวม

คู่มือนี้จะสอนวิธีการ deploy Project Scoring System ไปยัง Railway.app แบบฟรี!

---

## 🔧 ปัญหาที่แก้ไข

### ❌ Error เดิม:
```
ImportError: libsqlite3.so.0: cannot open shared object file: No such file or directory
Worker failed to boot.
```

### ✅ วิธีแก้:
สร้างไฟล์ `nixpacks.toml` เพื่อบอก Railway ให้ติดตั้ง SQLite library

---

## 📋 ข้อกำหนดเบื้องต้น

1. ✅ บัญชี GitHub (https://github.com)
2. ✅ บัญชี Railway.app (https://railway.app) - สมัครฟรีด้วย GitHub
3. ✅ Code ใน GitHub Repository

---

## 🚀 ขั้นตอนการ Deploy

### **Step 1: เตรียม Code ใน GitHub**

#### 1.1 ตรวจสอบไฟล์ที่จำเป็น:
```
✅ app.py
✅ templates/ (folder)
✅ requirements.txt
✅ nixpacks.toml        ← สำคัญ! (แก้ปัญหา SQLite)
✅ railway.json
✅ Procfile
✅ runtime.txt
✅ .gitignore
✅ .env.example
```

#### 1.2 Commit และ Push ไป GitHub:
```bash
cd C:\Users\User\project-scoring-system

# ตรวจสอบสถานะ
git status

# Add ไฟล์ใหม่
git add nixpacks.toml railway.json Procfile runtime.txt .env.example .gitignore
git add app.py requirements.txt

# Commit
git commit -m "Add Railway deployment configuration"

# Push
git push origin main
```

หรือใช้ GitHub Desktop:
1. เปิด GitHub Desktop
2. เลือก repository
3. ดูไฟล์ที่เปลี่ยน (Changes)
4. พิมพ์ commit message: "Add Railway deployment configuration"
5. กด "Commit to main"
6. กด "Push origin"

---

### **Step 2: Deploy บน Railway**

#### 2.1 เข้า Railway.app:
1. ไปที่: https://railway.app
2. กด **"Login"** ด้วย GitHub
3. กด **"New Project"**

#### 2.2 เชื่อมต่อ GitHub Repository:
1. เลือก **"Deploy from GitHub repo"**
2. เลือก repository: `project-scoring-system`
3. กด **"Deploy Now"**

#### 2.3 Railway จะ Build อัตโนมัติ:
- ⏳ รอประมาณ 2-5 นาที
- ✅ ดูว่า build สำเร็จ (เขียวปกติ)

---

### **Step 3: ตั้งค่า Environment Variables**

#### 3.1 เปิด Settings:
1. คลิกที่ Project
2. คลิกที่ **"Variables"** tab
3. กด **"+ New Variable"**

#### 3.2 เพิ่ม Variables:

**ตัวอย่าง:**
```
Key: SECRET_KEY
Value: your-super-secret-random-key-change-this-12345678

Key: DATABASE_PATH
Value: project_scoring.db

Key: PORT
Value: 5000
```

#### 3.3 Generate Secret Key (แนะนำ):
```python
# ใน Python
import secrets
print(secrets.token_hex(32))
# Copy ค่าที่ได้ไปใส่ใน SECRET_KEY
```

หรือใน PowerShell:
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

#### 3.4 บันทึก:
- กด **"Add"** หรือ **"Save"**
- Railway จะ restart service อัตโนมัติ

---

### **Step 4: ตรวจสอบ Deployment**

#### 4.1 ดู Logs:
1. คลิกที่ **"Deployments"** tab
2. คลิกที่ deployment ล่าสุด
3. ดู **"View Logs"**

#### 4.2 ต้องเห็น:
```
✅ Build successful
✅ Starting gunicorn
✅ Listening on port 5000
```

#### 4.3 เปิดเว็บ:
1. คลิกที่ **"Settings"** tab
2. ดูที่ **"Domains"** section
3. กด **"Generate Domain"**
4. จะได้ URL เช่น: `https://project-scoring-production.up.railway.app`

#### 4.4 ทดสอบ:
- เปิด URL ที่ได้
- ควรเห็นหน้า Login
- ทดสอบ login ด้วย: `admin` / `admin123`

---

## 🔐 สร้าง Admin User

### วิธีที่ 1: ใช้ Railway CLI

#### 1. ติดตั้ง Railway CLI:
```bash
# Windows (PowerShell)
iwr https://railway.app/install.ps1 -useb | iex

# Mac/Linux
sh -c "$(curl -sSL https://railway.app/install.sh)"
```

#### 2. Login:
```bash
railway login
```

#### 3. Link Project:
```bash
cd C:\Users\User\project-scoring-system
railway link
```

#### 4. เข้าถึง Shell:
```bash
railway shell
```

#### 5. สร้าง Admin:
```bash
python clear_database.py
# หรือ
python
>>> from app import ProjectScoringSystem
>>> ProjectScoringSystem.init_database()
>>> exit()
```

---

### วิธีที่ 2: สร้างผ่านหน้าเว็บ (ง่ายกว่า)

#### สร้าง Admin Route ชั่วคราว:

**แก้ไข `app.py` เพิ่ม route นี้:**
```python
@app.route('/init-admin', methods=['GET', 'POST'])
def init_admin():
    """Route ชั่วคราวสำหรับสร้าง admin - ลบทิ้งหลังใช้งาน"""
    if request.method == 'POST':
        # สร้าง database ใหม่
        ProjectScoringSystem.init_database()
        return jsonify({'success': True, 'message': 'Admin created: admin / admin123'})
    
    return '''
        <html>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>Initialize Admin User</h1>
            <button onclick="init()" style="padding: 10px 20px; font-size: 16px; cursor: pointer;">
                Create Admin User
            </button>
            <div id="result" style="margin-top: 20px;"></div>
            <script>
                function init() {
                    fetch('/init-admin', { method: 'POST' })
                    .then(r => r.json())
                    .then(data => {
                        document.getElementById('result').innerHTML = 
                            '<div style="color: green; font-size: 18px;">' +
                            '<b>✅ Success!</b><br>' +
                            'Username: admin<br>' +
                            'Password: admin123<br>' +
                            '<a href="/login">Go to Login</a>' +
                            '</div>';
                    })
                    .catch(e => {
                        document.getElementById('result').innerHTML = 
                            '<div style="color: red;">Error: ' + e + '</div>';
                    });
                }
            </script>
        </body>
        </html>
    '''
```

**ใช้งาน:**
1. Push code ขึ้น GitHub
2. Railway จะ deploy ใหม่อัตโนมัติ
3. เปิด: `https://your-app.up.railway.app/init-admin`
4. กดปุ่ม "Create Admin User"
5. **ลบ route นี้ทิ้งทันที** (เพื่อความปลอดภัย)

---

## 📊 ตรวจสอบสถานะ

### ดู Resource Usage:
1. เปิด Railway Dashboard
2. ดู **"Metrics"** tab
3. ตรวจสอบ:
   - CPU usage
   - Memory usage
   - Network traffic

### Free Tier Limits:
- ✅ $5 credit/month
- ✅ 500 hours runtime
- ✅ 8GB RAM
- ✅ Custom domain

---

## 🔄 Update Code

### ทุกครั้งที่แก้ไข Code:
```bash
# 1. แก้ไข code
# 2. Test ที่ local

# 3. Commit และ Push
git add .
git commit -m "Update: describe your changes"
git push origin main

# 4. Railway จะ deploy อัตโนมัติ (Auto-deploy)
# 5. รอ 2-5 นาที
# 6. Refresh หน้าเว็บ
```

---

## 🆘 Troubleshooting

### ปัญหา 1: SQLite Error
```
ImportError: libsqlite3.so.0: cannot open shared object file
```

**แก้:**
- ✅ ตรวจสอบว่ามีไฟล์ `nixpacks.toml`
- ✅ เนื้อหาต้องมี:
  ```toml
  [phases.setup]
  nixPkgs = ['python311', 'sqlite']
  ```

---

### ปัญหา 2: Worker Failed to Boot
```
Worker (pid:2) exited with code 3
Worker failed to boot
```

**แก้:**
1. ตรวจสอบ Logs
2. ตรวจสอบว่า `gunicorn` ติดตั้งแล้ว
3. ตรวจสอบ `Procfile`:
   ```
   web: gunicorn app:app --bind 0.0.0.0:$PORT
   ```

---

### ปัญหา 3: Database Not Found
```
no such table: users
```

**แก้:**
- ไปที่ `/init-admin` เพื่อสร้าง database
- หรือใช้ Railway CLI: `railway shell` → `python clear_database.py`

---

### ปัญหา 4: 500 Internal Server Error

**แก้:**
1. ดู Logs ใน Railway Dashboard
2. ตรวจสอบ Environment Variables
3. ตรวจสอบว่า `SECRET_KEY` ตั้งค่าแล้ว

---

### ปัญหา 5: Application Error

**ตรวจสอบ:**
```bash
# ดู logs
railway logs

# หรือใน Dashboard → Deployments → View Logs
```

---

## 🔐 Security Best Practices

### 1. เปลี่ยน SECRET_KEY:
```python
# Generate secure key
import secrets
secrets.token_hex(32)
```

### 2. เปลี่ยน Admin Password:
- Login ด้วย admin
- ไปที่ Settings → Change Password
- หรือสร้าง user ใหม่และลบ admin เดิม

### 3. ไม่ commit .env:
- ✅ ไฟล์ `.env` อยู่ใน `.gitignore`
- ✅ ใช้ `.env.example` แทน

### 4. ลบ /init-admin Route:
- หลังสร้าง admin แล้ว ให้ลบทิ้ง
- Push code ใหม่

---

## 📈 Monitoring

### เปิด Auto-Deploy:
1. Settings → GitHub
2. เปิด **"Auto Deploy"**
3. ทุกครั้งที่ push ไป main branch จะ deploy อัตโนมัติ

### ตั้ง Notifications:
1. Settings → Notifications
2. เชื่อมต่อ Slack/Discord/Email
3. จะได้รับแจ้งเตือนเมื่อ:
   - Deploy สำเร็จ
   - Deploy ล้มเหลว
   - Service down

---

## 💰 ราคา (Free Tier)

### ฟรี:
- ✅ $5 credit/month
- ✅ เพียงพอสำหรับ small app
- ✅ Custom domain
- ✅ SSL/HTTPS ฟรี

### ถ้าเกิน Free Tier:
- Hobby Plan: $5/month
- Pro Plan: $20/month

---

## 📝 ไฟล์สำคัญที่สร้าง

| ไฟล์               | วัตถุประสงค์                          |
|-------------------|--------------------------------------|
| `nixpacks.toml`   | ติดตั้ง SQLite (แก้ ImportError)     |
| `railway.json`    | Railway configuration                |
| `Procfile`        | คำสั่ง start gunicorn                |
| `runtime.txt`     | ระบุ Python version                  |
| `.env.example`    | ตัวอย่าง environment variables       |
| `.gitignore`      | ไฟล์ที่ไม่ต้อง commit                |

---

## 🎯 Checklist การ Deploy

- [ ] สร้างไฟล์ทั้งหมดแล้ว (nixpacks.toml, railway.json, etc.)
- [ ] Push code ไป GitHub
- [ ] สร้าง project บน Railway
- [ ] เชื่อมต่อ GitHub repository
- [ ] ตั้งค่า Environment Variables
- [ ] Generate domain
- [ ] สร้าง admin user
- [ ] ทดสอบ login
- [ ] ทดสอบ CRUD operations
- [ ] ทดสอบ Export PDF
- [ ] ลบ /init-admin route (ถ้ามี)
- [ ] เปลี่ยน admin password

---

## 🔗 Links

- Railway Dashboard: https://railway.app/dashboard
- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway

---

## 🔐 การเปลี่ยนรหัสผ่าน Admin

### ⚠️ สำคัญมาก: ต้องเปลี่ยนรหัสผ่าน Default ทันที!

---

### วิธีที่ 1: ใช้ Script (แนะนำ - ง่ายที่สุด)

**ขั้นตอน:**

1. **Clone repository ลงเครื่อง (ถ้ายังไม่ได้ทำ)**
   ```bash
   git clone https://github.com/YOUR_USERNAME/project-scoring-system.git
   cd project-scoring-system
   ```

2. **ติดตั้ง dependencies**
   ```bash
   pip install werkzeug
   ```

3. **Download database จาก Railway (ถ้าต้องการ)**
   ```bash
   railway link
   railway run python
   # แล้ว copy database file
   ```

4. **รัน script เปลี่ยนรหัสผ่าน**
   ```bash
   python change_admin_password.py
   ```

5. **ทำตามขั้นตอน:**
   ```
   รหัสผ่านใหม่: ********** (กรอกรหัสผ่านใหม่)
   ยืนยันรหัสผ่าน: ********** (กรอกอีกครั้ง)
   ✅ เปลี่ยนรหัสผ่านสำเร็จ!
   ```

6. **Upload database กลับไปที่ Railway**
   ```bash
   # ใช้ Railway CLI หรือ commit และ redeploy
   ```

---

### วิธีที่ 2: ใช้ Railway CLI

**ขั้นตอน:**

1. **ติดตั้ง Railway CLI**
   ```bash
   # Windows PowerShell
   iwr https://railway.app/install.ps1 -useb | iex
   
   # Mac/Linux
   sh -c "$(curl -sSL https://railway.app/install.sh)"
   ```

2. **Login และ Link Project**
   ```bash
   railway login
   cd project-scoring-system
   railway link
   ```

3. **เปิด Shell บน Railway**
   ```bash
   railway shell
   ```

4. **รัน Python**
   ```bash
   python
   ```

5. **เปลี่ยนรหัสผ่าน**
   ```python
   from werkzeug.security import generate_password_hash
   import sqlite3
   
   # กำหนดรหัสผ่านใหม่
   new_password = "YOUR_NEW_STRONG_PASSWORD"  # เปลี่ยนตรงนี้!
   
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

6. **ออกจาก Python**
   ```python
   exit()
   ```

7. **Restart Service**
   - ไปที่ Railway Dashboard → Deployments → Restart

---

### วิธีที่ 3: สร้าง Admin ใหม่และลบเก่า

**ขั้นตอน:**

1. **สมัครสมาชิกใหม่** ที่หน้าเว็บ (ใช้ email @g-able.com)

2. **ใช้ Railway CLI เข้า database**
   ```bash
   railway shell
   python
   ```

3. **เปลี่ยน Role เป็น Admin**
   ```python
   import sqlite3
   
   conn = sqlite3.connect('project_scoring.db')
   cursor = conn.cursor()
   
   # เปลี่ยน user ใหม่เป็น admin
   cursor.execute("UPDATE users SET role = 'admin', approved = 1 WHERE username = 'YOUR_NEW_USERNAME'")
   
   # ลบ admin เก่า
   cursor.execute("DELETE FROM users WHERE username = 'admin'")
   
   conn.commit()
   conn.close()
   
   print("✅ New admin created, old admin deleted!")
   ```

---

### วิธีที่ 4: ผ่าน Init Admin Route (ชั่วคราว)

**⚠️ วิธีนี้มีความเสี่ยง - ใช้เฉพาะในกรณีฉุกเฉิน**

1. **แก้ไข app.py เพิ่ม route ชั่วคราว**
   ```python
   @app.route('/reset-admin-password', methods=['GET', 'POST'])
   def reset_admin_password():
       if request.method == 'POST':
           from werkzeug.security import generate_password_hash
           new_password = request.form.get('new_password')
           hashed = generate_password_hash(new_password)
           
           conn = ProjectScoringSystem.get_db()
           cursor = conn.cursor()
           cursor.execute("UPDATE users SET password = ? WHERE username = 'admin'", (hashed,))
           conn.commit()
           conn.close()
           
           return jsonify({'success': True, 'message': 'Password changed!'})
       
       return '''
       <form method="post">
           New Password: <input type="password" name="new_password" required>
           <button type="submit">Change Password</button>
       </form>
       '''
   ```

2. **Push และ Deploy**

3. **เข้าไปที่:**
   ```
   https://your-app.up.railway.app/reset-admin-password
   ```

4. **⚠️ ลบ route ทันทีหลังใช้งาน!**

---

## 💡 ข้อกำหนดรหัสผ่านที่ดี

### ✅ รหัสผ่านที่แข็งแรง:

**ความยาว:**
- อย่างน้อย 12 ตัวอักษร
- แนะนำ 16+ ตัวอักษร

**ความซับซ้อน:**
- ✅ ตัวพิมพ์ใหญ่ (A-Z)
- ✅ ตัวพิมพ์เล็ก (a-z)
- ✅ ตัวเลข (0-9)
- ✅ สัญลักษณ์พิเศษ (!@#$%^&*)

**ตัวอย่างรหัสผ่านที่ดี:**
```
MySecure@Pass2025!
G-able#Proj2025Strong
Admin$Railway!2025Secure
P@ssw0rd!Scoring#2025
```

**ตัวอย่างรหัสผ่านที่ไม่ดี:**
```
❌ admin123
❌ password
❌ 12345678
❌ gable2025
❌ projectscoring
```

---

## 🔒 การตรวจสอบว่าเปลี่ยนสำเร็จ

### วิธีทดสอบ:

1. **ออกจากระบบ (Logout)**

2. **พยายาม Login ด้วยรหัสผ่านเก่า**
   - ถ้า Login ไม่ได้ = ✅ สำเร็จ!
   - ถ้า Login ได้ = ❌ ยังไม่เปลี่ยน

3. **Login ด้วยรหัสผ่านใหม่**
   - ถ้า Login ได้ = ✅ สำเร็จ!

---

## 📝 บันทึกรหัสผ่านให้ปลอดภัย

### แนะนำ Password Managers:

**ฟรี:**
- ✅ **Bitwarden** (Open Source)
- ✅ **LastPass** (Free tier)
- ✅ **KeePass** (Offline)

**Premium:**
- 💎 **1Password**
- 💎 **Dashlane**
- 💎 **NordPass**

### ไม่แนะนำ:
- ❌ บันทึกใน Notepad/Text file
- ❌ เขียนไว้บน Post-it
- ❌ ส่งใน Email/Chat
- ❌ เก็บใน Browser (ถ้าไม่มี Master Password)

---

## 🚨 ถ้าลืมรหัสผ่าน

### วิธีแก้:

**ไม่มีระบบ Reset Password อัตโนมัติ ต้องทำด้วยตนเอง:**

1. **ใช้ Railway CLI**
   ```bash
   railway shell
   python change_admin_password.py
   ```

2. **หรือสร้าง Admin ใหม่**
   - ตามวิธีที่ 3 ด้านบน

3. **หรือ Restore จาก Backup**
   - ถ้ามี database backup

---

## 🔐 Security Checklist

หลังจาก Deploy แล้ว ต้องทำ:

- [ ] ✅ เปลี่ยนรหัสผ่าน admin ทันที
- [ ] ✅ ใช้รหัสผ่านที่แข็งแรง (12+ ตัวอักษร)
- [ ] ✅ เก็บรหัสผ่านใน Password Manager
- [ ] ✅ ลบ /init-admin route (ถ้ามี)
- [ ] ✅ ลบ /reset-admin-password route (ถ้ามี)
- [ ] ✅ เปิดใช้ HTTPS (Railway ทำให้อัตโนมัติ)
- [ ] ✅ ตั้งค่า Environment Variables
- [ ] ✅ Backup database
- [ ] ✅ ตรวจสอบ logs เป็นประจำ

---

## 📞 ติดต่อ

ถ้ามีปัญหาหรือคำถาม:
1. ดู Logs ใน Railway Dashboard
2. ตรวจสอบ GitHub repository
3. ลอง redeploy
4. อ่าน `SECURITY_GUIDE.md` สำหรับรายละเอียดเพิ่มเติม

**หากพบปัญหาด้านความปลอดภัย:**
- แจ้งทีม IT Security ทันที
- ส่ง email: security@g-able.com

---

**Happy Deploying! 🚂🎉**

**Project Scoring System** - Railway Deployment  
October 2025

