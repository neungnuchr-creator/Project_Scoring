# 🔐 วิธีเปลี่ยนรหัสผ่าน Admin - Quick Reference

## ⚡ Quick Start

### 🖥️ **Local (ง่ายที่สุด)**
```bash
python change_admin_password.py
```

### 🚂 **Railway**
```bash
railway shell
python change_admin_password.py
```

### 🐳 **Docker**
```bash
docker exec -it project-scoring python change_admin_password.py
```

---

## 📋 เลือกวิธีตามสถานการณ์

| สถานการณ์ | วิธีที่แนะนำ | ขั้นตอน |
|-----------|-------------|---------|
| 🖥️ รัน Local | Script | `python change_admin_password.py` |
| 🚂 Deploy บน Railway | Railway CLI | `railway shell` → `python change_admin_password.py` |
| 🐳 รัน Docker | Docker exec | `docker exec -it project-scoring python change_admin_password.py` |
| 🆘 ลืมรหัสผ่าน | Reset | ใช้วิธีเดียวกับข้างบน |
| ⚙️ Production | Railway CLI + Strong Password | อ่านคู่มือเต็ม |

---

## 📖 คู่มือแต่ละแพลตฟอร์ม

### 🖥️ **Local Development**

**ขั้นตอน:**
1. เปิด Terminal/PowerShell
2. รันคำสั่ง:
   ```bash
   cd C:\Users\User\project-scoring-system
   python change_admin_password.py
   ```
3. กรอกรหัสผ่านใหม่
4. ยืนยันรหัสผ่าน
5. ✅ เสร็จสิ้น!

**Video Guide:** (ถ้ามี)

---

### 🚂 **Railway Deployment**

#### วิธีที่ 1: ใช้ Railway CLI (แนะนำ)

**ติดตั้ง CLI:**
```bash
# Windows
iwr https://railway.app/install.ps1 -useb | iex

# Mac/Linux
sh -c "$(curl -sSL https://railway.app/install.sh)"
```

**เปลี่ยนรหัสผ่าน:**
```bash
railway login
cd project-scoring-system
railway link
railway shell
python change_admin_password.py
```

#### วิธีที่ 2: ใช้ Python Script

```bash
railway shell
python
```

```python
from werkzeug.security import generate_password_hash
import sqlite3

new_password = "YOUR_NEW_STRONG_PASSWORD"
hashed = generate_password_hash(new_password)

conn = sqlite3.connect('project_scoring.db')
cursor = conn.cursor()
cursor.execute("UPDATE users SET password = ? WHERE username = 'admin'", (hashed,))
conn.commit()
conn.close()

print("✅ Password changed!")
exit()
```

📖 **คู่มือเต็ม:** [RAILWAY_DEPLOY_GUIDE.md](RAILWAY_DEPLOY_GUIDE.md#การเปลี่ยนรหัสผ่าน-admin)

---

### 🐳 **Docker Container**

#### วิธีที่ 1: เข้าไปใน Container

```bash
docker ps  # ดู container name
docker exec -it project-scoring /bin/bash
python change_admin_password.py
exit
```

#### วิธีที่ 2: รัน Command โดยตรง

```bash
docker exec -it project-scoring python3 << EOF
from werkzeug.security import generate_password_hash
import sqlite3

new_password = "YOUR_NEW_STRONG_PASSWORD"
hashed = generate_password_hash(new_password)

conn = sqlite3.connect('project_scoring.db')
cursor = conn.cursor()
cursor.execute("UPDATE users SET password = ? WHERE username = 'admin'", (hashed,))
conn.commit()
conn.close()

print("✅ Password changed!")
EOF
```

#### วิธีที่ 3: ใช้ docker-compose

```bash
docker-compose exec project-scoring python change_admin_password.py
```

📖 **คู่มือเต็ม:** [DOCKER_GUIDE.md](DOCKER_GUIDE.md#การเปลี่ยนรหัสผ่าน-admin)

---

## 💡 Tips สำหรับรหัสผ่านที่แข็งแรง

### ✅ รหัสผ่านที่ดี:
- ✅ ยาวอย่างน้อย 12 ตัวอักษร
- ✅ ผสมตัวพิมพ์ใหญ่-เล็ก (A-z)
- ✅ มีตัวเลข (0-9)
- ✅ มีสัญลักษณ์พิเศษ (!@#$%^&*)
- ✅ ไม่ใช่คำในพจนานุกรม
- ✅ ไม่ใช้ข้อมูลส่วนตัว

### ❌ รหัสผ่านที่ไม่ดี:
- ❌ admin123
- ❌ password
- ❌ 12345678
- ❌ company-name
- ❌ วันเกิด, ชื่อ

### 🎯 ตัวอย่างรหัสผ่านที่ดี:
```
MySecure@Pass2025!
G-able#Proj2025Strong
Admin$Railway!2025Secure
P@ssw0rd!Scoring#2025
Th1s!sMyStr0ng#Pass
```

### 🔧 Generate รหัสผ่านแบบสุ่ม:

**Python:**
```python
import secrets
import string

def generate_password(length=16):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(chars) for _ in range(length))

print(generate_password())
```

**Online Tools:**
- https://bitwarden.com/password-generator/
- https://1password.com/password-generator/

---

## 🔒 ตรวจสอบว่าเปลี่ยนสำเร็จ

### Checklist:

1. **Logout** จากระบบ
2. **ลอง Login** ด้วยรหัสผ่านเก่า
   - ❌ Login ไม่ได้ = ✅ สำเร็จ!
   - ✅ Login ได้ = ⚠️ ยังไม่เปลี่ยน
3. **Login** ด้วยรหัสผ่านใหม่
   - ✅ Login ได้ = 🎉 สำเร็จ!

---

## 🚨 Troubleshooting

### ปัญหา: "Permission Denied"

**วิธีแก้:**
```bash
# ใช้ sudo (Linux/Mac)
sudo python change_admin_password.py

# หรือรันด้วย admin privileges (Windows)
# คลิกขวา → Run as Administrator
```

### ปัญหา: "Database is locked"

**วิธีแก้:**
```bash
# ปิด Flask app ก่อน
# Windows:
taskkill /F /IM python.exe

# Linux/Mac:
pkill python

# แล้วรัน script ใหม่
python change_admin_password.py
```

### ปัญหา: "Module not found: werkzeug"

**วิธีแก้:**
```bash
pip install werkzeug
# หรือ
pip install -r requirements.txt
```

### ปัญหา: "SQLite3.OperationalError: no such table: users"

**วิธีแก้:**
```bash
# สร้าง database ใหม่
python clear_database.py
# พิมพ์: yes
```

### ปัญหา: ลืมรหัสผ่าน

**วิธีแก้:**
- ใช้ script นี้เพื่อตั้งรหัสผ่านใหม่
- หรือ reset database ทั้งหมด

---

## 📝 เก็บรหัสผ่านให้ปลอดภัย

### แนะนำ Password Managers:

**ฟรี:**
- 🔐 **Bitwarden** (Open Source, sync ได้)
- 🔐 **LastPass Free** (basic features)
- 🔐 **KeePass** (offline, secure)

**Premium:**
- 💎 **1Password** ($2.99/month)
- 💎 **Dashlane** (feature-rich)
- 💎 **NordPass** (by NordVPN)

### ไม่แนะนำ:
- ❌ Notepad/Text file
- ❌ Post-it notes
- ❌ Email/Chat
- ❌ Browser saved passwords (ถ้าไม่มี master password)
- ❌ Excel spreadsheet

---

## 🔐 Security Best Practices

### ควรทำ:
- ✅ เปลี่ยนรหัสผ่าน default ทันที
- ✅ ใช้รหัสผ่านแข็งแรง (12+ ตัวอักษร)
- ✅ ใช้ Password Manager
- ✅ เปลี่ยนรหัสผ่านเป็นประจำ (3-6 เดือน)
- ✅ ไม่ใช้รหัสผ่านซ้ำกับที่อื่น
- ✅ เปิด 2FA (ถ้ามี)

### ไม่ควรทำ:
- ❌ แชร์รหัสผ่านกับใคร
- ❌ เขียนรหัสผ่านไว้
- ❌ ใช้รหัสผ่านง่ายๆ
- ❌ ส่งรหัสผ่านทาง email/chat
- ❌ ใช้ WiFi สาธารณะตอน login

---

## 📞 ขอความช่วยเหลือ

### มีปัญหา?

1. **อ่านคู่มือเพิ่มเติม:**
   - [SECURITY_GUIDE.md](SECURITY_GUIDE.md)
   - [RAILWAY_DEPLOY_GUIDE.md](RAILWAY_DEPLOY_GUIDE.md)
   - [DOCKER_GUIDE.md](DOCKER_GUIDE.md)

2. **ติดต่อ IT Support:**
   - Email: it-support@g-able.com
   - Teams: IT Support Channel

3. **ปัญหาด้านความปลอดภัย:**
   - Email: security@g-able.com
   - ⚠️ แจ้งทันที!

---

## 📚 เอกสารเพิ่มเติม

| เอกสาร | เนื้อหา |
|--------|---------|
| [SECURITY_GUIDE.md](SECURITY_GUIDE.md) | คู่มือความปลอดภัยฉบับเต็ม |
| [RAILWAY_DEPLOY_GUIDE.md](RAILWAY_DEPLOY_GUIDE.md) | Deploy บน Railway |
| [DOCKER_GUIDE.md](DOCKER_GUIDE.md) | รัน Docker |
| [ADMIN_CREDENTIALS.txt](ADMIN_CREDENTIALS.txt) | ข้อมูล login (confidential) |

---

**อัพเดทล่าสุด:** October 2025  
**Version:** 1.0  
**ผู้จัดทำ:** IT Security Team

