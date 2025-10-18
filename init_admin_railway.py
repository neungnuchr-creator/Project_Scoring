"""
สคริปต์สำหรับสร้าง Admin user บน Railway
เพิ่ม route /init-admin ชั่วคราว
"""

from app import app, ProjectScoringSystem
from flask import request, jsonify

@app.route('/init-admin', methods=['GET', 'POST'])
def init_admin():
    """
    Route ชั่วคราวสำหรับสร้าง admin user บน Railway
    ⚠️ ลบทิ้งหลังจากสร้าง admin เรียบร้อยแล้ว (เพื่อความปลอดภัย)
    """
    if request.method == 'POST':
        try:
            # สร้าง database และ admin user
            ProjectScoringSystem.init_database()
            return jsonify({
                'success': True,
                'message': 'Admin user created successfully',
                'credentials': {
                    'username': 'admin',
                    'password': 'admin123'
                },
                'warning': '⚠️ Please change admin password after login!'
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    # หน้าเว็บสำหรับสร้าง admin
    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Initialize Admin - Project Scoring System</title>
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    padding: 20px;
                }
                .container {
                    background: white;
                    padding: 40px;
                    border-radius: 20px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    max-width: 500px;
                    width: 100%;
                    text-align: center;
                }
                h1 {
                    color: #333;
                    margin-bottom: 10px;
                    font-size: 28px;
                }
                .subtitle {
                    color: #666;
                    margin-bottom: 30px;
                    font-size: 14px;
                }
                .warning {
                    background: #fff3cd;
                    border: 2px solid #ffc107;
                    color: #856404;
                    padding: 15px;
                    border-radius: 10px;
                    margin-bottom: 30px;
                    font-size: 14px;
                    line-height: 1.6;
                }
                button {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    padding: 15px 40px;
                    font-size: 18px;
                    font-weight: 600;
                    border-radius: 10px;
                    cursor: pointer;
                    transition: all 0.3s;
                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
                }
                button:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
                }
                button:active {
                    transform: translateY(0);
                }
                button:disabled {
                    background: #ccc;
                    cursor: not-allowed;
                    box-shadow: none;
                }
                #result {
                    margin-top: 30px;
                    padding: 20px;
                    border-radius: 10px;
                    display: none;
                }
                .success {
                    background: #d4edda;
                    border: 2px solid #28a745;
                    color: #155724;
                }
                .error {
                    background: #f8d7da;
                    border: 2px solid #dc3545;
                    color: #721c24;
                }
                .credentials {
                    background: #f8f9fa;
                    padding: 15px;
                    border-radius: 8px;
                    margin: 15px 0;
                    font-family: 'Courier New', monospace;
                }
                .credentials div {
                    margin: 8px 0;
                    font-size: 16px;
                }
                .credentials strong {
                    color: #667eea;
                }
                .btn-login {
                    display: inline-block;
                    background: #28a745;
                    color: white;
                    padding: 12px 30px;
                    text-decoration: none;
                    border-radius: 8px;
                    margin-top: 15px;
                    font-weight: 600;
                    transition: all 0.3s;
                }
                .btn-login:hover {
                    background: #218838;
                    transform: translateY(-2px);
                }
                .spinner {
                    border: 3px solid #f3f3f3;
                    border-top: 3px solid #667eea;
                    border-radius: 50%;
                    width: 40px;
                    height: 40px;
                    animation: spin 1s linear infinite;
                    margin: 20px auto;
                    display: none;
                }
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚂 Initialize Admin User</h1>
                <p class="subtitle">Project Scoring System - Railway Deployment</p>
                
                <div class="warning">
                    ⚠️ <strong>Warning:</strong><br>
                    This will create/reset the database and create a default admin user.<br>
                    <strong>Delete this route after initialization!</strong>
                </div>
                
                <button id="initBtn" onclick="initAdmin()">
                    🔐 Create Admin User
                </button>
                
                <div class="spinner" id="spinner"></div>
                
                <div id="result"></div>
            </div>
            
            <script>
                async function initAdmin() {
                    const btn = document.getElementById('initBtn');
                    const spinner = document.getElementById('spinner');
                    const result = document.getElementById('result');
                    
                    // Disable button and show spinner
                    btn.disabled = true;
                    btn.textContent = 'Creating...';
                    spinner.style.display = 'block';
                    result.style.display = 'none';
                    
                    try {
                        const response = await fetch('/init-admin', { 
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            }
                        });
                        
                        const data = await response.json();
                        
                        spinner.style.display = 'none';
                        result.style.display = 'block';
                        
                        if (data.success) {
                            result.className = 'success';
                            result.innerHTML = `
                                <h2>✅ Success!</h2>
                                <div class="credentials">
                                    <div><strong>Username:</strong> ${data.credentials.username}</div>
                                    <div><strong>Password:</strong> ${data.credentials.password}</div>
                                </div>
                                <div style="color: #dc3545; font-weight: 600; margin: 15px 0;">
                                    ${data.warning}
                                </div>
                                <a href="/login" class="btn-login">
                                    🚀 Go to Login
                                </a>
                                <div style="margin-top: 20px; font-size: 12px; color: #666;">
                                    <strong>Next steps:</strong><br>
                                    1. Login with admin credentials<br>
                                    2. Change admin password<br>
                                    3. Delete /init-admin route from code<br>
                                    4. Redeploy to Railway
                                </div>
                            `;
                        } else {
                            result.className = 'error';
                            result.innerHTML = `
                                <h2>❌ Error</h2>
                                <p>${data.error}</p>
                            `;
                            btn.disabled = false;
                            btn.textContent = '🔐 Create Admin User';
                        }
                    } catch (error) {
                        spinner.style.display = 'none';
                        result.style.display = 'block';
                        result.className = 'error';
                        result.innerHTML = `
                            <h2>❌ Error</h2>
                            <p>${error.message}</p>
                        `;
                        btn.disabled = false;
                        btn.textContent = '🔐 Create Admin User';
                    }
                }
            </script>
        </body>
        </html>
    '''

if __name__ == '__main__':
    print("=" * 50)
    print("⚠️  WARNING:")
    print("This script adds /init-admin route to your app.")
    print("Use it only for initial deployment.")
    print("DELETE this route after creating admin user!")
    print("=" * 50)
    print("")
    print("To use:")
    print("1. Import this in app.py:")
    print("   from init_admin_railway import init_admin")
    print("")
    print("2. Deploy to Railway")
    print("")
    print("3. Visit: https://your-app.up.railway.app/init-admin")
    print("")
    print("4. Click 'Create Admin User'")
    print("")
    print("5. Remove the import and redeploy!")
    print("=" * 50)

