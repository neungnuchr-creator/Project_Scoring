@echo off
chcp 65001 >nul
echo ============================================
echo   🚂 Deploy to Railway.app
echo ============================================
echo.

REM ตรวจสอบว่ามี git หรือไม่
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git ยังไม่ได้ติดตั้ง
    echo.
    echo กรุณาติดตั้ง Git จาก:
    echo https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo ✅ พบ Git แล้ว
git --version
echo.

REM แสดงสถานะ Git
echo 📋 สถานะ Git:
echo.
git status --short
echo.

REM ถาม user ว่าต้องการ commit หรือไม่
echo 💾 ต้องการ commit และ push ไป GitHub? (y/n)
set /p do_commit="กด y เพื่อดำเนินการ หรือ n เพื่อข้าม: "

if /i "%do_commit%"=="y" (
    echo.
    echo 📝 กรอก Commit Message:
    set /p commit_msg="Message: "
    
    if "%commit_msg%"=="" (
        set commit_msg=Update deployment configuration
    )
    
    echo.
    echo 🔨 กำลัง commit...
    git add .
    git commit -m "%commit_msg%"
    
    if %errorlevel% equ 0 (
        echo ✅ Commit สำเร็จ
        echo.
        echo 📤 กำลัง push ไป GitHub...
        git push origin main
        
        if %errorlevel% equ 0 (
            echo.
            echo ============================================
            echo   ✅ Push สำเร็จ!
            echo ============================================
            echo.
            echo 🚂 ขั้นตอนต่อไป:
            echo.
            echo   1. เปิด Railway Dashboard:
            echo      https://railway.app/dashboard
            echo.
            echo   2. Railway จะ deploy อัตโนมัติ (ถ้าเปิด Auto-Deploy)
            echo.
            echo   3. รอ 2-5 นาที
            echo.
            echo   4. ตรวจสอบ:
            echo      - View Logs
            echo      - ดูว่า deploy สำเร็จ
            echo      - เปิดเว็บทดสอบ
            echo.
            echo ============================================
        ) else (
            echo.
            echo ❌ Push ไม่สำเร็จ
            echo กรุณาตรวจสอบ:
            echo   - Git remote ตั้งค่าถูกต้องหรือไม่
            echo   - มี permission ในการ push หรือไม่
            echo.
        )
    ) else (
        echo.
        echo ⚠️  ไม่มีการเปลี่ยนแปลง หรือ commit ไม่สำเร็จ
        echo.
    )
) else (
    echo.
    echo ⏭️  ข้ามการ commit
    echo.
)

echo.
echo 📚 คู่มือเพิ่มเติม:
echo    - RAILWAY_DEPLOY_GUIDE.md
echo.
echo 🔑 ต้องตั้งค่าใน Railway:
echo    SECRET_KEY=your-secret-key
echo    DATABASE_PATH=project_scoring.db
echo.

pause

