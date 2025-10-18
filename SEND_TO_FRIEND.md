# 📦 วิธีส่ง Project Scoring System ให้เพื่อนทดสอบ

## 🎯 เป้าหมาย
ส่งระบบให้เพื่อนทดสอบได้โดยไม่ต้องติดตั้ง Python หรือ dependencies อื่นๆ

---

## 📋 สิ่งที่ต้อง SEND ให้เพื่อน

### วิธีที่ 1: ส่ง Docker Image (แนะนำ)

#### ขั้นตอนการเตรียม:

**1. ล้าง Database (ถ้าต้องการ):**
```bash
python clear_database.py
```
พิมพ์: `yes`

**2. Build และ Export Docker Image:**
```bash
# วิธีที่ 1: ใช้ Script (ง่ายที่สุด)
.\export_docker.bat

# วิธีที่ 2: ใช้คำสั่ง
docker build -t project-scoring-system .
docker save -o project-scoring-system.tar project-scoring-system
```

**3. ไฟล์ที่ต้องส่ง:**
- ✅ `project-scoring-system.tar` (ประมาณ 200-300 MB)
- ✅ `README_DOCKER.md` (คู่มือสำหรับเพื่อน)

---

### วิธีที่ 2: ส่ง Source Code + Docker files

#### ไฟล์ที่ต้องส่ง:
- ✅ `app.py`
- ✅ `templates/` (folder)
- ✅ `static/` (folder)
- ✅ `requirements.txt`
- ✅ `Dockerfile`
- ✅ `docker-compose.yml`
- ✅ `.dockerignore`
- ✅ `README_DOCKER.md`

#### สร้าง ZIP:
```bash
# ใน PowerShell
$files = @(
    "app.py",
    "templates",
    "static", 
    "requirements.txt",
    "Dockerfile",
    "docker-compose.yml",
    ".dockerignore",
    "README_DOCKER.md"
)
Compress-Archive -Path $files -DestinationPath project-scoring-docker.zip -Force
```

**ส่ง:** `project-scoring-docker.zip` (ประมาณ 50-100 KB)

---

## 📨 วิธีที่เพื่อนใช้งาน

### ถ้าได้รับไฟล์ .tar:

```bash
# 1. Load Docker image
docker load -i project-scoring-system.tar

# 2. Run container
docker run -d -p 5000:5000 --name project-scoring project-scoring-system

# 3. เปิด browser
http://localhost:5000

# 4. Login
admin / admin123
```

### ถ้าได้รับไฟล์ ZIP:

```bash
# 1. Extract ZIP

# 2. เปิด Terminal ในโฟลเดอร์

# 3. Run
docker-compose up

# 4. เปิด browser
http://localhost:5000

# 5. Login
admin / admin123
```

---

## 🔑 ข้อมูล Login สำหรับ Demo

### Accounts ที่มี:
| Username | Password | ชื่อ             | รหัส     | Role     |
|----------|----------|------------------|----------|----------|
| admin    | admin123 | Admin System     | ADMIN001 | admin    |
| user1    | user123  | สมชาย ใจดี       | EMP001   | employee |
| user2    | user123  | สมหญิง รักสวย    | EMP002   | employee |
| user3    | user123  | วิชัย มั่นคง     | EMP003   | employee |

---

## 📊 ขนาดไฟล์โดยประมาณ

| วิธี                    | ขนาด          | ความเร็ว Upload |
|------------------------|---------------|-----------------|
| Docker Image (.tar)    | 200-300 MB    | ช้า             |
| Source Code (ZIP)      | 50-100 KB     | เร็วมาก         |
| Source + docs (ZIP)    | 100-200 KB    | เร็ว            |

---

## 💡 Tips

### เลือกวิธีส่ง:
- 📦 **ส่ง .tar** → ถ้าเพื่อนมี internet ช้า (ติดตั้งครั้งเดียว)
- 📁 **ส่ง ZIP** → ถ้าเพื่อนมี internet เร็ว (ไฟล์เล็ก)

### สำหรับคุณ (ผู้พัฒนา):
- ✅ Code เดิมไม่กระทบ
- ✅ Database แยกกัน (Docker ใช้ database ใหม่)
- ✅ Port แยกกัน (ถ้าตั้งค่า)
- ✅ สามารถรันพร้อมกันได้ (local + Docker)

---

## 🚀 Commands สำคัญ

### Build Docker:
```bash
.\build_docker.bat
```

### Export Docker Image:
```bash
.\export_docker.bat
```

### ล้าง Database:
```bash
python clear_database.py
```

### Run Docker:
```bash
docker-compose up
```

### Stop Docker:
```bash
docker-compose down
```

---

## ✅ Checklist ก่อนส่ง

- [ ] Build Docker image สำเร็จ
- [ ] ทดสอบรัน container แล้ว
- [ ] ทดสอบ login ได้
- [ ] ทดสอบเพิ่มโครงการได้
- [ ] ทดสอบ Export PDF ได้
- [ ] ส่งไฟล์และคู่มือให้เพื่อน

---

**Good Luck! 🎉**

