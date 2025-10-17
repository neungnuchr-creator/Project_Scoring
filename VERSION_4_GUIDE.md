# 🎉 เวอร์ชัน 4.0 - ระบบ Login & User Management

## 🆕 อัพเดทครั้งใหญ่!

เวอร์ชัน 4.0 เพิ่มระบบ Login และแยกสิทธิ์การใช้งานระหว่าง **พนักงาน** และ **Admin**

---

## ✨ ฟีเจอร์ใหม่

### 1. ระบบ Login/Register
- ✅ พนักงานสมัครสมาชิกด้วยตัวเอง
- ✅ กรอกข้อมูล (ชื่อ, นามสกุล, รหัสพนักงาน) ครั้งเดียว
- ✅ ไม่ต้องกรอกซ้ำทุกครั้ง
- ✅ Login ด้วย Username/Password

### 2. แยกสิทธิ์ผู้ใช้งาน
- 👤 **Employee (พนักงาน)**
  - เห็นเฉพาะโครงการของตัวเอง
  - เพิ่ม/แก้ไข/ลบ โครงการของตัวเอง
  - ดูสถิติของตัวเอง
  
- 👑 **Admin**
  - เห็นโครงการของทุกคน
  - ดูสถิติทั้งระบบ
  - ค้นหาและกรองข้อมูล
  - Auto-refresh ทุก 30 วินาที

### 3. การแก้ไขตามคำขอ
- ✅ แก้ "Governance" → "Government"
- ✅ เปลี่ยนป้าย → "ความคืบหน้าประจำปี (ปีปัจจุบัน)"
- ✅ แก้สูตร Baseline Manday ให้รวม Progress
- ✅ เพิ่ม "(Manday)" ใน Baseline PM Effort
- ✅ เปลี่ยนสถิติ → "คะแนนรวม" (แทน คะแนนเฉลี่ย)

---

## 📊 สูตรการคำนวณ (อัพเดท)

### Baseline Manday (แก้ไขแล้ว!)

```
Baseline Manday = ความยากโครงการ × (
    (ความยากโครงการ × (baseline_pm_effort/ระยะเวลา) × ระยะเวลา × (Progress/100) / 100)
    + Challenge_topup
)
```

**สิ่งที่เปลี่ยน:**
- ✅ เพิ่ม `× (Progress/100)` เพื่อให้ Baseline Manday ปรับตาม % ความคืบหน้า

---

## 🚀 วิธีเริ่มใช้งาน

### ⚠️ สำคัญมาก: ต้องลบ Database เก่า!

```
1. ไปที่โฟลเดอร์: C:\Users\User\project-scoring-system
2. ลบไฟล์: project_scoring.db (ถ้ามี)
```

### ขั้นตอนรัน

**วิธีที่ 1: ใช้ START.bat**
```
1. Double-click START.bat
2. รอจนเซิร์ฟเวอร์เริ่ม
3. เปิด browser → http://localhost:5000
```

**วิธีที่ 2: ใช้ Command Prompt**
```bash
cd C:\Users\User\project-scoring-system
python app.py
# เปิด browser → http://localhost:5000
```

---

## 👤 การใช้งานสำหรับพนักงาน

### ขั้นตอนที่ 1: สมัครสมาชิก

1. เปิด `http://localhost:5000`
2. จะเจอหน้า Login → คลิก "✨ สมัครสมาชิก"
3. กรอกข้อมูล:
   - ชื่อ *
   - นามสกุล *
   - รหัสพนักงาน * (ต้องไม่ซ้ำกัน)
   - Username * (สำหรับ login, ต้องไม่ซ้ำกัน)
   - Password * (อย่างน้อย 6 ตัว)
   - ยืนยัน Password *
4. คลิก "✅ สมัครสมาชิก"
5. รอระบบพาไปหน้า Login

### ขั้นตอนที่ 2: Login

1. กรอก Username และ Password
2. คลิก "🔐 เข้าสู่ระบบ"
3. ระบบจะพาไปหน้า Dashboard

### ขั้นตอนที่ 3: เพิ่มโครงการ

หน้า Dashboard จะแสดง:
- ชื่อ-นามสกุล และ รหัสพนักงานของคุณ (ไม่ต้องกรอกอีก!)
- ฟอร์มเพิ่มโครงการ
- รายการโครงการของคุณเท่านั้น

กรอกข้อมูลโครงการ:
1. ชื่อโครงการ
2. ความยากของลูกค้า (Government, State Enterprise, Banking, Telco, Other)
3. ความยากของงาน (9 ประเภท)
4. ความคืบหน้าประจำปี (%) ← **ป้ายใหม่**
5. Baseline PM Effort (Manday) ← **เพิ่ม (Manday)**
6. ระยะเวลาโครงการ (เดือน)
7. Challenge Type
8. หมายเหตุ

คลิก "🔢 คำนวณ" → แสดงคะแนนและ Baseline Manday

คลิก "➕ เพิ่ม" → บันทึกโครงการ

### ขั้นตอนที่ 4: จัดการโครงการ

- **แก้ไข**: คลิกที่โครงการในตาราง → แก้ไขข้อมูล → คลิก "✏️ อัปเดต"
- **ลบ**: คลิกที่โครงการ → คลิก "🗑️ ลบ"
- **ล้างฟอร์ม**: คลิก "🔄 ล้าง"

### สถิติที่แสดง (พนักงาน)

- จำนวนโครงการ (ของคุณ)
- **คะแนนรวม** (ของคุณ) ← **เปลี่ยนจาก คะแนนเฉลี่ย**
- คะแนนสูงสุด (ของคุณ)
- ความคืบหน้าเฉลี่ย
- Manday เฉลี่ย

---

## 👑 การใช้งานสำหรับ Admin

### Login Admin

**ข้อมูล Default:**
- Username: `admin`
- Password: `admin123`

### หน้า Admin Dashboard

Admin จะเห็น:
- ✅ สถิติโครงการทั้งระบบ
- ✅ รายการโครงการของทุกคน
- ✅ ชื่อพนักงานที่รับผิดชอบแต่ละโครงการ
- ✅ ช่องค้นหา (ค้นหาชื่อโครงการ, พนักงาน, รหัส)
- ✅ Auto-refresh ทุก 30 วินาที

### สถิติที่แสดง (Admin)

- จำนวนโครงการทั้งหมด
- **คะแนนรวมทั้งหมด** ← **เปลี่ยนจาก คะแนนเฉลี่ย**
- คะแนนสูงสุดในระบบ
- ความคืบหน้าเฉลี่ย
- Manday เฉลี่ย

---

## 🧪 ทดสอบการทำงาน

### Test Case 1: สมัครพนักงานใหม่

```
ชื่อ: สมชาย
นามสกุล: ใจดี
รหัสพนักงาน: EMP001
Username: somchai
Password: 123456
```

### Test Case 2: เพิ่มโครงการ

```
ชื่อโครงการ: ระบบทดสอบ
ความยากของลูกค้า: Banking (4)
ความยากของงาน: Application (1.7)
ความคืบหน้า: 50%
Baseline PM Effort: 50 manday
ระยะเวลา: 5 เดือน
Challenge: None

คำนวณ:
คะแนน = (50/100) × 4 × 1.7 = 3.40
Baseline Manday = 1.7 × ((1.7 × (50/5) × 5 × 0.5 / 100) + 0)
                = 1.7 × (0.425)
                = 0.72 manday
```

### Test Case 3: Admin Login

```
Username: admin
Password: admin123

→ จะเห็นโครงการของทุกคน
```

---

## 📋 เปรียบเทียบเวอร์ชัน

| ฟีเจอร์ | v3.0 (เก่า) | v4.0 (ใหม่) |
|---------|-------------|------------|
| Login/Register | ❌ | ✅ |
| กรอกชื่อ-นามสกุล | ทุกครั้ง | ครั้งเดียว |
| แยกสิทธิ์ | ❌ | ✅ (Employee/Admin) |
| เห็นโครงการ | ทั้งหมด | แยกตาม user |
| Admin Dashboard | ❌ | ✅ |
| Government | Governance | Government ✅ |
| Progress Label | ความคืบหน้า(%) | ประจำปี(ปีปัจจุบัน) ✅ |
| Baseline PM Effort | - | (Manday) ✅ |
| สถิติ | คะแนนเฉลี่ย | คะแนนรวม ✅ |
| สูตร Baseline | ไม่มี Progress | มี Progress ✅ |

---

## 🔐 ความปลอดภัย

- ✅ Password เข้ารหัสด้วย `werkzeug.security`
- ✅ ใช้ Session management
- ✅ Protected routes ด้วย `@login_required`
- ✅ Admin routes ต้องมี `@admin_required`

---

## 📂 โครงสร้างฐานข้อมูลใหม่

### ตาราง users
```sql
- id (PK)
- username (UNIQUE)
- password (hashed)
- first_name
- last_name
- employee_id (UNIQUE)
- role (employee/admin)
- created_date
```

### ตาราง projects
```sql
- id (PK)
- user_id (FK → users.id)
- project_name
- difficulty_customer
- difficulty_project
- progress
- baseline_pm_effort
- project_duration
- challenge_type
- score
- baseline_manday
- created_date
- updated_date
- notes
```

---

## ❓ คำถามที่พบบ่อย

**Q: ต้องสมัครสมาชิกใหม่ทุกคนไหม?**
A: ใช่! เพราะเป็นโครงสร้าง database แบบใหม่

**Q: Admin มีกี่คน?**
A: Default มี 1 คน (admin/admin123) สามารถสร้างเพิ่มได้ใน database

**Q: พนักงานเห็นโครงการคนอื่นได้ไหม?**
A: ไม่ได้ เห็นแค่ของตัวเอง

**Q: Admin แก้ไขโครงการได้ไหม?**
A: เวอร์ชันนี้ Admin ดูอย่างเดียว (read-only)

**Q: ลืม Password ทำยังไง?**
A: ต้องให้ Admin reset ใน database โดยตรง

**Q: Username ซ้ำได้ไหม?**
A: ไม่ได้ ต้องไม่ซ้ำกัน

**Q: รหัสพนักงานซ้ำได้ไหม?**
A: ไม่ได้ ต้องไม่ซ้ำกัน

---

## 🛠️ การจัดการผู้ใช้ (สำหรับ Admin)

### ดู User ทั้งหมด
```sql
sqlite3 project_scoring.db
SELECT * FROM users;
```

### เปลี่ยน Password
```python
# ใน Python console
from werkzeug.security import generate_password_hash
new_password = generate_password_hash('newpassword123')
print(new_password)

# นำ hash ไปอัพเดทใน database
```

### เปลี่ยน Role
```sql
UPDATE users SET role = 'admin' WHERE employee_id = 'EMP001';
```

---

## 📝 Changelog

### Version 4.0 (2025-10-17)
- ✨ เพิ่มระบบ Login/Register
- ✨ แยกสิทธิ์ Employee และ Admin
- ✨ พนักงานกรอกข้อมูลตัวเองครั้งเดียว
- ✨ แต่ละคนเห็นเฉพาะโครงการตัวเอง
- ✨ Admin เห็นทุกโครงการ + ค้นหาได้
- ✅ แก้ Governance → Government
- ✅ เปลี่ยนป้าย Progress
- ✅ แก้สูตร Baseline Manday ให้รวม Progress
- ✅ เพิ่ม (Manday) ใน label
- ✅ เปลี่ยนสถิติเป็นคะแนนรวม
- 🔐 เพิ่มระบบความปลอดภัย

### Version 3.0 (2025-10-17)
- เพิ่ม Baseline Manday

### Version 2.0 (2025-10-17)
- เพิ่มข้อมูลพนักงาน

### Version 1.0 (2025-10-17)
- เวอร์ชันแรก

---

## 🎊 พร้อมใช้งาน!

```
1. ลบ project_scoring.db (ถ้ามี)
2. Double-click START.bat
3. เปิด browser → http://localhost:5000
4. สมัครสมาชิก
5. Login และเริ่มใช้งาน!
```

**Admin Default:**
- Username: `admin`
- Password: `admin123`

---

**เวอร์ชัน 4.0 พร้อมใช้งานแล้ว! 🎉**


