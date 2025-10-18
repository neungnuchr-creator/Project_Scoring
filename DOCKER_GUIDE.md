# 🐳 Docker Deployment Guide - Project Scoring System

## 📦 ส่งให้เพื่อนทดสอบ

คู่มือนี้อธิบายวิธีการรัน Project Scoring System ด้วย Docker

---

## 🎯 ข้อดีของการใช้ Docker

- ✅ **ไม่ต้องติดตั้ง Python** - รันได้เลย
- ✅ **ไม่ต้อง setup environment** - Docker จัดการให้
- ✅ **Database สะอาด** - เริ่มใหม่ทุกครั้ง
- ✅ **รันได้หลาย OS** - Windows, Mac, Linux
- ✅ **แยกจาก code เดิม** - ไม่กระทบการพัฒนา

---

## 📋 ข้อกำหนดเบื้องต้น

### ติดตั้ง Docker Desktop:

**Windows:**
- ดาวน์โหลด: https://www.docker.com/products/docker-desktop/
- ติดตั้งและ restart เครื่อง
- เปิด Docker Desktop

**Mac:**
- ดาวน์โหลด: https://www.docker.com/products/docker-desktop/
- ติดตั้งและเปิด Docker Desktop

**Linux:**
```bash
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo systemctl start docker
```

---

## 🚀 วิธีใช้งาน

### วิธีที่ 1: ใช้ docker-compose (แนะนำ - ง่ายที่สุด)

#### 1. เปิด Terminal/PowerShell ในโฟลเดอร์โปรเจค
```bash
cd C:\Users\User\project-scoring-system
```

#### 2. Build และรัน
```bash
docker-compose up --build
```

#### 3. เปิดเว็บเบราว์เซอร์
```
http://localhost:5000
```

#### 4. Login ด้วย:
- **Admin**: `admin` / `admin123`
- **User1**: `user1` / `user123`
- **User2**: `user2` / `user123`
- **User3**: `user3` / `user123`

#### 5. หยุดการทำงาน
กด `Ctrl + C` ใน terminal หรือ:
```bash
docker-compose down
```

---

### วิธีที่ 2: ใช้ Docker โดยตรง

#### 1. Build Docker image
```bash
docker build -t project-scoring-system .
```

#### 2. Run container
```bash
docker run -d -p 5000:5000 --name project-scoring project-scoring-system
```

#### 3. เปิดเว็บเบราว์เซอร์
```
http://localhost:5000
```

#### 4. ดู logs (ถ้าต้องการ)
```bash
docker logs -f project-scoring
```

#### 5. หยุดและลบ container
```bash
docker stop project-scoring
docker rm project-scoring
```

---

## 🗄️ การจัดการ Database

### ล้าง Database และสร้างใหม่

**ก่อน Build Docker:**
```bash
python clear_database.py
```

พิมพ์: `yes` เพื่อยืนยัน

**หลัง Build แล้ว (Clear database ใน Docker):**
```bash
# หยุด container
docker-compose down

# ลบ volume (database)
docker volume rm project-scoring-system_project-data

# รันใหม่
docker-compose up
```

---

## 📤 ส่งให้เพื่อนทดสอบ

### วิธีที่ 1: ส่ง Docker Image (แนะนำ)

#### A. Export Docker Image เป็นไฟล์
```bash
# Build image
docker build -t project-scoring-system .

# Export เป็นไฟล์ .tar
docker save -o project-scoring-system.tar project-scoring-system

# ไฟล์จะได้: project-scoring-system.tar (ประมาณ 200-300 MB)
```

#### B. ส่งไฟล์ให้เพื่อน
- ส่งไฟล์ `project-scoring-system.tar`
- ส่งคู่มือนี้ (`DOCKER_GUIDE.md`)

#### C. เพื่อน Load และรัน
```bash
# Load image
docker load -i project-scoring-system.tar

# Run container
docker run -d -p 5000:5000 --name project-scoring project-scoring-system

# เปิด browser: http://localhost:5000
```

---

### วิธีที่ 2: ส่ง Source Code

#### A. สร้าง ZIP file
```bash
# ใน PowerShell
Compress-Archive -Path * -DestinationPath project-scoring-system.zip
```

#### B. ส่งให้เพื่อน:
- `project-scoring-system.zip`

#### C. เพื่อน Extract และรัน:
```bash
# Extract ZIP
# เปิด Terminal ในโฟลเดอร์

# รัน Docker
docker-compose up --build

# เปิด browser: http://localhost:5000
```

---

### วิธีที่ 3: ใช้ Docker Hub (ถ้ามี account)

#### A. Push to Docker Hub
```bash
# Login
docker login

# Tag image
docker tag project-scoring-system your-username/project-scoring-system:latest

# Push
docker push your-username/project-scoring-system:latest
```

#### B. เพื่อน Pull และรัน
```bash
# Pull image
docker pull your-username/project-scoring-system:latest

# Run
docker run -d -p 5000:5000 your-username/project-scoring-system:latest
```

---

## 🔧 คำสั่ง Docker ที่มีประโยชน์

### ดูสถานะ Containers:
```bash
docker ps -a
```

### ดู Logs:
```bash
docker logs project-scoring
docker logs -f project-scoring  # follow mode
```

### เข้าไปใน Container:
```bash
docker exec -it project-scoring /bin/bash
```

### ลบทั้งหมดและเริ่มใหม่:
```bash
docker-compose down -v
docker-compose up --build
```

### ลบ Images ที่ไม่ใช้:
```bash
docker image prune -a
```

### ดูขนาด Images:
```bash
docker images
```

---

## 🔐 การเปลี่ยนรหัสผ่าน Admin

### ⚠️ สำคัญมาก: เปลี่ยนรหัสผ่าน Default ทันที!

---

### วิธีที่ 1: เข้าไปใน Docker Container (แนะนำ)

**ขั้นตอน:**

1. **ตรวจสอบ Container ที่รันอยู่**
   ```bash
   docker ps
   ```

2. **เข้าไปใน Container**
   ```bash
   docker exec -it project-scoring /bin/bash
   ```

3. **รัน Script เปลี่ยนรหัสผ่าน**
   ```bash
   python change_admin_password.py
   ```

4. **ทำตามขั้นตอน:**
   ```
   รหัสผ่านใหม่: ********** (กรอกรหัสผ่านใหม่)
   ยืนยันรหัสผ่าน: ********** (กรอกอีกครั้ง)
   ✅ เปลี่ยนรหัสผ่านสำเร็จ!
   ```

5. **ออกจาก Container**
   ```bash
   exit
   ```

6. **Restart Container (ถ้าจำเป็น)**
   ```bash
   docker restart project-scoring
   ```

---

### วิธีที่ 2: ใช้ docker exec โดยตรง

**ขั้นตอน:**

```bash
# รัน Python command ใน container
docker exec -it project-scoring python3 << EOF
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
EOF
```

---

### วิธีที่ 3: ใช้ docker-compose

**ขั้นตอน:**

1. **เข้าไปใน Container**
   ```bash
   docker-compose exec project-scoring /bin/bash
   ```

2. **รัน Script**
   ```bash
   python change_admin_password.py
   ```

3. **ออกและ Restart**
   ```bash
   exit
   docker-compose restart
   ```

---

### วิธีที่ 4: แก้ไขก่อน Build Docker Image

**ขั้นตอน:**

1. **รัน Script ที่เครื่อง Local**
   ```bash
   python change_admin_password.py
   ```

2. **Build Docker Image ใหม่**
   ```bash
   docker build -t project-scoring-system .
   ```

3. **Run Container**
   ```bash
   docker-compose up -d
   ```

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
G-able#Docker2025Strong
Admin$Container!2025Secure
P@ssw0rd!Scoring#2025
```

**ตัวอย่างรหัสผ่านที่ไม่ดี:**
```
❌ admin123
❌ password
❌ 12345678
❌ docker2025
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

## 🚨 ถ้าลืมรหัสผ่าน

### วิธีแก้:

**ตัวเลือกที่ 1: Reset ผ่าน Container**
```bash
docker exec -it project-scoring python change_admin_password.py
```

**ตัวเลือกที่ 2: Clear Database และสร้างใหม่**
```bash
docker exec -it project-scoring python clear_database.py
# พิมพ์: yes
```

**ตัวเลือกที่ 3: Restart Container ใหม่**
```bash
docker-compose down -v  # ลบ volume (database หาย!)
docker-compose up --build
```

---

## 🔐 Security Checklist สำหรับ Docker

หลังจากรัน Docker แล้ว ต้องทำ:

- [ ] ✅ เปลี่ยนรหัสผ่าน admin ทันที
- [ ] ✅ ใช้รหัสผ่านที่แข็งแรง (12+ ตัวอักษร)
- [ ] ✅ เก็บรหัสผ่านใน Password Manager
- [ ] ✅ ไม่แชร์ข้อมูล credentials
- [ ] ✅ Backup database volume เป็นประจำ
- [ ] ✅ อัพเดท Docker image เป็นประจำ
- [ ] ✅ ใช้ Docker secrets (ถ้ารัน production)
- [ ] ✅ จำกัดการเข้าถึง Container

---

## 📦 Backup Database ใน Docker

### วิธี Backup:

**1. Copy database ออกจาก Container:**
```bash
docker cp project-scoring:/app/project_scoring.db ./backup_$(date +%Y%m%d).db
```

**2. Backup Volume:**
```bash
docker run --rm \
  -v project-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/backup_$(date +%Y%m%d).tar.gz /data
```

### วิธี Restore:

**1. Copy database เข้า Container:**
```bash
docker cp backup_20251018.db project-scoring:/app/project_scoring.db
docker restart project-scoring
```

**2. Restore Volume:**
```bash
docker run --rm \
  -v project-data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/backup_20251018.tar.gz -C /
```

---

## 📊 ข้อมูล Demo (Database ใหม่)

### 👤 Users:
| Username | Password  | ชื่อ-นามสกุล      | รหัส    | Role     |
|----------|-----------|------------------|---------|----------|
| admin    | admin123  | Admin System     | ADMIN001| admin    |
| user1    | user123   | สมชาย ใจดี       | EMP001  | employee |
| user2    | user123   | สมหญิง รักสวย    | EMP002  | employee |
| user3    | user123   | วิชัย มั่นคง     | EMP003  | employee |

### 📁 Projects:
- Database ว่างเปล่า (ไม่มีโครงการ)
- พร้อมให้เพิ่มข้อมูลทดสอบ

---

## 🌐 การเข้าถึง

### Local:
```
http://localhost:5000
```

### ใน Network เดียวกัน:
```
http://[IP-ของคุณ]:5000

# หา IP:
# Windows: ipconfig
# Mac/Linux: ifconfig
```

---

## 🛠️ Troubleshooting

### ปัญหา: Port 5000 ถูกใช้งานอยู่แล้ว
**แก้:**
```bash
# เปลี่ยน port ใน docker-compose.yml
ports:
  - "8000:5000"  # ใช้ port 8000 แทน

# หรือ stop process ที่ใช้ port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID [PID] /F
```

### ปัญหา: Docker build ช้า
**แก้:**
- ใช้ Docker cache: ไม่ต้อง `--build` ถ้าไม่ได้แก้ไข code
- ใช้ image ที่ save ไว้แล้ว

### ปัญหา: Container ไม่ start
**แก้:**
```bash
# ดู logs
docker logs project-scoring

# Restart
docker-compose restart
```

### ปัญหา: Database หาย
**แก้:**
- Database เก็บอยู่ใน Docker volume
- ใช้ `docker-compose down` (ไม่ใช่ `down -v`)

---

## 📦 ขนาดไฟล์

| Item                        | Size       |
|-----------------------------|------------|
| Source Code (ZIP)           | ~50 KB     |
| Docker Image (.tar)         | ~200-300 MB|
| Container (running)         | ~300 MB    |

---

## 🔐 Security Notes

### สำหรับ Production:

1. **เปลี่ยน SECRET_KEY** ใน `app.py`
2. **เปลี่ยน admin password** หลัง deploy
3. **ใช้ HTTPS** (ผ่าน reverse proxy)
4. **จำกัดการเข้าถึง** ด้วย firewall

---

## 📝 ไฟล์ที่เกี่ยวข้อง

- `Dockerfile` - คำสั่งสร้าง Docker image
- `docker-compose.yml` - Configuration สำหรับรันหลาย services
- `.dockerignore` - ไฟล์ที่ไม่ต้อง copy เข้า Docker
- `clear_database.py` - Script ล้าง database
- `requirements.txt` - Python dependencies

---

## 🎉 Quick Start สำหรับเพื่อน

```bash
# 1. Extract ZIP file
# 2. เปิด Terminal ในโฟลเดอร์
# 3. รัน:
docker-compose up

# 4. เปิด browser:
http://localhost:5000

# 5. Login:
admin / admin123
```

---

## 💡 Tips

1. **ใช้ docker-compose** - ง่ายกว่า Docker commands
2. **ไม่ต้อง rebuild** - ถ้าไม่ได้แก้ code
3. **ดู logs** - ถ้ามีปัญหา
4. **ลบ volume** - ถ้าต้องการ database ใหม่
5. **Use persistent volume** - ถ้าต้องการเก็บข้อมูล

---

**สร้างโดย:** Project Scoring System Team  
**วันที่:** October 2025  
**Version:** Docker 1.0

