const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

const dbPath = path.resolve(__dirname, 'database_tuned.sqlite');
const db = new sqlite3.Database(dbPath, (err) => {
    if (err) {
        console.error('Could not connect to database', err);
    } else {
        console.log('Connected to database');
    }
});

function loadLoadTestAccounts() {
    const csvPath = path.resolve(__dirname, 'test-data', 'test_accounts.csv');
    const expectedHeaders = ['email', 'password', 'full_name', 'role', 'scenario'];

    if (!fs.existsSync(csvPath)) {
        throw new Error(`Load-test account file not found: ${csvPath}`);
    }

    const [header, ...rows] = fs.readFileSync(csvPath, 'utf8').trim().split(/\r?\n/);
    if (header !== expectedHeaders.join(',')) {
        throw new Error(`Unexpected CSV header in ${csvPath}`);
    }

    return rows.filter(Boolean).map((row, index) => {
        const [email, password, fullName, role, scenario] = row.split(',');
        if (!email || !password || !fullName || !role || !scenario) {
            throw new Error(`Invalid load-test account on CSV row ${index + 2}`);
        }
        return { email, password, fullName, role, scenario };
    });
}

function loadSeedProducts() {
    const csvPath = path.resolve(__dirname, 'test-data', 'test_products.csv');
    const expectedHeaders = ['product_id', 'name', 'price', 'description', 'image_url', 'category_id', 'search_keyword'];

    if (!fs.existsSync(csvPath)) {
        throw new Error(`Product seed file not found: ${csvPath}`);
    }

    const [header, ...rows] = fs.readFileSync(csvPath, 'utf8').trim().split(/\r?\n/);
    if (header !== expectedHeaders.join(',')) {
        throw new Error(`Unexpected CSV header in ${csvPath}`);
    }

    return rows.filter(Boolean).map((row, index) => {
        const [id, name, price, description, imageUrl, categoryId, searchKeyword] = row.split(',');
        if (!id || !name || !price || !description || !imageUrl || !categoryId || !searchKeyword) {
            throw new Error(`Invalid product seed on CSV row ${index + 2}`);
        }
        return { id: Number(id), name, price: Number(price), description, imageUrl, categoryId: Number(categoryId), searchKeyword };
    });
}

function initDatabase() {
    db.serialize(() => {
        db.run('DROP TABLE IF EXISTS coupon_usage');
        db.run('DROP TABLE IF EXISTS coupons');
        db.run('DROP TABLE IF EXISTS users');
        db.run('DROP TABLE IF EXISTS products');
        db.run('DROP TABLE IF EXISTS categories');
        db.run('DROP TABLE IF EXISTS orders');

        // Create Categories Table
        db.run(`CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )`);

        // Create Coupons Table
        db.run(`CREATE TABLE coupons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            type TEXT DEFAULT 'percent',
            discount_value INTEGER,
            min_order_amount INTEGER DEFAULT 0,
            expired_at DATETIME,
            is_active INTEGER DEFAULT 1,
            max_uses_per_user INTEGER DEFAULT 1
        )`);

        // Create Coupon Usage Table
        db.run(`CREATE TABLE coupon_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coupon_id INTEGER,
            user_id INTEGER,
            used_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )`);

        // Create Users Table
        // Added columns for Phase 2 & 3: login_attempts, locked_until, reset_token, shipping_address, phone
        db.run(`CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            password TEXT,
            role TEXT DEFAULT 'user',
            login_attempts INTEGER DEFAULT 0,
            locked_until DATETIME,
            reset_token TEXT,
            shipping_address TEXT,
            phone TEXT
        )`);

        // Create Products Table
        db.run(`CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price INTEGER,
            description TEXT,
            imageUrl TEXT,
            category_id INTEGER
        )`);

        // Create Orders Table
        db.run(`CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            total_amount INTEGER,
            status TEXT DEFAULT 'pending',
            shipping_address TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )`);

        // Seed Categories
        const insertCategory = db.prepare('INSERT INTO categories (name) VALUES (?)');
        insertCategory.run('Điện thoại');
        insertCategory.run('Laptop');
        insertCategory.run('Phụ kiện');
        insertCategory.finalize();

        // Seed Users
        const insertUser = db.prepare('INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)');
        insertUser.run('Admin User', 'admin@eshop.com', 'Admin123!', 'admin');
        insertUser.run('Test User', 'test@eshop.com', 'Test1234!', 'user');
        const loadTestAccounts = loadLoadTestAccounts();
        loadTestAccounts.forEach(({ fullName, email, password, role }) => {
            insertUser.run(fullName, email, password, role);
        });
        insertUser.finalize();
        console.log(`Seeded ${loadTestAccounts.length} load-test accounts.`);

        const seedProducts = loadSeedProducts();
        const insertProduct = db.prepare('INSERT INTO products (id, name, price, description, imageUrl, category_id) VALUES (?, ?, ?, ?, ?, ?)');
        seedProducts.forEach(({ id, name, price, description, imageUrl, categoryId }) => {
            insertProduct.run(id, name, price, description, imageUrl, categoryId);
        });
        insertProduct.finalize();
        console.log(`Seeded ${seedProducts.length} workload products.`);

        // Seed Coupons
        const insertCoupon = db.prepare('INSERT INTO coupons (code, type, discount_value, min_order_amount, expired_at, is_active, max_uses_per_user) VALUES (?, ?, ?, ?, ?, ?, ?)');
        insertCoupon.run('SAVE10', 'percent', 10, 300000, '2099-12-31', 1, 1);   // 10% off, min 300k, valid
        insertCoupon.run('BIGBUY', 'fixed', 50000, 500000, '2099-12-31', 1, 1);  // 50k off, min 500k, valid
        insertCoupon.run('VIP100', 'fixed', 100000, 300000, '2099-12-31', 1, 2); // 100k off, min 300k, max 2 uses
        insertCoupon.run('EXPIRED', 'percent', 20, 100000, '2020-01-01', 1, 1);  // 20% off, EXPIRED
        insertCoupon.finalize();

        // Reapply tuning after reset/seed: DROP TABLE also removes its indexes.
        db.get('PRAGMA journal_mode=WAL', (err, row) => {
            if (err) throw err;
            if (row.journal_mode !== 'wal') {
                throw new Error(`Unexpected journal mode: ${row.journal_mode}`);
            }
            console.log('Database tuning: journal_mode=wal');
        });
        db.run('CREATE INDEX IF NOT EXISTS idx_products_name ON products(name)', (err) => {
            if (err) throw err;
            console.log('Database tuning: idx_products_name ON products(name)');
        });
        console.log('Database initialized and seeded (Phase 2).');
    });
}

initDatabase();

module.exports = db;
