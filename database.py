import sqlite3
import os

DB_PATH = 'mekawy_invoices.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if os.path.exists(DB_PATH):
        return
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create products table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )
    ''')
    
    # Create invoices table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        client_name TEXT NOT NULL,
        total_amount REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create invoice_items table for the relationship between invoices and products
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS invoice_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        total REAL NOT NULL,
        FOREIGN KEY (invoice_id) REFERENCES invoices (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    ''')
    
    # Insert some sample products
    sample_products = [
        ('P001', 'كابل USB', 25.0),
        ('P002', 'شاحن هاتف', 50.0),
        ('P003', 'سماعات بلوتوث', 120.0),
        ('P004', 'بطارية محمولة', 85.0),
        ('P005', 'حافظة هاتف', 30.0)
    ]
    
    cursor.executemany('INSERT INTO products (code, name, price) VALUES (?, ?, ?)', sample_products)
    
    conn.commit()
    conn.close()

# Product CRUD operations
def get_all_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products ORDER BY code').fetchall()
    conn.close()
    return products

def get_product(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    return product

def get_product_by_code(code):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE code = ?', (code,)).fetchone()
    conn.close()
    return product

def add_product(code, name, price):
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO products (code, name, price) VALUES (?, ?, ?)', 
                    (code, name, price))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    finally:
        conn.close()
    return success

def update_product(product_id, code, name, price):
    conn = get_db_connection()
    try:
        conn.execute('UPDATE products SET code = ?, name = ?, price = ? WHERE id = ?', 
                    (code, name, price, product_id))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    finally:
        conn.close()
    return success

def delete_product(product_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()

# Invoice CRUD operations
def create_invoice(date, client_name, total_amount, items):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert invoice
    cursor.execute(
        'INSERT INTO invoices (date, client_name, total_amount) VALUES (?, ?, ?)',
        (date, client_name, total_amount)
    )
    invoice_id = cursor.lastrowid
    
    # Insert invoice items
    for item in items:
        cursor.execute(
            'INSERT INTO invoice_items (invoice_id, product_id, quantity, price, total) VALUES (?, ?, ?, ?, ?)',
            (invoice_id, item['product_id'], item['quantity'], item['price'], item['total'])
        )
    
    conn.commit()
    conn.close()
    return invoice_id

def get_all_invoices():
    conn = get_db_connection()
    invoices = conn.execute('SELECT * FROM invoices ORDER BY created_at DESC').fetchall()
    conn.close()
    return invoices

def get_invoice(invoice_id):
    conn = get_db_connection()
    invoice = conn.execute('SELECT * FROM invoices WHERE id = ?', (invoice_id,)).fetchone()
    
    if invoice:
        items = conn.execute('''
            SELECT ii.*, p.code, p.name 
            FROM invoice_items ii 
            JOIN products p ON ii.product_id = p.id 
            WHERE ii.invoice_id = ?
        ''', (invoice_id,)).fetchall()
        
        conn.close()
        return {
            'invoice': invoice,
            'items': items
        }
    
    conn.close()
    return None

def delete_invoice(invoice_id):
    conn = get_db_connection()
    # First delete related invoice items
    conn.execute('DELETE FROM invoice_items WHERE invoice_id = ?', (invoice_id,))
    # Then delete the invoice
    conn.execute('DELETE FROM invoices WHERE id = ?', (invoice_id,))
    conn.commit()
    conn.close()
