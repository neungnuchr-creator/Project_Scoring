# 🚂 Railway Quick Start Guide

## 🚀 Deploy ใน 5 นาที!

### 1️⃣ Push ไป GitHub
```bash
git add .
git commit -m "Add Railway config"
git push origin main
```

### 2️⃣ Deploy บน Railway
1. ไปที่: https://railway.app
2. Login ด้วย GitHub
3. **New Project** → **Deploy from GitHub repo**
4. เลือก: `project-scoring-system`
5. กด **Deploy Now**

### 3️⃣ ตั้งค่า Environment Variables
ใน Railway Dashboard → **Variables** tab:

```
SECRET_KEY = your-super-secret-random-key-here-change-this
DATABASE_PATH = project_scoring.db
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4️⃣ Generate Domain
**Settings** tab → **Domains** → **Generate Domain**

คุณจะได้ URL: `https://your-app.up.railway.app`

### 5️⃣ สร้าง Admin User

#### วิธีที่ 1: ใช้ /init-admin route (ง่ายที่สุด)

**A. แก้ไข app.py เพิ่มบรรทัดนี้:**
```python
# ด้านบนสุดของไฟล์ (หลัง import อื่นๆ)
from init_admin_railway import init_admin
```

**B. Push และ Deploy:**
```bash
git add app.py
git commit -m "Add init-admin route"
git push origin main
```

**C. เข้าไปที่:**
```
https://your-app.up.railway.app/init-admin
```

**D. กดปุ่ม "Create Admin User"**

**E. Login:**
- Username: `admin`
- Password: `admin123`

**F. ⚠️ สำคัญ - ลบ route ทิ้ง:**
```python
# ลบบรรทัดนี้ออกจาก app.py
# from init_admin_railway import init_admin
```

Push อีกครั้ง:
```bash
git add app.py
git commit -m "Remove init-admin route"
git push origin main
```

---

#### วิธีที่ 2: ใช้ Railway CLI

**A. ติดตั้ง CLI:**
```bash
# Windows PowerShell
iwr https://railway.app/install.ps1 -useb | iex
```

**B. Login และ Link:**
```bash
railway login
cd C:\Users\User\project-scoring-system
railway link
```

**C. Run Command:**
```bash
railway run python clear_database.py
# พิมพ์: yes
```

---

## ✅ Checklist

- [ ] Push code ไป GitHub
- [ ] Deploy บน Railway
- [ ] ตั้งค่า SECRET_KEY
- [ ] Generate Domain
- [ ] สร้าง Admin user
- [ ] ทดสอบ Login
- [ ] ลบ /init-admin route (ถ้าใช้)
- [ ] เปลี่ยน admin password

---

## 🔑 Default Credentials

**Admin:**
- Username: `admin`
- Password: `admin123`

**⚠️ เปลี่ยน password ทันทีหลัง login!**

---

## 📋 ไฟล์ที่จำเป็นสำหรับ Railway

✅ **nixpacks.toml** - แก้ปัญหา SQLite  
✅ **railway.json** - Railway config  
✅ **Procfile** - Start command  
✅ **runtime.txt** - Python version  
✅ **requirements.txt** - Dependencies  
✅ **.env.example** - Environment variables template  

---

## 🆘 มีปัญหา?

### Build Failed?
ดู Logs ใน Railway Dashboard → Deployments → View Logs

### Worker Failed to Boot?
ตรวจสอบว่ามีไฟล์ `nixpacks.toml`:
```toml
[phases.setup]
nixPkgs = ['python311', 'sqlite']
```

### Cannot Login?
สร้าง admin user ใหม่ที่ `/init-admin`

---

## 📚 คู่มือเพิ่มเติม

- **RAILWAY_DEPLOY_GUIDE.md** - คู่มือฉบับเต็ม
- **README_DOCKER.md** - สำหรับ Docker
- **DOCKER_GUIDE.md** - Docker ฉบับละเอียด

---

**ใช้เวลาทั้งหมดประมาณ 5-10 นาที! 🎉**

Questions? Check logs or deploy guide!

