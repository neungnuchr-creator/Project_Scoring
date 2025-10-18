# 🧪 คู่มือทดสอบระบบ - Email & Approval System

## 🎯 ระบบที่ต้องทดสอบ:

1. ✅ Email Validation (@g-able.com)
2. ✅ User Registration
3. ✅ Approval System
4. ✅ Admin User Management
5. ✅ Login with Approval Check

---

## 🚀 การทดสอบแบบครบถ้วน:

### **Test 1: สมัครสมาชิก - Email Validation**

#### ขั้นตอน:
1. เปิด `http://localhost:5000/register`
2. กรอกข้อมูล:
   - ชื่อ: `ทดสอบ`
   - นามสกุล: `ระบบ`
   - รหัสพนักงาน: `TEST001`
   - Email: `test@gmail.com` ❌
   - Username: `testuser`
   - Password: `test1234`
   - ยืนยันรหัสผ่าน: `test1234`
3. กด "สมัครสมาชิก"

#### ผลที่คาดหวัง:
```
❌ แสดง error: "อีเมลต้องเป็น @g-able.com เท่านั้น"
```

---

### **Test 2: สมัครสมาชิก - สำเร็จ**

#### ขั้นตอน:
1. เปิด `http://localhost:5000/register`
2. กรอกข้อมูล:
   - ชื่อ: `ทดสอบ`
   - นามสกุล: `ระบบ`
   - รหัสพนักงาน: `TEST001`
   - Email: `test@g-able.com` ✅
   - Username: `testuser`
   - Password: `test1234`
   - ยืนยันรหัสผ่าน: `test1234`
3. กด "สมัครสมาชิก"

#### ผลที่คาดหวัง:
```
✅ แสดงข้อความสีเขียว: "สมัครสมาชิกสำเร็จ! ✅ รอผู้ดูแลระบบอนุมัติ..."
✅ Redirect ไปหน้า login หลัง 3 วินาที
```

---

### **Test 3: Login ก่อนได้รับการอนุมัติ**

#### ขั้นตอน:
1. เปิด `http://localhost:5000/login`
2. Login ด้วย:
   - Username: `testuser`
   - Password: `test1234`
3. กด "เข้าสู่ระบบ"

#### ผลที่คาดหวัง:
```
❌ แสดง error สีแดง: "รอการอนุมัติจากผู้ดูแลระบบ"
❌ ไม่สามารถเข้าระบบได้
```

---

### **Test 4: Admin Dashboard - เห็น User Management**

#### ขั้นตอน:
1. เปิด `http://localhost:5000/login`
2. Login ด้วย admin (ดู `ADMIN_CREDENTIALS.txt`)
3. เข้าสู่ Admin Dashboard

#### ผลที่คาดหวัง:
```
✅ เห็น Section "👥 จัดการผู้ใช้งาน"
✅ เห็น badge "รออนุมัติ: 1" (หรือมากกว่า)
✅ เห็น 3 tabs:
   - ⏰ รออนุมัติ (1)
   - ✅ อนุมัติแล้ว (3)
   - 👥 ทั้งหมด (4)
```

---

### **Test 5: ดูรายการ Users รออนุมัติ**

#### ขั้นตอน:
1. อยู่ที่หน้า Admin Dashboard
2. ดูที่ Section "จัดการผู้ใช้งาน"
3. Tab "รออนุมัติ" เลือกอยู่แล้ว (default)

#### ผลที่คาดหวัง:
```
✅ เห็นรายการ users ที่ approved = 0
✅ แสดงข้อมูล:
   - ID
   - ชื่อ-นามสกุล (พร้อม Avatar)
   - Email
   - รหัสพนักงาน
   - Username
   - สถานะ: "⏰ รออนุมัติ"
   - วันที่สมัคร
   - ปุ่ม: "✅ อนุมัติ" และ "❌ ปฏิเสธ"
```

---

### **Test 6: อนุมัติ User**

#### ขั้นตอน:
1. คลิกปุ่ม "✅ อนุมัติ" ของ user ที่สมัครใหม่
2. ยืนยันใน popup

#### ผลที่คาดหวัง:
```
✅ แสดง notification สีเขียว: "อนุมัติ ทดสอบ ระบบ สำเร็จ"
✅ User หายจาก tab "รออนุมัติ"
✅ User ปรากฏใน tab "อนุมัติแล้ว"
✅ Badge "รออนุมัติ: 0" อัพเดท
```

---

### **Test 7: Login หลังได้รับการอนุมัติ**

#### ขั้นตอน:
1. Logout จาก admin
2. Login ด้วย:
   - Username: `testuser`
   - Password: `test1234`
3. กด "เข้าสู่ระบบ"

#### ผลที่คาดหวัง:
```
✅ Login สำเร็จ
✅ Redirect ไปหน้า Dashboard
✅ เห็นหน้า User Dashboard
```

---

### **Test 8: ปฏิเสธ User (Optional)**

#### ขั้นตอน:
1. สมัครสมาชิกใหม่อีกคน (test2@g-able.com)
2. Login เป็น admin
3. ไปที่ tab "รออนุมัติ"
4. คลิก "❌ ปฏิเสธ"
5. ยืนยันใน popup

#### ผลที่คาดหวัง:
```
✅ แสดง warning popup:
   "⚠️ ยืนยันการปฏิเสธและลบ..."
   "- User จะถูกลบออกจากระบบถาวร"
   "- โครงการทั้งหมดของ user นี้จะถูกลบด้วย"
   
✅ หลังยืนยัน:
   - แสดง notification: "ปฏิเสธและลบ ... สำเร็จ"
   - User หายจากรายการ
   - Projects ของ user ถูกลบ (ถ้ามี)
```

---

### **Test 9: Auto Refresh**

#### ขั้นตอน:
1. เปิด Admin Dashboard ทิ้งไว้
2. เปิด browser window ใหม่
3. สมัครสมาชิกใหม่
4. กลับมาดู Admin Dashboard (รอ 30 วินาที หรือกด "รีเฟรช Users")

#### ผลที่คาดหวัง:
```
✅ User ใหม่ปรากฏในรายการ (หลัง 30 วินาที หรือหลังกด refresh)
✅ จำนวน "รออนุมัติ" อัพเดทอัตโนมัติ
```

---

### **Test 10: ดูรายการ Users ที่อนุมัติแล้ว**

#### ขั้นตอน:
1. คลิก tab "✅ อนุมัติแล้ว"

#### ผลที่คาดหวัง:
```
✅ เห็น users ทั้งหมดที่ approved = 1
✅ แสดงสถานะ: "✅ อนุมัติแล้ว"
✅ แสดงข้อความ: "✅ ใช้งานได้แล้ว" (ไม่มีปุ่ม approve/reject)
```

---

### **Test 11: ดูรายการทั้งหมด**

#### ขั้นตอน:
1. คลิก tab "👥 ทั้งหมด"

#### ผลที่คาดหวัง:
```
✅ เห็น users ทั้งหมด (ทั้ง pending และ approved)
✅ แสดงสถานะที่ถูกต้องของแต่ละ user
✅ ปุ่ม approve/reject แสดงเฉพาะ users ที่ pending
```

---

## 🔍 Debug Console Logs:

### เปิด Developer Tools (F12) → Console

#### **Test Registration:**
```
🚀 Form submitted!
📝 Form data: {firstName: "ทดสอบ", lastName: "ระบบ", ...}
✅ Email validation passed
⏳ Sending request to /api/register...
📡 Response status: 200
✅ Success response: {success: true, message: "..."}
```

#### **Test Load Users (Admin):**
```
Fetching: /api/admin/users
Users loaded: 4
Pending: 1, Approved: 3, All: 4
```

---

## 📊 Checklist สำหรับทดสอบทั้งหมด:

### Registration:
- [ ] Email ไม่ใช่ @g-able.com → Error
- [ ] Email เป็น @g-able.com → สำเร็จ
- [ ] Username ซ้ำ → Error
- [ ] Employee ID ซ้ำ → Error
- [ ] รหัสผ่านไม่ตรงกัน → Error
- [ ] สมัครสำเร็จแสดง "รอการอนุมัติ"

### Login:
- [ ] User ที่ pending → Error "รอการอนุมัติ"
- [ ] User ที่ approved → Login ได้
- [ ] Admin → Login ได้ปกติ
- [ ] Username/Password ผิด → Error

### Admin Dashboard:
- [ ] เห็น Section "จัดการผู้ใช้งาน"
- [ ] เห็น badge "รออนุมัติ: X"
- [ ] Tabs ทำงาน (pending/approved/all)
- [ ] แสดงรายการ users ถูกต้อง

### User Management:
- [ ] กด "อนุมัติ" → สำเร็จ
- [ ] User ย้ายไปแท็บ "อนุมัติแล้ว"
- [ ] User login ได้หลังถูกอนุมัติ
- [ ] กด "ปฏิเสธ" → ลบสำเร็จ
- [ ] Auto-refresh ทำงาน (30 วินาที)
- [ ] Manual refresh ทำงาน

---

## 🎨 UI ที่ควรเห็น:

### **Admin Dashboard - User Management Section:**

```
┌────────────────────────────────────────────────────────────┐
│ 👥 จัดการผู้ใช้งาน        [⏰ รออนุมัติ: 1] [🔄 รีเฟรช] │
├────────────────────────────────────────────────────────────┤
│ [⏰ รออนุมัติ (1)] [✅ อนุมัติแล้ว (3)] [👥 ทั้งหมด (4)]│
├────────────────────────────────────────────────────────────┤
│ ID │ ชื่อ     │ Email         │ รหัส │ สถานะ │ จัดการ   │
├────┼──────────┼───────────────┼──────┼────────┼───────────┤
│ 5  │ 👤 ทดสอบ │test@g-able... │TEST..│⏰ รอ..│✅อนุมัติ ❌│
└────────────────────────────────────────────────────────────┘
```

---

## 🐛 Troubleshooting:

### ปัญหา: ไม่เห็น Section "จัดการผู้ใช้งาน"

**แก้:**
- Refresh หน้าเว็บ (Ctrl+F5)
- ตรวจสอบว่า login เป็น admin
- ดู Console errors (F12)

### ปัญหา: กดปุ่มแล้วไม่มีอะไรเกิดขึ้น

**แก้:**
- เปิด Console (F12)
- ดู error messages
- ตรวจสอบว่า API ทำงาน:
  ```javascript
  fetch('/api/admin/users').then(r => r.json()).then(console.log)
  ```

### ปัญหา: "TypeError: Cannot read property..."

**แก้:**
- Refresh หน้าเว็บ
- Clear cache (Ctrl+Shift+Del)
- ตรวจสอบ JavaScript errors

---

## 📞 ขั้นตอนหากพบปัญหา:

1. **เปิด Console** (F12) และดู errors
2. **ดู Network tab** ตรวจสอบ API requests
3. **ตรวจสอบ Server logs** ใน Terminal
4. **อ่านคู่มือ:**
   - [HOW_TO_ADD_USER_MANAGEMENT.md](HOW_TO_ADD_USER_MANAGEMENT.md)
   - [COMPLETE_SETUP_GUIDE.md](COMPLETE_SETUP_GUIDE.md)

---

## ✅ ผลลัพธ์สุดท้าย:

หลังจากทดสอบทั้งหมดแล้ว คุณควรได้:

- ✅ ระบบสมัครสมาชิกที่ตรวจสอบ email @g-able.com
- ✅ User ใหม่ไม่สามารถ login จนกว่าจะได้รับการอนุมัติ
- ✅ Admin สามารถอนุมัติหรือปฏิเสธ users ได้
- ✅ UI สวยงามพร้อม animations
- ✅ Auto-refresh ทุก 30 วินาที
- ✅ Notifications แสดงผลการทำงาน

---

**Happy Testing! 🧪✨**

Created: October 2025

