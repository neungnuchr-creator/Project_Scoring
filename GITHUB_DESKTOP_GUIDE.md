# 🖥️ คู่มือการใช้ GitHub Desktop

## 📦 Upload Project Scoring System ไปยัง GitHub

---

## ขั้นตอนที่ 1: ดาวน์โหลดและติดตั้ง

### 1.1 ดาวน์โหลด
- 🌐 ไปที่: https://desktop.github.com/
- ⬇️ กด "Download for Windows"
- 💾 รอให้ดาวน์โหลดเสร็จ (ประมาณ 100 MB)

### 1.2 ติดตั้ง
- 📂 เปิดไฟล์ `GitHubDesktopSetup.exe`
- ⏳ รอให้ติดตั้งเสร็จ (ประมาณ 1-2 นาที)
- ✅ โปรแกรมจะเปิดขึ้นมาอัตโนมัติ

---

## ขั้นตอนที่ 2: Sign In เข้าสู่ระบบ

### 2.1 เข้าสู่ระบบ
```
┌─────────────────────────────┐
│  Welcome to GitHub Desktop  │
│                             │
│  [Sign in to GitHub.com]    │ ← คลิกที่นี่
│                             │
└─────────────────────────────┘
```

### 2.2 Login ผ่าน Browser
- 🌐 Browser จะเปิดขึ้นมา
- 📝 ใส่ Username: `neungnuchr-creator`
- 🔐 ใส่ Password ของคุณ
- ✅ กด "Authorize desktop"

### 2.3 กลับมาที่ GitHub Desktop
- ✅ จะเห็นข้อความว่า "You're signed in!"
- ➡️ กด "Continue"

---

## ขั้นตอนที่ 3: เพิ่ม Repository

### 3.1 Add Local Repository
```
┌─────────────────────────────────────┐
│  File → Add Local Repository...    │ ← คลิกเมนูนี้
└─────────────────────────────────────┘
```

หรือ:
- กด `Ctrl + O`
- หรือกด "Add" ที่มุมซ้ายบน

### 3.2 เลือกโฟลเดอร์
```
┌─────────────────────────────────────┐
│  Choose a local repository          │
│                                     │
│  Local path:                        │
│  [C:\Users\User\project-scoring-... │ ← คลิก "Choose..."
│                                     │
│  [Choose...]           [Cancel]     │
└─────────────────────────────────────┘
```

**เลือกโฟลเดอร์:**
```
C:\Users\User\project-scoring-system
```

### 3.3 สร้าง Repository (ถ้ายังไม่มี .git)
```
┌─────────────────────────────────────┐
│  This directory does not appear     │
│  to be a Git repository.            │
│                                     │
│  Would you like to create a         │
│  repository here instead?           │
│                                     │
│  [Create a Repository]              │ ← คลิกที่นี่
└─────────────────────────────────────┘
```

**กรอกข้อมูล:**
- Name: `Project_Scoring`
- Description: `Project scoring for PMO team start OCT 2025`
- ✅ เลือก **"Initialize this repository with a README"** (ถ้าต้องการ)
- Git ignore: **Python**
- License: **None** (หรือเลือกตามต้องการ)
- ➡️ กด "Create Repository"

---

## ขั้นตอนที่ 4: เชื่อมต่อกับ GitHub Repository

### 4.1 Publish Repository
```
┌─────────────────────────────────────┐
│  Publish repository                 │
│                                     │
│  Name: Project_Scoring              │
│  Description: Project scoring...    │
│                                     │
│  ☐ Keep this code private           │ ← ติ๊กถ้าต้องการ private
│                                     │
│  Organization: None                 │
│                                     │
│  [Publish Repository]               │ ← คลิกที่นี่
└─────────────────────────────────────┘
```

**หรือ** ถ้ามี repository อยู่แล้ว:

### 4.2 เชื่อมต่อกับ Repository ที่มีอยู่

#### A. ไปที่ Repository Settings
```
Repository → Repository Settings... (Ctrl + ,)
```

#### B. ตั้งค่า Remote
```
┌─────────────────────────────────────┐
│  Remote                             │
│                                     │
│  Primary remote repository (origin)│
│                                     │
│  Remote URL:                        │
│  https://github.com/neungnuchr-... │
│                                     │
│  [Save]                             │
└─────────────────────────────────────┘
```

**ใส่ URL:**
```
https://github.com/neungnuchr-creator/Project_Scoring.git
```

---

## ขั้นตอนที่ 5: เปลี่ยน Branch เป็น Project_score

### 5.1 สร้าง Branch ใหม่
```
┌─────────────────────────────────────┐
│  Current Branch: main               │
│                                     │
│  [▼] main                           │ ← คลิกที่นี่
│                                     │
│  [New Branch]                       │ ← เลือกนี้
└─────────────────────────────────────┘
```

### 5.2 ตั้งชื่อ Branch
```
┌─────────────────────────────────────┐
│  Create a Branch                    │
│                                     │
│  Name:                              │
│  [Project_score]                    │ ← พิมพ์ที่นี่
│                                     │
│  Create branch based on:            │
│  • main                             │
│  ○ Current branch                   │
│                                     │
│  [Create Branch]                    │ ← คลิก
└─────────────────────────────────────┘
```

**หรือ** ถ้า Branch มีอยู่แล้วบน GitHub:

### 5.3 Pull Branch จาก GitHub
```
Branch → Pull (Ctrl + Shift + P)
```

---

## ขั้นตอนที่ 6: Commit และ Push

### 6.1 ดูไฟล์ที่เปลี่ยนแปลง

หน้าจอจะแสดง:
```
┌─────────────────────────────────────┐
│  Changes (25)                       │ ← จำนวนไฟล์ที่เปลี่ยน
│                                     │
│  ✅ app.py                          │
│  ✅ templates/dashboard.html        │
│  ✅ templates/admin.html            │
│  ✅ requirements.txt                │
│  ✅ README.md                       │
│  ✅ ...                             │
│                                     │
└─────────────────────────────────────┘
```

### 6.2 เลือกไฟล์ที่ต้องการ Commit
- ✅ **ติ๊กเครื่องหมายถูก** ที่ไฟล์ที่ต้องการ
- หรือกด **Ctrl + A** เพื่อเลือกทั้งหมด

### 6.3 เขียน Commit Message
```
┌─────────────────────────────────────┐
│  Summary (required)                 │
│  [Update Project Scoring System]    │ ← พิมพ์ที่นี่
│                                     │
│  Description                        │
│  [Complete version with modern UI]  │ ← (ไม่บังคับ)
│                                     │
│  [Commit to Project_score]          │ ← คลิก
└─────────────────────────────────────┘
```

**ตัวอย่าง Commit Message:**
- `Update Project Scoring System - Complete version`
- `Add new features: contract no, year field, session timeout`
- `Fix: Update score calculation formula`
- `Improve: Modern UI with better design`

### 6.4 Push ไปยัง GitHub
```
┌─────────────────────────────────────┐
│  Push origin                        │
│                                     │
│  ↑ Push 1 commit to the origin     │
│     remote                          │
│                                     │
│  [Push origin]                      │ ← คลิกที่นี่
└─────────────────────────────────────┘
```

หรือกด: `Ctrl + P`

### 6.5 รอให้ Upload เสร็จ
```
┌─────────────────────────────────────┐
│  Pushing to origin...               │
│                                     │
│  [████████████████░░░░] 75%         │
│                                     │
│  Uploading objects... (15/20)       │
└─────────────────────────────────────┘
```

---

## ขั้นตอนที่ 7: ตรวจสอบผลลัพธ์

### 7.1 เปิด Repository บน GitHub
```
Repository → View on GitHub (Ctrl + Shift + G)
```

หรือไปที่:
```
https://github.com/neungnuchr-creator/Project_Scoring/tree/Project_score
```

### 7.2 ตรวจสอบว่ามีไฟล์ครบหรือไม่
คุณควรเห็น:
- ✅ `app.py`
- ✅ `templates/` folder
- ✅ `requirements.txt`
- ✅ `README.md`
- ✅ `.gitignore`
- ✅ เอกสารต่างๆ

---

## 🎯 เคล็ดลับ

### ✅ ควรทำ:
1. **Commit บ่อยๆ** - แยก commit ตามฟีเจอร์
2. **เขียน message ชัดเจน** - บอกว่าเปลี่ยนอะไร
3. **Pull ก่อน Push** - เพื่อไม่ให้เกิด conflict
4. **ตรวจสอบ Changes** - ก่อน commit ทุกครั้ง

### ❌ ไม่ควรทำ:
1. **อย่า commit ไฟล์ที่ไม่จำเป็น** - เช่น `venv/`, `*.db`
2. **อย่า commit password** - หรือข้อมูลลับ
3. **อย่า force push** - อาจทำข้อมูลหาย

---

## 🆘 แก้ปัญหา

### ปัญหา: ไม่สามารถ Push ได้
**แก้:** 
- ตรวจสอบว่าคุณมีสิทธิ์ในการ push หรือไม่
- ลอง Sign out และ Sign in ใหม่
- ตรวจสอบ Internet connection

### ปัญหา: มี Conflict
**แก้:**
- Pull ก่อน: `Repository → Pull`
- แก้ไขไฟล์ที่ conflict
- Commit และ Push ใหม่

### ปัญหา: ไฟล์บางไฟล์ไม่ขึ้น
**แก้:**
- ตรวจสอบ `.gitignore` - อาจถูกกรองออก
- ลบไฟล์ออกจาก `.gitignore` ถ้าต้องการอัปโหลด

---

## 📱 การใช้งานต่อไป

### การอัปเดตใหม่:
1. แก้ไข code ในโปรเจค
2. เปิด GitHub Desktop
3. เห็นไฟล์ที่เปลี่ยนแปลงอัตโนมัติ
4. Commit และ Push

### การดึงข้อมูลล่าสุด:
```
Repository → Pull (Ctrl + Shift + P)
```

### การสลับ Branch:
```
Current Branch → เลือก branch ที่ต้องการ
```

---

## 🎉 สำเร็จ!

หลังจาก Push แล้ว คุณสามารถ:
- 👀 **ดู code** ได้ที่: https://github.com/neungnuchr-creator/Project_Scoring/tree/Project_score
- 📊 **ดูประวัติ** commits
- 🌿 **จัดการ** branches
- 👥 **แชร์** repository กับทีม

---

**สร้างโดย:** Project Scoring System Team  
**วันที่:** October 2025  
**Repository:** https://github.com/neungnuchr-creator/Project_Scoring

---

## 📞 ต้องการความช่วยเหลือ?

ถ้ามีปัญหาหรือข้อสงสัย:
1. ดูที่ GitHub Desktop Help: `Help → Show Help`
2. อ่าน GitHub Docs: https://docs.github.com/desktop
3. ติดต่อทีม

**Happy Coding! 🚀**

