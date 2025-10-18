@echo off
chcp 65001 >nul
echo ============================================
echo   📦 Export Docker Image
echo ============================================
echo.

REM ตรวจสอบว่ามี Docker หรือไม่
where docker >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker ยังไม่ได้ติดตั้ง
    pause
    exit /b 1
)

echo ✅ พบ Docker แล้ว
echo.

REM Build Docker image
echo 🔨 กำลัง build Docker image...
docker build -t project-scoring-system .

if %errorlevel% neq 0 (
    echo ❌ Build ไม่สำเร็จ
    pause
    exit /b 1
)

echo ✅ Build สำเร็จ
echo.

REM Export Docker image
echo 📦 กำลัง export Docker image เป็นไฟล์...
docker save -o project-scoring-system.tar project-scoring-system

if %errorlevel% equ 0 (
    echo.
    echo ============================================
    echo   ✅ Export สำเร็จ!
    echo ============================================
    echo.
    echo 📁 ไฟล์ที่สร้าง:
    echo    - project-scoring-system.tar
    echo.
    echo 📊 ขนาดไฟล์:
    for %%F in (project-scoring-system.tar) do echo    - %%~zF bytes (%%~zF / 1048576 MB)
    echo.
    echo 📤 วิธีส่งให้เพื่อน:
    echo    1. ส่งไฟล์: project-scoring-system.tar
    echo    2. ส่งไฟล์: README_DOCKER.md
    echo.
    echo 📝 เพื่อนใช้คำสั่งนี้เพื่อ load:
    echo    docker load -i project-scoring-system.tar
    echo    docker run -d -p 5000:5000 project-scoring-system
    echo.
    echo ============================================
) else (
    echo ❌ Export ไม่สำเร็จ
)

pause

