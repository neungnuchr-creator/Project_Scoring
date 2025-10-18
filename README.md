# 📊 ระบบจัดเก็บและคำนวณคะแนนโครงการ (Project Scoring System)

Web Application สำหรับจัดการและคำนวณคะแนนโครงการตามความยาก ความคืบหน้า และประเภทลูกค้า

## ✨ คุณสมบัติ

- **คำนวณคะแนนอัตโนมัติ** - คำนวณตามสูตรที่ซับซ้อนพร้อม Baseline PM Effort
- **จัดเก็บข้อมูลใน Local Database** - ใช้ SQLite เก็บข้อมูลในเครื่อง
- **แสดงสถิติโครงการ** - สรุปข้อมูลโครงการแบบ Real-time
- **UI สวยงามและใช้งานง่าย** - ออกแบบด้วย Modern UI/UX
- **CRUD Operations** - สร้าง แก้ไข ลบ และดูข้อมูลโครงการ
- **Responsive Design** - รองรับทั้ง Desktop และ Tablet
- **Export PDF** - สร้างรายงานพร้อม Summary
- **Role-Based Access** - แยก User และ Admin Dashboard
- **Custom Scrollbar** - Scrollbar สวยงามทุกหน้า

## 📋 โครงสร้างโปรเจกต์

```
project-scoring-system/
├── app.py                  # Flask backend API
├── templates/
│   └── index.html         # Frontend HTML + CSS + JavaScript
├── static/                # Static files (ถ้ามี)
├── project_scoring.db     # SQLite database (สร้างอัตโนมัติ)
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore file
├── Procfile              # สำหรับ deploy บน Heroku/Render
├── runtime.txt           # Python version
├── README.md             # คู่มือนี้
└── DEPLOYMENT_GUIDE.md   # คู่มือการ deploy
```

## 🚀 การติดตั้งและรันในเครื่อง (Local)

### ข้อกำหนดเบื้องต้น
- Python 3.8 หรือสูงกว่า
- pip (Python package manager)

### ขั้นตอนการติดตั้ง

1. **เปิด Command Prompt หรือ Terminal**

2. **ไปยังโฟลเดอร์โปรเจกต์**
   ```bash
   cd path/to/project-scoring-system
   ```

3. **สร้าง Virtual Environment (แนะนำ)**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **ติดตั้ง Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **รันโปรแกรม**
   ```bash
   python app.py
   ```

6. **เปิดเว็บเบราว์เซอร์**
   - ไปที่: `http://localhost:5000`
   - หรือ: `http://127.0.0.1:5000`

## 🎯 วิธีใช้งาน

### เพิ่มโครงการใหม่
1. กรอกชื่อโครงการ
2. เลือกระดับความยาก
3. ปรับความคืบหน้า (%)
4. เลือกประเภทลูกค้า
5. กรอกหมายเหตุ (ถ้ามี)
6. คลิก "คำนวณคะแนน" เพื่อดูคะแนน
7. คลิก "เพิ่มโครงการ" เพื่อบันทึก

### แก้ไขโครงการ
1. คลิกที่โครงการในตาราง
2. แก้ไขข้อมูลที่ต้องการ
3. คลิก "อัปเดต"

### ลบโครงการ
1. คลิกที่โครงการในตาราง
2. คลิก "ลบโครงการ"
3. ยืนยันการลบ

## 📊 สูตรการคำนวณคะแนน

```
คะแนน = (ความคืบหน้า ÷ 100) × น้ำหนักความยาก × น้ำหนักประเภทลูกค้า × 100
```

### น้ำหนักความยาก (Difficulty Weights)
| ระดับ | น้ำหนัก |
|-------|---------|
| ง่าย | 1.0 |
| ปานกลาง | 1.5 |
| ยาก | 2.0 |
| ยากมาก | 2.5 |

### น้ำหนักประเภทลูกค้า (Customer Type Weights)
| ประเภท | น้ำหนัก |
|--------|---------|
| ลูกค้าทั่วไป | 1.0 |
| ลูกค้าองค์กร | 1.3 |
| ลูกค้า VIP | 1.5 |
| หน่วยงานรัฐ | 1.4 |

### ตัวอย่างการคำนวณ

**โครงการ A:**
- ความยาก: ยาก (2.0)
- ความคืบหน้า: 75%
- ประเภทลูกค้า: ลูกค้า VIP (1.5)

```
คะแนน = (75 ÷ 100) × 2.0 × 1.5 × 100
      = 0.75 × 2.0 × 1.5 × 100
      = 225.00
```

## 🔧 API Endpoints

### คำนวณคะแนน
```http
POST /api/calculate
Content-Type: application/json

{
  "difficulty": "ยาก",
  "progress": 75,
  "customer_type": "ลูกค้า VIP"
}
```

### ดึงรายการโครงการทั้งหมด
```http
GET /api/projects
```

### ดึงข้อมูลโครงการตาม ID
```http
GET /api/projects/{id}
```

### เพิ่มโครงการใหม่
```http
POST /api/projects
Content-Type: application/json

{
  "project_name": "โครงการตัวอย่าง",
  "difficulty": "ยาก",
  "progress": 75,
  "customer_type": "ลูกค้า VIP",
  "notes": "หมายเหตุ"
}
```

### อัปเดตโครงการ
```http
PUT /api/projects/{id}
Content-Type: application/json

{
  "project_name": "โครงการตัวอย่าง (แก้ไข)",
  "difficulty": "ยากมาก",
  "progress": 85,
  "customer_type": "ลูกค้า VIP",
  "notes": "หมายเหตุใหม่"
}
```

### ลบโครงการ
```http
DELETE /api/projects/{id}
```

### ดึงสถิติ
```http
GET /api/statistics
```

## 🌐 การ Deploy

ดูรายละเอียดการ deploy ได้ที่ [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

### ตัวเลือกการ Deploy:
1. **Render** (ฟรี, แนะนำ)
2. **PythonAnywhere** (ฟรี)
3. **Heroku** (มีค่าใช้จ่าย)
4. **Railway** (ฟรีจำกัด)

## 🛠️ เทคโนโลยีที่ใช้

- **Backend**: Flask 3.0.0 (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: SQLite
- **Web Server**: Gunicorn (Production)

## 📝 หมายเหตุ

- Database (project_scoring.db) จะถูกสร้างอัตโนมัติเมื่อรันโปรแกรมครั้งแรก
- ไฟล์ database จะอยู่ในโฟลเดอร์เดียวกับ app.py
- ข้อมูลทั้งหมดจะถูกเก็บใน local database
- ไม่ต้องติดตั้งฐานข้อมูลเพิ่มเติม SQLite มีมากับ Python

## 🐛 แก้ไขปัญหาที่พบบ่อย

### ปัญหา: ModuleNotFoundError
```bash
# แก้ไข: ติดตั้ง dependencies ใหม่
pip install -r requirements.txt
```

### ปัญหา: Port 5000 ถูกใช้งานอยู่
```bash
# Windows: หา process ที่ใช้ port
netstat -ano | findstr :5000

# Mac/Linux: หา process ที่ใช้ port
lsof -i :5000

# แก้ไข: เปลี่ยน port ใน app.py
# แก้ไขบรรทัดสุดท้ายเป็น:
app.run(debug=False, host='0.0.0.0', port=8000)
```

### ปัญหา: Database locked
```bash
# แก้ไข: ปิดโปรแกรมที่เปิด database อยู่
# หรือลบไฟล์ project_scoring.db แล้วรันใหม่
```

## 🔐 ความปลอดภัย

### เปลี่ยนรหัสผ่าน Admin

**⚠️ สำคัญมาก:** ต้องเปลี่ยนรหัสผ่าน admin ทันทีหลัง setup!

**วิธีเปลี่ยนรหัสผ่าน:**
```bash
python change_admin_password.py
```

**ข้อมูล Login:**
- ดูในไฟล์ `ADMIN_CREDENTIALS.txt` (ไม่ถูก commit ใน Git)
- ไฟล์นี้เก็บข้อมูล credentials อย่างปลอดภัย

**คู่มือเพิ่มเติม:**
- 📖 [CHANGE_PASSWORD_GUIDE.md](CHANGE_PASSWORD_GUIDE.md) - วิธีเปลี่ยนรหัสผ่านแบบละเอียด
- 📖 [SECURITY_GUIDE.md](SECURITY_GUIDE.md) - คู่มือความปลอดภัยฉบับเต็ม

---

## 📚 เอกสารเพิ่มเติม

| คู่มือ | เนื้อหา |
|-------|---------|
| [QUICK_START.md](QUICK_START.md) | เริ่มต้นใช้งานอย่างรวดเร็ว |
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | Deploy บน Cloud |
| [RAILWAY_DEPLOY_GUIDE.md](RAILWAY_DEPLOY_GUIDE.md) | Deploy บน Railway.app |
| [DOCKER_GUIDE.md](DOCKER_GUIDE.md) | รัน Docker |
| [README_DOCKER.md](README_DOCKER.md) | Docker Quick Start |
| [SECURITY_GUIDE.md](SECURITY_GUIDE.md) | คู่มือความปลอดภัย |
| [CHANGE_PASSWORD_GUIDE.md](CHANGE_PASSWORD_GUIDE.md) | วิธีเปลี่ยนรหัสผ่าน |
| [ADMIN_CREDENTIALS.txt](ADMIN_CREDENTIALS.txt) | ข้อมูล Login (confidential) |

---

## 📞 ติดต่อและสนับสนุน

หากพบปัญหาหรือต้องการความช่วยเหลือ:
1. อ่านคู่มือที่เกี่ยวข้องก่อน
2. ตรวจสอบ logs ของ error
3. ตรวจสอบว่าติดตั้ง dependencies ครบถ้วน

**หากพบปัญหาด้านความปลอดภัย:**
- แจ้งทีม IT Security ทันที
- Email: security@g-able.com

---

## 📄 License

MIT License - ใช้งานได้อย่างอิสระ

---

## 🏆 Credits

**พัฒนาโดย:** G-Able IT Team  
**เทคโนโลยี:** Flask, SQLite, ReportLab  
**Version:** 4.1  
**อัพเดทล่าสุด:** October 2025

---

**พัฒนาด้วย ❤️ โดยใช้ Flask และ SQLite**


