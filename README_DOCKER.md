# 🚀 Project Scoring System - Docker Version

## สำหรับเพื่อนที่ได้รับไฟล์นี้

ระบบนี้ใช้สำหรับคำนวณคะแนนโครงการและจัดการข้อมูลโครงการของทีม PMO

---

## ⚡ Quick Start (3 ขั้นตอน)

### 1️⃣ ติดตั้ง Docker Desktop
- ดาวน์โหลด: https://www.docker.com/products/docker-desktop/
- ติดตั้งและเปิดโปรแกรม Docker Desktop

### 2️⃣ รัน Docker Container
เปิด Terminal/PowerShell ในโฟลเดอร์นี้ แล้วพิมพ์:
```bash
docker-compose up
```

รอสักครู่จนเห็นข้อความ:
```
* Running on http://0.0.0.0:5000
```

### 3️⃣ เปิดเว็บเบราว์เซอร์
```
http://localhost:5000
```

---

## 🔑 ข้อมูล Login

### Admin (ดูข้อมูลทั้งหมด):
- **Username:** `admin`
- **Password:** `admin123`

### Users ทดสอบ:
- **User 1:** `user1` / `user123` (สมชาย ใจดี - EMP001)
- **User 2:** `user2` / `user123` (สมหญิง รักสวย - EMP002)
- **User 3:** `user3` / `user123` (วิชัย มั่นคง - EMP003)

---

## 🎯 ฟีเจอร์หลัก

### 👤 User Dashboard:
- ✅ เพิ่ม/แก้ไข/ลบโครงการ
- ✅ คำนวณคะแนนโครงการอัตโนมัติ
- ✅ ดูสถิติส่วนตัว
- ✅ **Export PDF** พร้อม Summary

### 👨‍💼 Admin Dashboard:
- ✅ ดูโครงการทั้งหมดของทุกคน
- ✅ ค้นหาและกรองข้อมูล
- ✅ ดูสถิติภาพรวม
- ✅ **Export PDF** (ทั้งหมด หรือ เลือกรายบุคคล)
- ✅ Auto-refresh ทุก 30 วินาที

---

## 📊 การคำนวณคะแนน

### สูตร:
```
Score = B2 × ((C2 × (D2/E2)) × G2/100) + F2
```

โดยที่:
- **B2** = Difficulty Type of Project (1.0 - 2.0)
- **C2** = Difficulty Customer (3 - 5)
- **D2** = Baseline PM Effort (manday)
- **E2** = Duration (ปี)
- **G2** = Progress (%)
- **F2** = Challenge Topup (0, 8, 15)

---

## 🛑 หยุดการทำงาน

### วิธีที่ 1: กด Ctrl+C
ใน Terminal ที่รัน `docker-compose up`

### วิธีที่ 2: ใช้คำสั่ง
```bash
docker-compose down
```

---

## 🔄 รันใหม่

```bash
# ถ้าไม่ได้แก้ code
docker-compose up

# ถ้าแก้ code แล้ว
docker-compose up --build
```

---

## 📤 Export PDF

### User:
1. Login → Dashboard
2. กดปุ่ม **"Export PDF"** (สีแดง)
3. ไฟล์จะ Download: `Project_Report_[รหัสพนักงาน]_[วันที่].pdf`

### Admin:
1. Login → Admin Dashboard
2. **เลือกจาก Dropdown:**
   - "ทั้งหมด (ภาพรวม)" → รายงานรวมทุกคน
   - เลือกชื่อพนักงาน → รายงานเฉพาะคนนั้น
3. กดปุ่ม **"Export PDF"**
4. ไฟล์จะ Download

### เนื้อหา PDF:
- 📋 Summary คะแนนรวม
- 📊 ตารางรายละเอียดโครงการ
- 📅 วันที่สร้างรายงาน

---

## 💾 ข้อมูลจะหายไหม?

### ไม่หาย - ถ้าใช้คำสั่ง:
```bash
docker-compose down
docker-compose up
```

### หาย - ถ้าใช้คำสั่ง:
```bash
docker-compose down -v  # ลบ volume ด้วย
```

---

## 🆘 ติดปัญหา?

### ตรวจสอบ:
1. ✅ Docker Desktop เปิดอยู่หรือไม่?
2. ✅ Port 5000 ว่างหรือไม่?
3. ✅ Internet connection (สำหรับ pull images)

### ดู Logs:
```bash
docker-compose logs
```

### Restart:
```bash
docker-compose restart
```

---

## 📞 ติดต่อ

ถ้ามีปัญหาหรือข้อสงสัย กรุณาติดต่อผู้พัฒนา

---

**Happy Testing! 🎉**

**Project Scoring System** - PMO Team  
October 2025

