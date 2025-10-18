# 🚀 เริ่มต้นใช้งานอย่างรวดเร็ว (Quick Start)

## สำหรับ Windows

### วิธีที่ 1: ใช้ไฟล์ START.bat (ง่ายที่สุด) ⭐

1. **Double-click ไฟล์ `START.bat`**
2. **รอจนเซิร์ฟเวอร์เริ่มทำงาน**
3. **เปิดเว็บเบราว์เซอร์ไปที่**: `http://localhost:5000`
4. **เสร็จสิ้น!** ✅

### วิธีที่ 2: ใช้ Command Prompt

```batch
# 1. เปิด Command Prompt ในโฟลเดอร์นี้
# 2. รันคำสั่งต่อไปนี้

# สร้าง Virtual Environment
python -m venv venv

# Activate
venv\Scripts\activate

# ติดตั้ง dependencies
pip install -r requirements.txt

# รันโปรแกรม
python app.py

# 3. เปิดเว็บเบราว์เซอร์ไปที่: http://localhost:5000
```

---

## สำหรับ Mac/Linux

### ขั้นตอนการรัน

```bash
# 1. เปิด Terminal ในโฟลเดอร์นี้
# 2. รันคำสั่งต่อไปนี้

# สร้าง Virtual Environment
python3 -m venv venv

# Activate
source venv/bin/activate

# ติดตั้ง dependencies
pip install -r requirements.txt

# รันโปรแกรม
python app.py

# 3. เปิดเว็บเบราว์เซอร์ไปที่: http://localhost:5000
```

---

## 📋 สิ่งที่ต้องมีก่อนเริ่ม

✅ Python 3.8 หรือสูงกว่า  
✅ เชื่อมต่ออินเทอร์เน็ต (สำหรับติดตั้ง dependencies ครั้งแรก)

---

## 🎯 ทดสอบว่าทำงานหรือไม่

เมื่อโปรแกรมรันแล้ว คุณจะเห็น:

```
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server...
 * Running on http://0.0.0.0:5000
```

เปิดเว็บเบราว์เซอร์แล้วไปที่ `http://localhost:5000` จะเห็นหน้าเว็บพร้อมใช้งาน!

---

## ❓ แก้ไขปัญหาเบื้องต้น

### ปัญหา: "python is not recognized"
**แก้ไข**: ติดตั้ง Python จาก https://python.org และเลือก "Add Python to PATH"

### ปัญหา: "Permission denied" (Mac/Linux)
**แก้ไข**: ใช้ `chmod +x` หรือรันด้วย `sudo`

### ปัญหา: Port 5000 ถูกใช้งานอยู่
**แก้ไข**: 
1. หยุดโปรแกรมที่ใช้ port 5000 อยู่
2. หรือแก้ไขไฟล์ `app.py` บรรทัดสุดท้ายเปลี่ยน port เป็น 8000

---

## 📱 ขั้นตอนถัดไป

หลังจากโปรแกรมรันได้แล้ว:

1. ✅ ลองเพิ่มโครงการทดสอบ
2. ✅ ทดสอบคำนวณคะแนน
3. ✅ ลองแก้ไขและลบโครงการ
4. ✅ ดูสถิติโครงการ
5. 🚀 Deploy ออนไลน์ (ดู DEPLOYMENT_GUIDE.md)

---

**พร้อมใช้งานแล้ว! Have fun! 🎉**



