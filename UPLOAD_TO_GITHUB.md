# 📦 วิธีอัปโหลด Code ไปยัง GitHub

## 🎯 GitHub Repository ของคุณ
https://github.com/neungnuchr-creator/Project_Scoring/tree/Project_score

---

## ⚡ วิธีที่ 1: ใช้ Git Command Line (แนะนำ)

### 1️⃣ ติดตั้ง Git for Windows
1. ดาวน์โหลดจาก: https://git-scm.com/download/win
2. ติดตั้งด้วยค่า default ทั้งหมด
3. เปิด PowerShell หรือ Command Prompt ใหม่

### 2️⃣ ตั้งค่า Git (ครั้งแรกเท่านั้น)
```bash
git config --global user.name "neungnuchr-creator"
git config --global user.email "your-email@example.com"
```

### 3️⃣ เข้าไปยังโฟลเดอร์โปรเจค
```bash
cd C:\Users\User\project-scoring-system
```

### 4️⃣ ตรวจสอบว่ามี .git หรือไม่
```bash
# ถ้ายังไม่มี ให้รันคำสั่งนี้
git init
```

### 5️⃣ เชื่อมต่อกับ GitHub Repository
```bash
git remote add origin https://github.com/neungnuchr-creator/Project_Scoring.git
```

### 6️⃣ เปลี่ยน branch เป็น Project_score
```bash
git checkout -b Project_score
```

### 7️⃣ เพิ่มไฟล์ทั้งหมด (ยกเว้นไฟล์ใน .gitignore)
```bash
git add .
```

### 8️⃣ Commit การเปลี่ยนแปลง
```bash
git commit -m "Update Project Scoring System - Complete version with modern UI"
```

### 9️⃣ Push ขึ้น GitHub
```bash
git push -u origin Project_score
```

**หมายเหตุ:** GitHub อาจขอ username และ password (หรือ Personal Access Token)

---

## 🌐 วิธีที่ 2: ใช้ GitHub Desktop (ง่ายที่สุด)

### 1️⃣ ติดตั้ง GitHub Desktop
- ดาวน์โหลดจาก: https://desktop.github.com/
- ติดตั้งและเข้าสู่ระบบด้วย GitHub account

### 2️⃣ เพิ่ม Repository
1. เปิด GitHub Desktop
2. File → Add Local Repository
3. เลือกโฟลเดอร์: `C:\Users\User\project-scoring-system`
4. ถ้าแจ้งว่ายังไม่ใช่ git repository ให้กด "Create a repository"

### 3️⃣ เชื่อมต่อกับ GitHub
1. Repository → Repository Settings
2. Remote → ใส่ URL: `https://github.com/neungnuchr-creator/Project_Scoring.git`
3. เลือก branch: `Project_score`

### 4️⃣ Commit และ Push
1. เลือกไฟล์ทั้งหมดที่ต้องการ
2. กรอก commit message: "Update Project Scoring System"
3. กด "Commit to Project_score"
4. กด "Push origin"

---

## 📤 วิธีที่ 3: อัปโหลดผ่าน Web (ถ้า Git ไม่ทำงาน)

### 1️⃣ สร้างไฟล์ ZIP
1. คลิกขวาที่โฟลเดอร์ `project-scoring-system`
2. Send to → Compressed (zipped) folder

### 2️⃣ ลบไฟล์ที่ไม่จำเป็นออก
- `venv/` (virtual environment)
- `project_scoring.db` (database)
- `__pycache__/` (cache)

### 3️⃣ อัปโหลดผ่าน GitHub Web
1. ไปที่: https://github.com/neungnuchr-creator/Project_Scoring/tree/Project_score
2. กด "Add file" → "Upload files"
3. ลากไฟล์ทั้งหมดมาวาง (หรือแตกไฟล์ ZIP ก่อน)
4. กรอก commit message
5. กด "Commit changes"

---

## 📝 ไฟล์ที่ควรอัปโหลด

### ✅ อัปโหลดไฟล์เหล่านี้:
- `app.py` ⭐ (Backend หลัก)
- `templates/` ⭐ (HTML files)
- `static/` (CSS, JS, images)
- `requirements.txt` ⭐ (Python dependencies)
- `.gitignore` (ไฟล์ที่ไม่ต้องอัปโหลด)
- `README.md` (คำอธิบายโปรเจค)
- `QUICK_START.md`
- `DEPLOYMENT_GUIDE.md`
- `START.bat`
- เอกสารต่างๆ (.md files)

### ❌ ไม่ต้องอัปโหลดไฟล์เหล่านี้:
- `venv/` (virtual environment - ใหญ่มาก)
- `project_scoring.db` (database - มีข้อมูลส่วนตัว)
- `__pycache__/` (Python cache)
- `*.pyc` (compiled Python)
- `.env` (environment variables)

---

## 🔐 การใช้ Personal Access Token (ถ้า Git ขอ password)

ถ้า Git ขอ password แต่คุณใช้ไม่ได้ ให้สร้าง Personal Access Token:

1. ไปที่: https://github.com/settings/tokens
2. Generate new token (classic)
3. เลือก scopes: `repo` (ทั้งหมด)
4. Generate token
5. **คัดลอกและเก็บไว้** (จะเห็นได้ครั้งเดียว)
6. ใช้ token นี้แทน password เมื่อ Git ถาม

---

## 🎉 หลังจาก Push แล้ว

### ตรวจสอบที่:
https://github.com/neungnuchr-creator/Project_Scoring/tree/Project_score

คุณจะเห็น:
- 📁 Code ทั้งหมด
- 📝 README.md แสดงอัตโนมัติ
- 🕐 ประวัติ Commits
- 📊 Project structure

---

## 💡 Tips

1. **ใช้ .gitignore ที่มีอยู่แล้ว** - จะช่วยไม่ให้อัปโหลดไฟล์ที่ไม่จำเป็น
2. **Commit บ่อยๆ** - แยก commit ตามฟีเจอร์
3. **เขียน commit message ที่ชัดเจน**
4. **ทดสอบก่อน commit** - ให้แน่ใจว่าโค้ดทำงานได้

---

## 🆘 มีปัญหา?

### Git ขอ username/password แต่ใช้ไม่ได้:
→ ใช้ Personal Access Token แทน (ดูด้านบน)

### Push ไม่ได้เพราะมีไฟล์ขนาดใหญ่:
→ ตรวจสอบว่าได้ลบ `venv/` และ `*.db` หรือยัง

### Conflict เกิดขึ้น:
→ Pull ก่อน: `git pull origin Project_score`
→ แก้ไข conflict แล้ว commit ใหม่

---

**สร้างโดย:** Project Scoring System Team  
**วันที่:** October 2025  
**Repository:** https://github.com/neungnuchr-creator/Project_Scoring

