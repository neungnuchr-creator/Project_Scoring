@echo off
echo ========================================
echo   Project Scoring System - Starter
echo ========================================
echo.

REM ตรวจสอบว่ามี Python หรือไม่
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python ไม่ได้ติดตั้งหรือไม่อยู่ใน PATH
    echo กรุณาติดตั้ง Python จาก https://python.org
    pause
    exit /b 1
)

echo [INFO] ตรวจพบ Python แล้ว
python --version
echo.

REM ตรวจสอบว่ามี venv หรือไม่
if not exist "venv" (
    echo [INFO] สร้าง Virtual Environment...
    python -m venv venv
    echo [SUCCESS] สร้าง Virtual Environment เรียบร้อย
    echo.
)

REM Activate venv
echo [INFO] Activating Virtual Environment...
call venv\Scripts\activate.bat

REM ติดตั้ง dependencies
echo [INFO] กำลังติดตั้ง dependencies...
pip install -r requirements.txt
echo.

REM รันโปรแกรม
echo ========================================
echo [SUCCESS] เริ่มต้นเซิร์ฟเวอร์...
echo.
echo เปิดเว็บเบราว์เซอร์ไปที่:
echo   http://localhost:5000
echo   หรือ http://127.0.0.1:5000
echo.
echo กด Ctrl+C เพื่อหยุดเซิร์ฟเวอร์
echo ========================================
echo.

python app.py

pause


