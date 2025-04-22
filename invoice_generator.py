import pdfkit
import os
from database import get_invoice, get_product

def generate_invoice_html(invoice_data):
    invoice = invoice_data['invoice']
    items = invoice_data['items']
    
    # Create table rows for items
    items_html = ""
    for item in items:
        items_html += f"""
        <tr>
            <td class="text-center">{item['total']}</td>
            <td class="text-center">{item['quantity']}</td>
            <td class="text-center">{item['price']}</td>
            <td>{item['name']}</td>
            <td>{item['code']}</td>
        </tr>
        """
    
    # Calculate how many empty rows to add (minimum 3 rows)
    min_rows = 3
    current_rows = len(items)
    empty_rows_count = max(min_rows - current_rows, 0)
    
    # Add empty rows if needed
    for _ in range(empty_rows_count):
        items_html += '<tr><td class="text-center"></td><td class="text-center"></td><td class="text-center"></td><td></td><td></td></tr>'
    
    html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>فاتورة - {invoice['client_name']}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Cairo', sans-serif;
            background-color: white;
            margin: 0;
            padding: 0;
            color: #333;
        }}
        
        .container {{
            width: 100%;
            padding: 10px;
            background-color: white;
        }}
        
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }}
        
        .company-info {{
            text-align: right;
        }}
        
        .company-logo {{
            width: 40px;
            height: 40px;
            margin-bottom: 5px;
        }}
        
        .company-info h2 {{
            font-size: 16px;
            font-weight: bold;
            margin: 0 0 3px 0;
        }}
        
        .company-info p {{
            font-size: 12px;
            color: #555;
            margin: 0;
        }}
        
        .invoice-title {{
            text-align: left;
            font-size: 32px;
            font-weight: bold;
            color: #333;
        }}
        
        .client-info {{
            margin-bottom: 15px;
            width: 100%;
        }}
        
        .info-row {{
            display: flex;
            align-items: center;
            margin-bottom: 8px;
        }}
        
        .info-label {{
            font-weight: 600;
            width: 50px;
            font-size: 14px;
        }}
        
        .input-line {{
            border-bottom: 1px solid #999;
            padding-bottom: 3px;
            flex-grow: 1;
            margin-right: 5px;
            min-height: 20px;
            font-size: 14px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 15px;
        }}
        
        table, th, td {{
            border: 1px solid #999;
        }}
        
        th, td {{
            padding: 6px;
            text-align: right;
            vertical-align: middle;
            font-size: 12px;
        }}
        
        th {{
            background-color: #f5f5f5;
            font-weight: bold;
            text-align: center;
            color: #444;
        }}
        
        td {{
            height: 28px;
        }}
        
        .text-center {{
            text-align: center;
        }}
        
        .text-left {{
            text-align: left;
        }}
        
        .summary-section {{
            display: flex;
            justify-content: flex-end;
            align-items: flex-start;
            margin-top: 15px;
            margin-bottom: 25px;
        }}
        
        .total-container {{
            width: 30%;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        
        .total-box {{
            width: 100%;
            background-color: #f5f5f5;
            padding: 6px 8px;
            border: 1px solid #999;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }}
        
        .thank-you {{
            text-align: center;
            width: 100%;
        }}
        
        .thank-you p {{
            font-size: 18px;
            font-weight: 600;
            color: #444;
        }}
        
        .footer {{
            padding-top: 10px;
            font-size: 10px;
            color: #555;
            border-top: 1px solid #ccc;
            margin-top: 15px;
        }}
        
        .footer-content {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }}
        
        .tax-info {{
            text-align: right;
        }}
        
        .contact-info {{
            text-align: left;
        }}
        
        .contact-info p, .tax-info p {{
            margin: 3px 0;
        }}
        
        .icon {{
            display: inline-flex;
            align-items: center;
        }}
        
        .icon svg {{
            width: 10px;
            height: 10px;
            margin-left: 3px;
        }}
        
        @page {{
            size: A5;
            margin: 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="invoice-title">
                فاتوره
            </div>
            <div class="company-info">
                <svg class="company-logo" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 7C9.24 7 7 9.24 7 12C7 14.76 9.24 17 12 17C14.76 17 17 14.76 17 12C17 9.24 14.76 7 12 7ZM12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C7.58 20 4 16.42 4 12C4 7.58 7.58 4 12 4C16.42 4 20 7.58 20 12C20 16.42 16.42 20 12 20Z" fill="black"/>
                </svg>
                <h2>المكاوي للاستيراد و التصدير</h2>
                <p>أحمد حسين المكاوي</p>
            </div>
        </div>
        
        <div class="client-info">
            <div class="info-row">
                <span class="info-label">التاريخ:</span>
                <div class="input-line">{invoice['date']}</div>
            </div>
            <div class="info-row">
                <span class="info-label">العميل:</span>
                <div class="input-line">{invoice['client_name']}</div>
            </div>
            <div class="info-row">
                <span class="info-label"></span>
                <div class="input-line"></div>
            </div>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th style="width: 20%">الإجمالي</th>
                    <th style="width: 10%">عدد</th>
                    <th style="width: 15%">السعر</th>
                    <th style="width: 40%">الصنف</th>
                    <th style="width: 15%">كود</th>
                </tr>
            </thead>
            <tbody>
                {items_html}
            </tbody>
        </table>
        
        <div class="summary-section">
            <div class="total-container">
                <div class="total-box">
                    <span style="font-weight: bold;">إجمالي:</span>
                    <span style="font-weight: bold; font-size: 14px;">{invoice['total_amount']}</span>
                </div>
                <div class="thank-you">
                    <p>شكراً جزيلاً</p>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <div class="footer-content">
                <div class="tax-info">
                    <p><span style="font-weight: 600;">الملف الضريبي:</span> ٦٨٦-٥٠٣-٧٥٩ </p>
                    <p><span style="font-weight: 600;">السجل التجاري:</span> ١١٤٩٠٢</p>
                </div>
                <div class="contact-info">
                    <p class="icon">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                        </svg>
                        0502266489
                    </p>
                    <p class="icon">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                        </svg>
                        Elmekawy22@gmail.com
                    </p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
    """
    
    return html

def generate_invoice_pdf(invoice_id):
    invoice_data = get_invoice(invoice_id)
    if not invoice_data:
        return None
    
    html_content = generate_invoice_html(invoice_data)
    
    # Create directory for invoices if it doesn't exist
    os.makedirs('static/invoices', exist_ok=True)
    
    output_path = f'static/invoices/invoice_{invoice_id}.pdf'
    
    # Configure pdfkit options specifically for A5
    options = {
        'page-size': 'A5',
        'orientation': 'Portrait',
        'encoding': 'UTF-8',
        'margin-top': '3mm',
        'margin-right': '3mm',
        'margin-bottom': '3mm',
        'margin-left': '3mm',
        'enable-local-file-access': None,
        'no-outline': None,
        'print-media-type': None,
        'dpi': 300
    }
    
    # Specify the path to wkhtmltopdf based on your operating system
    # For Windows (example path, adjust to your installation):
    try:
        wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        if not os.path.exists(wkhtmltopdf_path):
            wkhtmltopdf_path = '/usr/local/bin/wkhtmltopdf'
    except:
        wkhtmltopdf_path = '/usr/local/bin/wkhtmltopdf'     
    # For macOS (if installed via Homebrew):
    # wkhtmltopdf_path = '/usr/local/bin/wkhtmltopdf'
    
    # For Linux:
    # wkhtmltopdf_path = '/usr/bin/wkhtmltopdf'
    
    # Generate PDF with specified path
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
    pdfkit.from_string(html_content, output_path, options=options, configuration=config)
    
    return output_path
