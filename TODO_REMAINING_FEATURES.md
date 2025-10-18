# 📋 ฟีเจอร์ที่เหลือต้องทำ

## ✅ สิ่งที่ทำเสร็จแล้ว:

1. ✅ Database migration (เพิ่ม email, approved columns)
2. ✅ Login ด้วย Email แทน Username
3. ✅ Email validation (@g-able.com)
4. ✅ User approval system  
5. ✅ Admin Dashboard มี User Management UI
6. ✅ API approve/reject users
7. ✅ ติดตั้ง Flask-Mail

---

## 🔄 สิ่งที่ต้องทำต่อ:

### 1. **Email Notification เมื่อมี User สมัครใหม่** 📧

**ต้องทำ:**
- เพิ่ม Flask-Mail configuration ใน app.py
- สร้าง function send_email_notification()
- ส่งอีเมลไป neungnuch.r@g-able.com เมื่อมี user สมัครใหม่
- Template email สวยงาม

**ไฟล์ที่ต้องแก้:**
- `app.py` - เพิ่ม Mail config และ function
- `.env.example` - เพิ่ม SMTP settings

**Code ตัวอย่าง:**
```python
from flask_mail import Mail, Message

# Config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = 'noreply@g-able.com'

mail = Mail(app)

def send_new_user_notification(user_data):
    msg = Message(
        '🔔 มีผู้ใช้สมัครสมาชิกใหม่',
        recipients=['neungnuch.r@g-able.com']
    )
    msg.body = f"""
    มีผู้ใช้สมัครสมาชิกใหม่ในระบบ Project Scoring:
    
    ชื่อ: {user_data['first_name']} {user_data['last_name']}
    Email: {user_data['email']}
    รหัสพนักงาน: {user_data['employee_id']}
    
    กรุณาเข้าสู่ระบบเพื่ออนุมัติ:
    https://your-app.up.railway.app/admin
    """
    mail.send(msg)

# ใน api_register():
if user_id:
    send_new_user_notification(data)
    return jsonify({'success': True, 'message': '...'})
```

---

### 2. **หน้าจัดการสมาชิก (Edit/Delete)** 👥

**ต้องทำ:**
- เพิ่มปุ่ม "✏️ แก้ไข" ในตาราง users
- สร้าง Modal/Form สำหรับแก้ไขข้อมูล user
- API PUT `/api/admin/users/<id>` - แก้ไขข้อมูล
- API DELETE `/api/admin/users/<id>` - ลบ user
- UI สวยงามพร้อม validation

**ไฟล์ที่ต้องแก้:**
- `app.py` - เพิ่ม API endpoints
- `templates/admin.html` - เพิ่ม Edit Modal และ functions

**Features:**
- แก้ไข: ชื่อ, นามสกุล, รหัสพนักงาน, email
- ลบ user พร้อมยืนยัน 2 ชั้น
- Validation ครบถ้วน

---

### 3. **หน้า Admin Detail/Settings** ⚙️

**ต้องทำ:**
- สร้างหน้า `/admin/settings`
- แสดงข้อมูล admin profile
- เปลี่ยนรหัสผ่านผ่านหน้าเว็บ
- แก้ไขข้อมูลส่วนตัว
- System settings

**ไฟล์ที่ต้องสร้าง:**
- `templates/admin_settings.html` - หน้าตั้งค่า
- API สำหรับแก้ไขข้อมูล

**Features:**
- Profile management
- Change password form
- Email preferences
- System settings

---

### 4. **Role Management** 👑

**ต้องทำ:**
- หน้า `/admin/roles` หรือ tab ใน settings
- แสดงรายการ users ทั้งหมด
- Dropdown เลือก role (employee/admin)
- API POST `/api/admin/users/<id>/change-role`
- Confirmation สำหรับเปลี่ยน role

**ไฟล์ที่ต้องแก้:**
- `app.py` - เพิ่ม API change role
- `templates/admin.html` - เพิ่ม role column และ dropdown
- หรือสร้างหน้าแยก `templates/admin_roles.html`

**Features:**
- เปลี่ยน employee → admin
- เปลี่ยน admin → employee
- ป้องกันการลบ admin คนสุดท้าย
- Audit log (optional)

---

## 📁 โครงสร้างไฟล์ที่ต้องสร้าง/แก้:

```
project-scoring-system/
├── app.py                              # เพิ่ม Mail config + APIs
├── templates/
│   ├── admin.html                      # เพิ่ม Edit Modal + Role dropdown
│   ├── admin_settings.html             # ใหม่ - Admin settings page
│   └── email_new_user_notification.html # ใหม่ - Email template
├── .env.example                        # เพิ่ม SMTP settings
└── FEATURE_IMPLEMENTATION_GUIDE.md     # คู่มือนี้
```

---

## 🔧 ขั้นตอนการทำ (แนะนำ):

### **Phase 1: Email Notification** (30 นาที)
1. Config Flask-Mail
2. สร้าง email template
3. เพิ่มใน api_register()
4. ทดสอบส่ง email

### **Phase 2: User Edit/Delete** (45 นาที)
1. สร้าง Edit Modal UI
2. เพิ่ม API PUT/DELETE
3. JavaScript functions
4. ทดสอบ

### **Phase 3: Admin Settings** (30 นาที)
1. สร้างหน้า admin_settings.html
2. Form เปลี่ยนรหัสผ่าน
3. Profile edit
4. Route และ API

### **Phase 4: Role Management** (45 นาที)
1. เพิ่ม role column ในตาราง
2. Dropdown เลือก role
3. API change-role
4. Validation และ testing

**รวมเวลา:** ~2.5 ชั่วโมง

---

## 💡 Tips การทำ:

### **สำหรับ Email Notification:**

**ใช้ Gmail SMTP (ง่ายที่สุด):**
```python
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'your-email@gmail.com'
MAIL_PASSWORD = 'your-app-password'  # ต้องสร้าง App Password
```

**สร้าง Gmail App Password:**
1. ไปที่ Google Account Settings
2. Security → 2-Step Verification
3. App passwords → Generate
4. Copy password ใส่ใน .env

**หรือใช้ Railway Variables:**
- ตั้งค่าใน Railway Dashboard → Variables

---

### **สำหรับ User Edit:**

**Modal Pattern:**
```html
<div id="editUserModal" class="modal">
    <div class="modal-content">
        <h2>แก้ไขข้อมูล User</h2>
        <form id="editUserForm">
            <input type="hidden" id="editUserId">
            <input type="text" id="editFirstName">
            <input type="text" id="editLastName">
            <input type="email" id="editEmail">
            <!-- ... -->
            <button type="submit">บันทึก</button>
        </form>
    </div>
</div>
```

**API:**
```python
@app.route('/api/admin/users/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    data = request.json
    conn = ProjectScoringSystem.get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE users 
        SET first_name=?, last_name=?, email=?, employee_id=?
        WHERE id=?
    ''', (data['first_name'], data['last_name'], 
          data['email'], data['employee_id'], user_id))
    
    conn.commit()
    conn.close()
    return jsonify({'success': True})
```

---

### **สำหรับ Role Management:**

**Dropdown in Table:**
```html
<select onchange="changeUserRole(${user.id}, this.value)">
    <option value="employee" ${user.role === 'employee' ? 'selected' : ''}>
        Employee
    </option>
    <option value="admin" ${user.role === 'admin' ? 'selected' : ''}>
        Admin
    </option>
</select>
```

**API:**
```python
@app.route('/api/admin/users/<int:user_id>/change-role', methods=['POST'])
@admin_required
def change_user_role(user_id):
    data = request.json
    new_role = data['role']
    
    # Validation
    if new_role not in ['employee', 'admin']:
        return jsonify({'error': 'Invalid role'}), 400
    
    # ป้องกันการลบ admin คนสุดท้าย
    if new_role == 'employee':
        cursor.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
        admin_count = cursor.fetchone()[0]
        if admin_count <= 1:
            return jsonify({'error': 'ต้องมี admin อย่างน้อย 1 คน'}), 400
    
    cursor.execute("UPDATE users SET role=? WHERE id=?", (new_role, user_id))
    conn.commit()
    return jsonify({'success': True})
```

---

## 📚 เอกสารเพิ่มเติม:

- Flask-Mail Docs: https://flask-mail.readthedocs.io/
- Gmail SMTP: https://support.google.com/mail/answer/7126229
- Modal UI: Bootstrap หรือ custom CSS

---

## 🆘 ต้องการความช่วยเหลือ?

ถ้าต้องการให้ช่วยทำฟีเจอร์เหล่านี้ บอกได้เลยครับ!

**ฟีเจอร์ไหนที่ต้องการให้ทำก่อน?**
1. Email Notification
2. User Edit/Delete  
3. Admin Settings
4. Role Management

---

**Status:** 🔄 In Progress  
**Created:** October 18, 2025  
**Priority:** High

