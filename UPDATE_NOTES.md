# 🆕 อัพเดท: เวอร์ชัน 2.0

## การเปลี่ยนแปลงหลัก

### ✨ ฟีเจอร์ใหม่

1. **เพิ่มข้อมูลพนักงาน**
   - ชื่อ (First Name)
   - นามสกุล (Last Name)
   - รหัสพนักงาน (Employee ID)

2. **ความยากของลูกค้า (Difficulty Customer) - ใหม่!**
   - Governance = 5
   - State Enterprise = 5
   - Banking = 4
   - Telco = 4
   - Other = 3

3. **ความยากของงาน (Difficulty Type of Project) - ใหม่!**
   
   **Complexity Level: High**
   - New Business = 2.0
   - (Application or Custom SW) + Infrastructure = 1.8
   
   **Complexity Level: Medium**
   - Application = 1.7
   - Custom software package = 1.6
   - Rollout = 1.5
   - SW infra = 1.4
   - Infrastructure integration = 1.3
   
   **Complexity Level: Normal**
   - Service = 1.2
   - Hardware/Software delivery = 1.0

### 📊 สูตรการคำนวณใหม่

```
คะแนน = (ความคืบหน้า% ÷ 100) × ความยากของลูกค้า × ความยากของงาน
```

**ตัวอย่าง:**
- ลูกค้า: Banking (4)
- งาน: Application (1.7)
- ความคืบหน้า: 80%
- **คะแนน** = (80 ÷ 100) × 4 × 1.7 = **5.44**

---

## 🚀 วิธีอัพเดทโปรแกรม

### ⚠️ สำคัญ: ต้องลบ Database เก่า

เนื่องจากโครงสร้างฐานข้อมูลเปลี่ยนแปลง คุณต้องลบไฟล์ database เก่า:

```
1. ไปที่โฟลเดอร์: C:\Users\User\project-scoring-system
2. ลบไฟล์: project_scoring.db (ถ้ามี)
3. รันโปรแกรมใหม่
```

### ขั้นตอนการรัน (หลังอัพเดท)

**วิธีที่ 1: ใช้ START.bat**
```
1. Double-click START.bat
2. เปิด browser → http://localhost:5000
```

**วิธีที่ 2: ใช้ Command Prompt**
```batch
cd C:\Users\User\project-scoring-system
python app.py
# เปิด browser → http://localhost:5000
```

---

## 📋 ข้อมูลที่ต้องกรอก (เวอร์ชันใหม่)

### ข้อมูลโครงการ
1. ✅ ชื่อโครงการ *
2. ✅ ชื่อ *
3. ✅ นามสกุล *
4. ✅ รหัสพนักงาน *
5. ✅ ความยากของลูกค้า (Difficulty Customer)
6. ✅ ความยากของงาน (Difficulty Type of Project)
7. ✅ ความคืบหน้า (0-100%)
8. ✅ หมายเหตุ (ถ้ามี)

---

## 🆚 เปรียบเทียบเวอร์ชันเก่า vs ใหม่

### เวอร์ชัน 1.0 (เก่า)
```
- ชื่อโครงการ
- ความยาก (ง่าย, ปานกลาง, ยาก, ยากมาก)
- ความคืบหน้า
- ประเภทลูกค้า (ทั่วไป, องค์กร, VIP, รัฐ)
```

### เวอร์ชัน 2.0 (ใหม่)
```
✨ ชื่อโครงการ
✨ ชื่อ
✨ นามสกุล
✨ รหัสพนักงาน
✨ ความยากของลูกค้า (Governance, State Enterprise, Banking, Telco, Other)
✨ ความยากของงาน (9 ประเภท แบ่งตาม Complexity)
✨ ความคืบหน้า
```

---

## 💾 การสำรองข้อมูลเก่า (ถ้าต้องการ)

ถ้าคุณมีข้อมูลเก่าและต้องการสำรอง:

```batch
1. ไปที่โฟลเดอร์: C:\Users\User\project-scoring-system
2. คัดลอกไฟล์ project_scoring.db
3. เปลี่ยนชื่อเป็น project_scoring_backup_old.db
4. เก็บไว้ที่อื่น
```

---

## 🎯 การทดสอบหลังอัพเดท

### ทดสอบฟีเจอร์ใหม่:

1. **เพิ่มโครงการทดสอบ**
   - ชื่อโครงการ: "ทดสอบระบบใหม่"
   - ชื่อ: "สมชาย"
   - นามสกุล: "ใจดี"
   - รหัสพนักงาน: "EMP001"
   - ความยากของลูกค้า: Banking
   - ความยากของงาน: Application
   - ความคืบหน้า: 50%
   - คลิก "คำนวณคะแนน"
   - **ควรได้คะแนน**: 3.40

2. **ทดสอบคะแนนสูงสุด**
   - ลูกค้า: Governance (5)
   - งาน: New Business (2.0)
   - ความคืบหน้า: 100%
   - **ควรได้คะแนน**: 10.00

3. **ทดสอบคะแนนต่ำสุด**
   - ลูกค้า: Other (3)
   - งาน: Hardware/Software delivery (1.0)
   - ความคืบหน้า: 25%
   - **ควรได้คะแนน**: 0.75

---

## 📊 ตัวอย่างการคำนวณคะแนน

### ตัวอย่างที่ 1: โครงการ Banking
```
ลูกค้า: Banking (4)
งาน: Application (1.7)
ความคืบหน้า: 75%

คะแนน = (75 ÷ 100) × 4 × 1.7
      = 0.75 × 4 × 1.7
      = 5.10
```

### ตัวอย่างที่ 2: โครงการ State Enterprise
```
ลูกค้า: State Enterprise (5)
งาน: New Business (2.0)
ความคืบหน้า: 60%

คะแนน = (60 ÷ 100) × 5 × 2.0
      = 0.60 × 5 × 2.0
      = 6.00
```

### ตัวอย่างที่ 3: โครงการ Telco
```
ลูกค้า: Telco (4)
งาน: Infrastructure integration (1.3)
ความคืบหน้า: 90%

คะแนน = (90 ÷ 100) × 4 × 1.3
      = 0.90 × 4 × 1.3
      = 4.68
```

---

## ❓ คำถามที่พบบ่อย

**Q: ข้อมูลเก่าหายไปไหม?**
A: ใช่ เพราะโครงสร้าง database เปลี่ยน ต้องเริ่มใหม่

**Q: ต้องติดตั้งอะไรเพิ่มไหม?**
A: ไม่ต้อง ใช้ packages เดิม

**Q: สูตรคำนวณเปลี่ยนแปลงยังไง?**
A: เปลี่ยนจาก `(Progress × Difficulty × Customer Type) × 100`
   เป็น `(Progress × Difficulty Customer × Difficulty Project) / 100`

**Q: คะแนนสูงสุดคือเท่าไหร่?**
A: 10.00 (Governance/State Enterprise × New Business × 100%)

---

## 🐛 แก้ไขปัญหา

### ปัญหา: ไม่มีฟีลด์ใหม่ในเว็บ
**แก้ไข**: 
1. Refresh browser (F5)
2. Clear cache (Ctrl + Shift + Delete)
3. ปิดหยุด Flask server (Ctrl+C)
4. ลบไฟล์ project_scoring.db
5. รันใหม่

### ปัญหา: Error "no such column"
**แก้ไข**:
1. ลบไฟล์ project_scoring.db
2. รันโปรแกรมใหม่
3. Database ใหม่จะถูกสร้างอัตโนมัติ

---

## 📝 Changelog

### Version 2.0 (2025-10-17)
- ✨ เพิ่มฟีลด์ชื่อ นามสกุล รหัสพนักงาน
- ✨ เปลี่ยนระบบความยากเป็น Difficulty Customer
- ✨ เปลี่ยนระบบประเภทงานเป็น Difficulty Type of Project
- ✨ อัพเดทสูตรการคำนวณคะแนนใหม่
- 🔧 ปรับปรุง UI ให้รองรับข้อมูลเพิ่มเติม
- 🔧 เพิ่ม optgroup ใน dropdown เพื่อแบ่งกลุ่ม Complexity Level

### Version 1.0 (2025-10-17)
- 🎉 เวอร์ชันแรก
- ✅ ระบบ CRUD พื้นฐาน
- ✅ คำนวณคะแนนตามความยากและประเภทลูกค้า

---

**อัพเดทเมื่อ**: 17 ตุลาคม 2568
**พร้อมใช้งาน!** 🎉



