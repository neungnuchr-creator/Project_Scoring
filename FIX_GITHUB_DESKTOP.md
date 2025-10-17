# 🔧 แก้ปัญหา GitHub Desktop - ปุ่ม Commit กดไม่ได้

## ปัญหา: ปุ่ม "Commit to Project_score" กดไม่ได้ (สีเทา/Disabled)

---

## ✅ วิธีแก้ทั้งหมด

### วิธีที่ 1: ตรวจสอบว่าเลือกไฟล์แล้วหรือยัง

#### ขั้นตอน:
1. ดูด้านซ้ายมือที่ **"Changes"**
2. จะเห็นรายการไฟล์ที่เปลี่ยนแปลง
3. **ติ๊กเครื่องหมายถูก** (✓) ที่ไฟล์ที่ต้องการ commit

#### ภาพประกอบ:
```
Changes (25)
├─ ✅ app.py                        ← ต้องมีเครื่องหมายถูก
├─ ✅ templates/dashboard.html     ← ติ๊กที่นี่
├─ ✅ templates/admin.html         
├─ ✅ requirements.txt              
└─ ✅ README.md                     
```

#### เลือกทั้งหมดอย่างรวดเร็ว:
- **คลิก "Select All"** (ถ้ามี)
- หรือกด **Ctrl + A** ในหน้าต่าง Changes

---

### วิธีที่ 2: กรอก Summary (ข้อความ commit)

#### ขั้นตอน:
1. ดูด้านล่างซ้าย จะมีช่อง:
   ```
   Summary (required)
   [_________________] ← พิมพ์ที่นี่
   
   Description
   [_________________] ← (ไม่บังคับ)
   ```

2. **พิมพ์ข้อความในช่อง Summary** (บังคับ!)

#### ตัวอย่างข้อความ:
- `Initial commit`
- `Add project files`
- `Update Project Scoring System`
- `First upload to GitHub`
- `Complete version October 2025`

#### ⚠️ ข้อควรระวัง:
- **ต้องกรอก Summary** ไม่งั้นปุ่มจะกดไม่ได้
- Description ไม่กรอกก็ได้
- ไม่ต้องยาวมาก แค่ 5-10 คำ

---

### วิธีที่ 3: ตรวจสอบ Branch

#### ขั้นตอน:
1. ดูที่มุมบน จะเห็น:
   ```
   Current Branch: [ชื่อ branch]
   ```

2. **ถ้าเป็น "main" หรือ "master":**
   - ให้เปลี่ยนเป็น `Project_score` ก่อน

#### วิธีสร้าง Branch ใหม่:

**A. คลิกที่ Current Branch**
```
┌──────────────────────┐
│ Current Branch: main │ ← คลิกที่นี่
└──────────────────────┘
```

**B. คลิก "New Branch"**
```
┌──────────────────────┐
│ ○ main               │
│ [New Branch]         │ ← คลิกที่นี่
└──────────────────────┘
```

**C. พิมพ์ชื่อ Branch**
```
┌──────────────────────────┐
│ Name:                    │
│ [Project_score]          │ ← พิมพ์ที่นี่
│                          │
│ [Create Branch]          │ ← คลิก
└──────────────────────────┘
```

**D. ตอนนี้ควรเห็น:**
```
Current Branch: Project_score ✅
```

---

### วิธีที่ 4: ตรวจสอบว่ามีการเปลี่ยนแปลงจริงๆ

#### อาการ:
- ไม่เห็นไฟล์ใดๆ ใน Changes
- แสดงข้อความ "No local changes"

#### สาเหตุ:
- ไฟล์ทั้งหมด commit ไปแล้ว
- หรือยังไม่ได้แก้ไขอะไร

#### วิธีแก้:
1. แก้ไขไฟล์ใดๆ ในโปรเจค
2. กลับมาที่ GitHub Desktop
3. จะเห็นไฟล์ที่เปลี่ยนแปลงขึ้นมาอัตโนมัติ

---

### วิธีที่ 5: Restart GitHub Desktop

#### ถ้าวิธีอื่นไม่ได้ผล:
1. ปิด GitHub Desktop
2. เปิดใหม่
3. เปิด repository: `File → Add Local Repository`
4. เลือก: `C:\Users\User\project-scoring-system`
5. ลองอีกครั้ง

---

## 📋 Checklist ก่อน Commit

ก่อนกด Commit ให้ตรวจสอบ:

- [ ] ✅ มีไฟล์ใน Changes อย่างน้อย 1 ไฟล์
- [ ] ✅ ติ๊กเครื่องหมายถูกที่ไฟล์ที่ต้องการ
- [ ] ✅ กรอก Summary (required) แล้ว
- [ ] ✅ Branch เป็น "Project_score" (ไม่ใช่ main)
- [ ] ✅ ปุ่ม "Commit to Project_score" เป็นสีน้ำเงิน (ไม่ใช่สีเทา)

---

## 🎯 ขั้นตอนทั้งหมดอีกครั้ง

### 1. เปิด GitHub Desktop
```
เปิดโปรแกรม GitHub Desktop
```

### 2. เปิด Repository
```
File → Add Local Repository
เลือก: C:\Users\User\project-scoring-system
```

### 3. สร้าง/เปลี่ยน Branch
```
Current Branch → New Branch → "Project_score"
```

### 4. เลือกไฟล์
```
✅ เลือกไฟล์ทั้งหมดใน Changes
```

### 5. กรอก Summary
```
Summary: "Initial commit"
```

### 6. Commit
```
คลิก "Commit to Project_score" (ควรเป็นสีน้ำเงิน)
```

### 7. Push
```
คลิก "Push origin"
```

---

## 🖼️ ตัวอย่างหน้าจอที่ถูกต้อง

```
┌─────────────────────────────────────────────────┐
│ GitHub Desktop                                  │
│                                                 │
│ Current Branch: Project_score          [▼]     │ ← Branch ถูกต้อง
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│ Changes (25)                                    │ ← มีไฟล์
│                                                 │
│ ✅ app.py                                       │ ← ติ๊กแล้ว
│ ✅ templates/dashboard.html                     │
│ ✅ templates/admin.html                         │
│ ✅ requirements.txt                             │
│ ✅ README.md                                    │
│ ... (แสดงไฟล์อื่นๆ)                            │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│ Summary (required)                              │
│ [Initial commit]                                │ ← กรอกแล้ว
│                                                 │
│ Description                                     │
│ [Complete project files]                        │ ← (ไม่บังคับ)
│                                                 │
│ [Commit to Project_score]                       │ ← สีน้ำเงิน กดได้!
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## ⚠️ สถานการณ์ที่ปุ่มกดไม่ได้

### 1. ปุ่มเป็นสีเทา (Disabled)
```
[Commit to Project_score]  ← สีเทา
```
**สาเหตุ:** ขาด Summary หรือไม่มีไฟล์เลือก

### 2. ปุ่มไม่แสดง
```
(ไม่มีปุ่ม Commit)
```
**สาเหตุ:** ไม่มีการเปลี่ยนแปลงใดๆ

### 3. แสดง "No local changes"
```
No local changes
```
**สาเหตุ:** ไฟล์ทั้งหมด commit ไปแล้ว

---

## 🆘 ยังไม่ได้?

### ลองวิธีนี้:

#### A. ใช้ Command Line แทน:
1. เปิด PowerShell ในโฟลเดอร์โปรเจค
2. รันคำสั่ง:
   ```bash
   cd C:\Users\User\project-scoring-system
   git init
   git checkout -b Project_score
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/neungnuchr-creator/Project_Scoring.git
   git push -u origin Project_score
   ```

#### B. ใช้ Web Upload:
1. สร้างไฟล์ ZIP ของโปรเจค
2. ไปที่: https://github.com/neungnuchr-creator/Project_Scoring/tree/Project_score
3. คลิก "Add file" → "Upload files"
4. ลากไฟล์มาวาง

---

## 📞 ต้องการความช่วยเหลือเพิ่มเติม?

ถ้ายังแก้ไม่ได้ กรุณาส่ง:
1. Screenshot หน้าจอ GitHub Desktop
2. ข้อความ error (ถ้ามี)
3. Branch ที่กำลังใช้อยู่
4. จำนวนไฟล์ที่เห็นใน Changes

---

**สร้างโดย:** Project Scoring System Team  
**อัปเดต:** October 2025

