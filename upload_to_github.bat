@echo off
chcp 65001 >nul
echo ============================================
echo   📦 Upload to GitHub - Project Scoring
echo ============================================
echo.

REM ตรวจสอบว่ามี Git หรือไม่
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git ยังไม่ได้ติดตั้ง
    echo.
    echo กรุณาติดตั้ง Git for Windows จาก:
    echo https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo ✅ พบ Git แล้ว
echo.

REM ตรวจสอบว่ามี .git หรือไม่
if not exist ".git" (
    echo 📁 สร้าง Git repository...
    git init
    git remote add origin https://github.com/neungnuchr-creator/Project_Scoring.git
    git checkout -b Project_score
    echo ✅ สร้าง repository เรียบร้อย
    echo.
)

REM แสดงสถานะ
echo 📊 สถานะไฟล์:
git status
echo.

REM ถามว่าต้องการดำเนินการต่อหรือไม่
set /p continue="ต้องการ commit และ push ไปยัง GitHub? (y/n): "
if /i not "%continue%"=="y" (
    echo ❌ ยกเลิกการอัปโหลด
    pause
    exit /b 0
)

REM เพิ่มไฟล์ทั้งหมด
echo.
echo 📦 เพิ่มไฟล์ทั้งหมด...
git add .

REM สร้าง commit
echo.
set /p message="กรอก commit message (Enter = ใช้ค่า default): "
if "%message%"=="" set message=Update Project Scoring System - %date% %time%

git commit -m "%message%"
echo ✅ Commit เรียบร้อย
echo.

REM Push ไปยัง GitHub
echo 🚀 กำลัง push ไปยัง GitHub...
echo.
git push -u origin Project_score

if %errorlevel% equ 0 (
    echo.
    echo ============================================
    echo   ✅ อัปโหลดสำเร็จ!
    echo ============================================
    echo.
    echo ตรวจสอบได้ที่:
    echo https://github.com/neungnuchr-creator/Project_Scoring/tree/Project_score
    echo.
) else (
    echo.
    echo ============================================
    echo   ❌ อัปโหลดไม่สำเร็จ
    echo ============================================
    echo.
    echo เคล็ดลับ:
    echo - ตรวจสอบว่าได้ login GitHub แล้วหรือไม่
    echo - อาจต้องใช้ Personal Access Token แทน password
    echo - ดูวิธีแก้ไขใน UPLOAD_TO_GITHUB.md
    echo.
)

pause

