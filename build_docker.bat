@echo off
chcp 65001 >nul
echo ============================================
echo   🐳 Build Docker - Project Scoring System
echo ============================================
echo.

REM ตรวจสอบว่ามี Docker หรือไม่
where docker >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker ยังไม่ได้ติดตั้ง
    echo.
    echo กรุณาติดตั้ง Docker Desktop จาก:
    echo https://www.docker.com/products/docker-desktop/
    echo.
    pause
    exit /b 1
)

echo ✅ พบ Docker แล้ว
docker --version
echo.

REM ล้าง database ก่อน build
echo 📋 ต้องการล้าง database ก่อน build Docker? (y/n)
set /p clear_db="กด y เพื่อล้าง database หรือ n เพื่อข้าม: "

if /i "%clear_db%"=="y" (
    echo.
    echo 🗑️  กำลังล้าง database...
    python clear_database.py
    echo.
)

REM Build Docker image
echo 🔨 กำลัง build Docker image...
echo.
docker build -t project-scoring-system .

if %errorlevel% equ 0 (
    echo.
    echo ============================================
    echo   ✅ Build สำเร็จ!
    echo ============================================
    echo.
    echo 📝 คำสั่งที่ใช้ได้:
    echo.
    echo   1. รัน container:
    echo      docker-compose up
    echo.
    echo   2. รันแบบ background:
    echo      docker-compose up -d
    echo.
    echo   3. หยุด container:
    echo      docker-compose down
    echo.
    echo   4. Export image เป็นไฟล์:
    echo      docker save -o project-scoring-system.tar project-scoring-system
    echo.
    echo ============================================
) else (
    echo.
    echo ❌ Build ไม่สำเร็จ
    echo กรุณาตรวจสอบ error ด้านบนและแก้ไข
    echo.
)

pause

