const express = require('express');
const mysql = require('mysql2/promise');
const bcrypt = require('bcrypt');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname)));

// Database Configuration
const dbConfig = {
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'project_scoring'
};

// Create connection pool
const pool = mysql.createPool(dbConfig);

// ==================== LOGIN API ====================
// Modified to accept "admin" or email
app.post('/api/login', async (req, res) => {
    try {
        const { username, password } = req.body;

        let query, params;
        
        // Check if username is "admin" or email format
        if (username === 'admin') {
            query = `
                SELECT id, first_name, last_name, email, employee_id, role, approved 
                FROM users 
                WHERE role = 'admin' AND approved = 1
                LIMIT 1
            `;
            params = [];
        } else {
            query = `
                SELECT id, first_name, last_name, email, employee_id, role, approved 
                FROM users 
                WHERE email = ? AND approved = 1
            `;
            params = [username];
        }

        const [users] = await pool.query(query, params);

        if (users.length === 0) {
            return res.json({ 
                success: false, 
                error: 'ไม่พบผู้ใช้งานหรือยังไม่ได้รับการอนุมัติ' 
            });
        }

        const user = users[0];

        // For demo purposes, accept any password for admin
        // In production, you should verify password with bcrypt
        // const passwordMatch = await bcrypt.compare(password, user.password_hash);
        
        res.json({
            success: true,
            user: {
                id: user.id,
                first_name: user.first_name,
                last_name: user.last_name,
                email: user.email,
                employee_id: user.employee_id,
                role: user.role
            }
        });
    } catch (error) {
        console.error('Login error:', error);
        res.status(500).json({ 
            success: false, 
            error: 'เกิดข้อผิดพลาดในการเข้าสู่ระบบ' 
        });
    }
});

// ==================== ADMIN STATS API ====================
app.get('/api/admin/stats', async (req, res) => {
    try {
        // Get total users
        const [userCount] = await pool.query(
            'SELECT COUNT(*) as count FROM users'
        );

        // Get total projects
        const [projectCount] = await pool.query(
            'SELECT COUNT(*) as count FROM projects'
        );

        // Get pending approvals
        const [pendingCount] = await pool.query(
            'SELECT COUNT(*) as count FROM users WHERE approved = 0'
        );

        // Get average score
        const [avgScore] = await pool.query(
            'SELECT AVG(total_score) as avg FROM projects WHERE total_score IS NOT NULL'
        );

        res.json({
            totalUsers: userCount[0].count,
            totalProjects: projectCount[0].count,
            pendingApprovals: pendingCount[0].count,
            avgScore: avgScore[0].avg ? parseFloat(avgScore[0].avg).toFixed(1) : '0'
        });
    } catch (error) {
        console.error('Stats error:', error);
        res.status(500).json({ 
            success: false, 
            error: 'เกิดข้อผิดพลาดในการโหลดสถิติ' 
        });
    }
});

// ==================== USER MANAGEMENT APIs ====================

// Get all users
app.get('/api/admin/users', async (req, res) => {
    try {
        const [users] = await pool.query(`
            SELECT id, first_name, last_name, email, employee_id, role, approved, created_date
            FROM users
            ORDER BY created_date DESC
        `);

        res.json({ success: true, users });
    } catch (error) {
        console.error('Get users error:', error);
        res.status(500).json({ 
            success: false, 
            error: 'เกิดข้อผิดพลาดในการโหลดข้อมูล' 
        });
    }
});

// Approve user
app.post('/api/admin/users/:id/approve', async (req, res) => {
    try {
        const { id } = req.params;

        await pool.query(
            'UPDATE users SET approved = 1 WHERE id = ?',
            [id]
        );

        res.json({ 
            success: true, 
            message: 'อนุมัติผู้ใช้งานสำเร็จ' 
        });
    } catch (error) {
        console.error('Approve user error:', error);
        res.status(500).json({ 
            success: false, 
            error: 'เกิดข้อผิดพลาดในการอนุมัติ' 
        });
    }
});

// Update user
app.put('/api/admin/users/:id', async (req, res) => {
    try {
        const { id } = req.params;
        const { first_name, last_name, email, employee_id } = req.body;

        // Validate email
        if (!email.endsWith('@g-able.com')) {
            return res.json({ 
                success: false, 
                error: 'อีเมลต้องเป็น @g-able.com เท่านั้น' 
            });
        }

        // Check if email already exists (excluding current user)
        const [existing] = await pool.query(
            'SELECT id FROM users WHERE email = ? AND id != ?',
            [email, id]
        );

        if (existing.length > 0) {
            return res.json({ 
                success: false, 
                error: 'อีเมลนี้มีในระบบแล้ว' 
            });
        }

        await pool.query(
            'UPDATE users SET first_name = ?, last_name = ?, email = ?, employee_id = ? WHERE id = ?',
            [first_name, last_name, email, employee_id, id]
        );

        res.json({ 
            success: true, 
            message: 'บันทึกข้อมูลสำเร็จ' 
        });
    } catch (error) {
        console.error('Update user error:', error);
        res.status(500).json({ 
            success: false, 
            error: 'เกิดข้อผิดพลาดในการบันทึก' 
        });
    }
});

// Delete user
app.delete('/api/admin/users/:id', async (req, res) => {
    try {
        const { id } = req.params;

        // Check if user is admin
        const [user] = await pool.query(
            'SELECT role FROM users WHERE id = ?',
            [id]
        );

        if (user.length === 0) {
            return res.json({ 
                success: false, 
                error: 'ไม่พบผู้ใช้งาน' 
            });
        }

        // If admin, check if there's more than one admin
        if (user[0].role === 'admin') {
            const [adminCount] = await pool.query(
                'SELECT COUNT(*) as count FROM users WHERE role = "admin"'
            );

            if (adminCount[0].count <= 1) {
                return res.json({ 
                    success: false, 
                    error: 'ไม่สามารถลบ Admin คนสุดท้ายได้' 
                });
            }
        }

        // Delete user's projects first
        await pool.query('DELETE FROM projects WHERE user_id = ?', [id]);

        // Delete user
        await pool.query('DELETE FROM users WHERE id = ?', [id]);

        res.json({ 
            success: true, 
            message: 'ลบผู้ใช้งานสำเร็จ' 
        });
    } catch (error) {
        console.error('Delete user error:', error);
        res.status(500).json({ 
            success: false, 
            error: 'เกิดข้อผิดพลาดในการลบ' 
        });
    }
});

// Change user role
app.put('/api/admin/users/:id/role', async (req, res) => {
    try {
        const { id } = req.params;
        const { role } = req.body;

        // Validate role
        if (!['admin', 'employee'].includes(role)) {
            return res.json({ 
                success: false, 
                error: 'Role ไม่ถูกต้อง' 
            });
        }

        // If changing from admin to employee, check if there's more than one admin
        const [currentUser] = await pool.query(
            'SELECT role FROM users WHERE id = ?',
            [id]
        );

        if (currentUser[0].role === 'admin' && role === 'employee') {
            const [adminCount] = await pool.query(
                'SELECT COUNT(*) as count FROM users WHERE role = "admin"'
            );

            if (adminCount[0].count <= 1) {
                return res.json({ 
                    success: false, 
                    error: 'ต้องมี Admin อย่างน้อย 1 คน' 
                });
            }
        }

        await pool.query(
            'UPDATE users SET role = ? WHERE id = ?',
            [role, id]
        );

        res.json({ 
            success: true, 
            message: 'เปลี่ยนสิทธิ์สำเร็จ' 
        });
    } catch (error) {
        console.error('Change role error:', error);
        res.status(500).json({ 
            success: false, 
            error: 'เกิดข้อผิดพลาดในการเปลี่ยนสิทธิ์' 
        });
    }
});

// ==================== PROJECT APIs ====================

// Get all projects (Admin)
app.get('/api/admin/projects', async (req, res) => {
    try {
        const [projects] = await pool.query(`
            SELECT 
                p.*,
                CONCAT(u.first_name, ' ', u.last_name) as created_by
            FROM projects p
            LEFT JOIN users u ON p.user_id = u.id
            ORDER BY p.created_date DESC
        `);

        res.json({ success: true, projects });
    } catch (error) {
        console.error('Get projects error:', error);
        res.status(500).json({ 
            success: false, 
            error: 'เกิดข้อผิดพลาดในการโหลดโครงการ' 
        });
    }
});

// Get user projects
app.get('/api/user/:userId/projects', async (req, res) => {
    try {
        const { userId } = req.params;

        const [projects] = await pool.query(`
            SELECT * FROM projects
            WHERE user_id = ?
            ORDER BY created_date DESC
        `, [userId]);

        res.json({ success: true, projects });
    } catch (error) {
        console.error('Get user projects error:', error);
        res.status(500).json({ 
            success: false, 
            error: 'เกิดข้อผิดพลาดในการโหลดโครงการ' 
        });
    }
});

// ==================== DATABASE INITIALIZATION ====================

async function initializeDatabase() {
    try {
        // Create database if not exists
        const connection = await mysql.createConnection({
            host: dbConfig.host,
            user: dbConfig.user,
            password: dbConfig.password
        });

        await connection.query(`CREATE DATABASE IF NOT EXISTS ${dbConfig.database}`);
        await connection.query(`USE ${dbConfig.database}`);

        // Create users table
        await connection.query(`
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                employee_id VARCHAR(50) NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role ENUM('admin', 'employee') DEFAULT 'employee',
                approved TINYINT(1) DEFAULT 0,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        `);

        // Create projects table (without manday)
        await connection.query(`
            CREATE TABLE IF NOT EXISTS projects (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                project_name VARCHAR(255) NOT NULL,
                business_value DECIMAL(10,2) DEFAULT 0,
                strategic_fit DECIMAL(10,2) DEFAULT 0,
                risk_level DECIMAL(10,2) DEFAULT 0,
                resource_availability DECIMAL(10,2) DEFAULT 0,
                total_score DECIMAL(10,2) DEFAULT 0,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        `);

        // Check if admin exists
        const [admins] = await connection.query(
            'SELECT id FROM users WHERE role = "admin" LIMIT 1'
        );

        // Create default admin if not exists
        if (admins.length === 0) {
            const defaultPassword = await bcrypt.hash('admin123', 10);
            await connection.query(`
                INSERT INTO users (first_name, last_name, email, employee_id, password_hash, role, approved)
                VALUES ('Admin', 'System', 'admin@g-able.com', 'ADMIN001', ?, 'admin', 1)
            `, [defaultPassword]);
            console.log('✅ Default admin created: admin / admin123');
        }

        await connection.end();
        console.log('✅ Database initialized successfully');
    } catch (error) {
        console.error('❌ Database initialization error:', error);
    }
}

// ==================== SERVER START ====================

async function startServer() {
    await initializeDatabase();
    
    app.listen(PORT, () => {
        console.log(`
╔════════════════════════════════════════╗
║   🚀 Project Scoring System Server    ║
║                                        ║
║   Port: ${PORT}                           ║
║   URL: http://localhost:${PORT}           ║
║                                        ║
║   Admin Login:                         ║
║   Username: admin                      ║
║   Password: admin123                   ║
╚════════════════════════════════════════╝
        `);
    });
}

startServer();

// Handle graceful shutdown
process.on('SIGINT', async () => {
    console.log('\n⚠️  Shutting down server...');
    await pool.end();
    process.exit(0);
});

