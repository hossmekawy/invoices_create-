from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
import os
import database
from invoice_generator import generate_invoice_pdf
from datetime import datetime
import socket
import base64
from io import BytesIO

# Try to import qrcode, but handle the case where it's not installed
qrcode_available = False
try:
    import qrcode
    qrcode_available = True
except ImportError:
    pass

app = Flask(__name__)
app.secret_key = 'mekawy_invoices_secret_key'

# Initialize database
database.init_db()

def get_server_ip():
    """Get the server's local IP address"""
    try:
        # Get the server's hostname
        hostname = socket.gethostname()
        # Get the server's IP address
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except:
        return "127.0.0.1"  # Default to localhost if unable to get IP

def generate_qr_code():
    """Generate QR code for the server URL"""
    global qrcode_available
    
    if not qrcode_available:
        return {
            'image': '',
            'url': 'QR code generation not available. Please install qrcode package.',
            'available': False
        }
    
    try:
        ip = get_server_ip()
        port = 5000  # Flask default port
        server_url = f"http://{ip}:{port}"
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(server_url)
        qr.make(fit=True)
        
        # Create an image from the QR Code
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to BytesIO object
        buffered = BytesIO()
        img.save(buffered)
        
        # Encode to base64 for embedding in HTML
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return {
            'image': img_str,
            'url': server_url,
            'available': True
        }
    except Exception as e:
        print(f"Error generating QR code: {e}")
        return {
            'image': '',
            'url': f'Error generating QR code: {str(e)}',
            'available': False
        }

@app.route('/')
def index():
    qr_data = generate_qr_code()
    return render_template('index.html', qr_data=qr_data)

# Product routes
@app.route('/products')
def products():
    products_list = database.get_all_products()
    return render_template('products.html', products=products_list)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        code = request.form['code']
        name = request.form['name']
        price = float(request.form['price'])
        
        success = database.add_product(code, name, price)
        if success:
            flash('تم إضافة المنتج بنجاح', 'success')
            return redirect(url_for('products'))
        else:
            flash('خطأ: كود المنتج موجود بالفعل', 'danger')
    
    return render_template('product_form.html', product=None)

@app.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = database.get_product(product_id)
    
    if request.method == 'POST':
        code = request.form['code']
        name = request.form['name']
        price = float(request.form['price'])
        
        success = database.update_product(product_id, code, name, price)
        if success:
            flash('تم تحديث المنتج بنجاح', 'success')
            return redirect(url_for('products'))
        else:
            flash('خطأ: كود المنتج موجود بالفعل', 'danger')
    
    return render_template('product_form.html', product=product)

@app.route('/products/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    database.delete_product(product_id)
    flash('تم حذف المنتج بنجاح', 'success')
    return redirect(url_for('products'))

@app.route('/api/products/search')
def search_products():
    code = request.args.get('code', '')
    product = database.get_product_by_code(code)
    if product:
        return jsonify({
            'id': product['id'],
            'code': product['code'],
            'name': product['name'],
            'price': product['price']
        })
    return jsonify(None)

# Invoice routes
@app.route('/invoices')
def invoices():
    invoices_list = database.get_all_invoices()
    return render_template('invoices.html', invoices=invoices_list)

@app.route('/invoices/create', methods=['GET', 'POST'])
def create_invoice():
    if request.method == 'POST':
        date = request.form['date']
        client_name = request.form['client_name']
        
        # Process invoice items
        items = []
        product_ids = request.form.getlist('product_id[]')
        quantities = request.form.getlist('quantity[]')
        prices = request.form.getlist('price[]')
        totals = request.form.getlist('total[]')
        
        total_amount = 0
        
        for i in range(len(product_ids)):
            if product_ids[i] and quantities[i] and prices[i] and totals[i]:
                item = {
                    'product_id': int(product_ids[i]),
                    'quantity': int(quantities[i]),
                    'price': float(prices[i]),
                    'total': float(totals[i])
                }
                items.append(item)
                total_amount += item['total']
        
        # Create invoice in database
        invoice_id = database.create_invoice(date, client_name, total_amount, items)
        
        # Generate PDF
        generate_invoice_pdf(invoice_id)
        
        flash('تم إنشاء الفاتورة بنجاح', 'success')
        return redirect(url_for('view_invoice', invoice_id=invoice_id))
    
    products_list = database.get_all_products()
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('invoice_form.html', products=products_list, today=today)

@app.route('/invoices/view/<int:invoice_id>')
def view_invoice(invoice_id):
    invoice_data = database.get_invoice(invoice_id)
    if not invoice_data:
        flash('الفاتورة غير موجودة', 'danger')
        return redirect(url_for('invoices'))
    
    pdf_path = f'static/invoices/invoice_{invoice_id}.pdf'
    if not os.path.exists(pdf_path):
        generate_invoice_pdf(invoice_id)
    
    return render_template('invoice_view.html', 
                          invoice=invoice_data['invoice'], 
                          items=invoice_data['items'],
                          pdf_url=url_for('static', filename=f'invoices/invoice_{invoice_id}.pdf'))

@app.route('/invoices/download/<int:invoice_id>')
def download_invoice(invoice_id):
    pdf_path = f'static/invoices/invoice_{invoice_id}.pdf'
    if not os.path.exists(pdf_path):
        invoice_data = database.get_invoice(invoice_id)
        if not invoice_data:
            flash('الفاتورة غير موجودة', 'danger')
            return redirect(url_for('invoices'))
        generate_invoice_pdf(invoice_id)
    
    return send_file(pdf_path, as_attachment=True, download_name=f'invoice_{invoice_id}.pdf')

@app.route('/invoices/delete/<int:invoice_id>', methods=['POST'])
def delete_invoice(invoice_id):
    database.delete_invoice(invoice_id)
    
    # Delete PDF file if exists
    pdf_path = f'static/invoices/invoice_{invoice_id}.pdf'
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    
    flash('تم حذف الفاتورة بنجاح', 'success')
    return redirect(url_for('invoices'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
