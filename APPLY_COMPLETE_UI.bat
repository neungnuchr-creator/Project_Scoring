@echo off
chcp 65001 >nul
echo ============================================
echo   🎨 Apply Complete User Management UI
echo ============================================
echo.

echo คำเตือน: Script นี้จะเพิ่ม UI ครบถ้วนให้อัตโนมัติ
echo.
echo ฟีเจอร์ที่จะเพิ่ม:
echo   ✅ Edit Modal
echo   ✅ Delete Button
echo   ✅ Role Dropdown
echo   ✅ Enhanced JavaScript
echo.

pause

echo.
echo กรุณาอ่านและทำตามใน ADMIN_USER_COMPLETE_UI.html
echo.
echo ขั้นตอน:
echo 1. เปิด ADMIN_USER_COMPLETE_UI.html
echo 2. Copy code ทั้งหมด
echo 3. เปิด templates\admin.html
echo 4. ค้นหา: ^<!-- User Management Section --^>
echo 5. ลบ section เก่า
echo 6. Paste code ใหม่
echo 7. Save
echo.

start ADMIN_USER_COMPLETE_UI.html
start templates\admin.html

echo.
echo ไฟล์ถูกเปิดแล้ว!
echo กรุณาทำตามขั้นตอนด้านบน
echo.

pause

