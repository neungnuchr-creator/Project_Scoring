# 🚀 คู่มือการ Deploy ระบบจัดเก็บและคำนวณคะแนนโครงการ

คู่มือนี้จะแนะนำวิธีการ deploy โปรแกรมไปยัง hosting platforms ต่างๆ แบบละเอียด

## 📑 สารบัญ

1. [Deploy บน Render (แนะนำ - ฟรี)](#1-deploy-บน-render-ฟรี-แนะนำ)
2. [Deploy บน PythonAnywhere (ฟรี)](#2-deploy-บน-pythonanywhere-ฟรี)
3. [Deploy บน Railway (ฟรีจำกัด)](#3-deploy-บน-railway-ฟรีจำกัด)
4. [Deploy บน Heroku (มีค่าใช้จ่าย)](#4-deploy-บน-heroku)
5. [Deploy บน VPS/Server ของตัวเอง](#5-deploy-บน-vpsserver-ของตัวเอง)

---

## 1. Deploy บน Render (ฟรี, แนะนำ)

Render เป็น platform ที่ใช้งานง่ายและมี free tier ที่ดี

### ขั้นตอนที่ 1: เตรียมโค้ด

1. **สร้าง GitHub Repository**
   - ไปที่ https://github.com
   - คลิก "New repository"
   - ตั้งชื่อ เช่น "project-scoring-system"
   - เลือก Public หรือ Private
   - คลิก "Create repository"

2. **Upload โค้ดขึ้น GitHub**
   ```bash
   # เปิด Command Prompt ในโฟลเดอร์โปรเจกต์
   cd C:\Users\User\project-scoring-system
   
   # Initialize git
   git init
   
   # Add all files
   git add .
   
   # Commit
   git commit -m "Initial commit"
   
   # Add remote repository (เปลี่ยน URL เป็นของคุณ)
   git remote add origin https://github.com/your-username/project-scoring-system.git
   
   # Push to GitHub
   git branch -M main
   git push -u origin main
   ```

### ขั้นตอนที่ 2: Deploy บน Render

1. **สร้างบัญชี Render**
   - ไปที่ https://render.com
   - คลิก "Get Started for Free"
   - สมัครด้วย GitHub account

2. **สร้าง Web Service ใหม่**
   - คลิก "New +" → "Web Service"
   - เชื่อมต่อ GitHub repository ของคุณ
   - เลือก repository "project-scoring-system"

3. **ตั้งค่า Web Service**
   - **Name**: project-scoring-system (หรือชื่ออื่นที่ต้องการ)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

4. **คลิก "Create Web Service"**
   - รอ 5-10 นาที Render จะ deploy ให้อัตโนมัติ
   - เมื่อเสร็จจะได้ URL เช่น: `https://project-scoring-system.onrender.com`

5. **เปิดใช้งาน**
   - คลิกที่ URL ที่ได้
   - เว็บจะทำงาน!

### ⚠️ หมายเหตุสำคัญ (Render Free Tier)
- Web service จะ "หลับ" หลังไม่มีการใช้งาน 15 นาที
- ครั้งแรกที่เข้าหลังจากหลับจะใช้เวลา 30-60 วินาที
- Database จะรีเซ็ตทุกครั้งที่ deploy ใหม่ (ใช้ free disk)

---

## 2. Deploy บน PythonAnywhere (ฟรี)

PythonAnywhere เหมาะสำหรับ Python web apps และมี free tier

### ขั้นตอนที่ 1: สร้างบัญชี

1. ไปที่ https://www.pythonanywhere.com
2. คลิก "Start running Python online in less than a minute"
3. สร้าง Beginner account (ฟรี)

### ขั้นตอนที่ 2: Upload ไฟล์

1. **คลิกที่ "Files"**
2. **สร้างโฟลเดอร์ใหม่**: `project-scoring-system`
3. **Upload ไฟล์ทั้งหมด**:
   - app.py
   - requirements.txt
   - templates/index.html
   - .gitignore

### ขั้นตอนที่ 3: ติดตั้ง Dependencies

1. **คลิกที่ "Consoles"**
2. **เปิด Bash console**
3. **รันคำสั่ง**:
   ```bash
   cd project-scoring-system
   pip3 install --user -r requirements.txt
   ```

### ขั้นตอนที่ 4: ตั้งค่า Web App

1. **คลิกที่ "Web"**
2. **คลิก "Add a new web app"**
3. **เลือก "Manual configuration"**
4. **เลือก Python 3.10**

5. **ตั้งค่า WSGI file**:
   - คลิกที่ลิงก์ "WSGI configuration file"
   - ลบโค้ดทั้งหมด
   - ใส่โค้ดนี้:
   ```python
   import sys
   path = '/home/yourusername/project-scoring-system'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```
   - **เปลี่ยน `yourusername`** เป็น username ของคุณ
   - คลิก "Save"

6. **ตั้งค่า Static files**:
   - URL: `/static/`
   - Directory: `/home/yourusername/project-scoring-system/static/`

7. **Reload web app**:
   - กลับไปที่ "Web" tab
   - คลิกปุ่ม "Reload"

8. **เปิดใช้งาน**:
   - URL จะเป็น: `https://yourusername.pythonanywhere.com`

### ⚠️ หมายเหตุ (PythonAnywhere Free Tier)
- รองรับ traffic จำกัด
- ต้อง log in ทุก 3 เดือนเพื่อรักษาบัญชี
- ไม่สามารถใช้ custom domain (Free tier)

---

## 3. Deploy บน Railway (ฟรีจำกัด)

Railway ให้ $5 free credit ต่อเดือน

### ขั้นตอนการ Deploy

1. **สร้างบัญชี**
   - ไปที่ https://railway.app
   - Sign up ด้วย GitHub

2. **Create New Project**
   - คลิก "New Project"
   - เลือก "Deploy from GitHub repo"
   - เลือก repository ของคุณ

3. **ตั้งค่า**
   - Railway จะ detect Python project อัตโนมัติ
   - กด "Deploy Now"

4. **เพิ่ม Domain**
   - ไปที่ Settings
   - Generate Domain
   - จะได้ URL เช่น: `https://project-scoring-system.up.railway.app`

5. **เสร็จสิ้น** - เว็บพร้อมใช้งาน!

---

## 4. Deploy บน Heroku

**หมายเหตุ**: Heroku ยกเลิก free tier แล้ว ต้องมีบัตรเครดิต

### ขั้นตอนการ Deploy

1. **ติดตั้ง Heroku CLI**
   - ดาวน์โหลดจาก: https://devcenter.heroku.com/articles/heroku-cli
   - ติดตั้งตามขั้นตอน

2. **Login**
   ```bash
   heroku login
   ```

3. **สร้าง Heroku App**
   ```bash
   cd C:\Users\User\project-scoring-system
   heroku create project-scoring-system
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **เปิดเว็บ**
   ```bash
   heroku open
   ```

---

## 5. Deploy บน VPS/Server ของตัวเอง

สำหรับผู้ที่มี VPS (Digital Ocean, Linode, AWS EC2 ฯลฯ)

### ขั้นตอนการติดตั้ง (Ubuntu)

1. **เชื่อมต่อ SSH**
   ```bash
   ssh user@your-server-ip
   ```

2. **ติดตั้ง Python และ Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv nginx
   ```

3. **Clone โปรเจกต์**
   ```bash
   cd /var/www
   git clone https://github.com/your-username/project-scoring-system.git
   cd project-scoring-system
   ```

4. **สร้าง Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **ติดตั้ง Gunicorn**
   ```bash
   pip install gunicorn
   ```

6. **สร้าง Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/project-scoring.service
   ```
   
   ใส่:
   ```ini
   [Unit]
   Description=Project Scoring System
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/var/www/project-scoring-system
   Environment="PATH=/var/www/project-scoring-system/venv/bin"
   ExecStart=/var/www/project-scoring-system/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 app:app

   [Install]
   WantedBy=multi-user.target
   ```

7. **เปิดใช้งาน Service**
   ```bash
   sudo systemctl start project-scoring
   sudo systemctl enable project-scoring
   ```

8. **ตั้งค่า Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/project-scoring
   ```
   
   ใส่:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

9. **Enable Site**
   ```bash
   sudo ln -s /etc/nginx/sites-available/project-scoring /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

10. **เปิด Firewall**
    ```bash
    sudo ufw allow 80
    sudo ufw allow 443
    ```

11. **ติดตั้ง SSL (Optional แต่แนะนำ)**
    ```bash
    sudo apt install certbot python3-certbot-nginx
    sudo certbot --nginx -d your-domain.com
    ```

---

## 📝 Checklist ก่อน Deploy

- [ ] ทดสอบโปรแกรมใน local แล้ว
- [ ] ตรวจสอบว่า requirements.txt มี dependencies ครบ
- [ ] เปลี่ยน `debug=True` เป็น `debug=False` ใน app.py
- [ ] เปลี่ยน `SECRET_KEY` เป็นค่าที่ปลอดภัย
- [ ] ทดสอบ API endpoints ทั้งหมด
- [ ] เตรียม .gitignore ไม่ให้ push database และ sensitive files
- [ ] สำรองข้อมูล database (ถ้ามี)

---

## 🔧 การแก้ไขปัญหาที่พบบ่อย

### ปัญหา: Application Error หลัง Deploy

**แก้ไข**:
1. ตรวจสอบ logs:
   ```bash
   # Render/Railway: ดูที่ Dashboard → Logs
   # Heroku: heroku logs --tail
   ```
2. ตรวจสอบว่าติดตั้ง dependencies ครบ
3. ตรวจสอบ Python version ใน runtime.txt

### ปัญหา: Database ไม่ทำงาน

**แก้ไข**:
- ตรวจสอบว่าโฟลเดอร์มีสิทธิ์เขียนไฟล์
- ใช้ environment variable สำหรับ database path
- พิจารณาใช้ PostgreSQL สำหรับ production

### ปัญหา: Static files ไม่โหลด

**แก้ไข**:
1. ตรวจสอบ path ใน templates
2. ตั้งค่า static files ใน hosting platform
3. ใช้ CDN สำหรับ static files

---

## 🌟 Best Practices

1. **ใช้ Environment Variables**
   - เก็บ SECRET_KEY, DATABASE_URL ใน environment variables
   - ไม่ hard-code sensitive data

2. **ใช้ Production-ready Database**
   - PostgreSQL สำหรับ production
   - SQLite เหมาะสำหรับ development เท่านั้น

3. **Enable HTTPS**
   - ใช้ Let's Encrypt สำหรับ SSL certificate ฟรี
   - บังคับให้ใช้ HTTPS

4. **Monitor และ Log**
   - ติดตั้ง monitoring tools
   - เก็บ logs สำหรับ debugging

5. **Backup ข้อมูล**
   - สำรอง database เป็นประจำ
   - มี disaster recovery plan

---

## 📚 แหล่งข้อมูลเพิ่มเติม

- [Flask Deployment Documentation](https://flask.palletsprojects.com/en/latest/deploying/)
- [Render Documentation](https://render.com/docs)
- [PythonAnywhere Help](https://help.pythonanywhere.com/)
- [Railway Documentation](https://docs.railway.app/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

---

## ❓ คำถามที่พบบ่อย (FAQ)

**Q: ควรเลือก hosting แบบไหน?**
A: สำหรับเริ่มต้น แนะนำ Render (ฟรี, ใช้งานง่าย)

**Q: Database จะหายไหมถ้า deploy ใหม่?**
A: ใช่ ถ้าใช้ free tier ของ Render ควรใช้ external database

**Q: ทำไม web ช้า?**
A: Free tier มักจะ "หลับ" เมื่อไม่มีการใช้งาน ควร upgrade เป็น paid plan

**Q: ต้องมีบัตรเครดิตไหม?**
A: Render และ PythonAnywhere ไม่ต้องมีบัตรเครดิตสำหรับ free tier

---

**สร้างด้วย ❤️ | Happy Deploying! 🚀**


