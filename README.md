# Mekawy Invoices

![Mekawy Invoices](https://img.shields.io/badge/Mekawy-Invoices-blue?style=for-the-badge&logo=flask)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)

<p align="center">
  <img src="https://www.svgrepo.com/show/309429/circle-small.svg" alt="Mekawy Invoices Logo" width="120">
</p>

## 📋 Overview

Mekawy Invoices is a modern, Arabic-first invoice management system built with Flask. It provides a complete solution for businesses to manage products, create professional invoices, and track sales. The system is designed with simplicity and efficiency in mind, making it perfect for small to medium-sized businesses.

## ✨ Features

- **🏠 Responsive Dashboard** - Access your data from any device with a mobile-friendly interface
- **📱 Mobile Access via QR Code** - Scan QR code to access the system from your phone
- **📦 Product Management** - Add, edit, and delete products with custom codes and prices
- **📄 Invoice Creation** - Generate professional invoices with automatic calculations
- **🖨️ PDF Generation** - Export invoices as PDF documents for printing or sharing
- **🔍 Product Search** - Quickly find products by code during invoice creation
- **📊 Invoice History** - View and manage all created invoices
- **🌐 Arabic Interface** - Fully localized for Arabic-speaking users

## 🖼️ Screenshots

<p align="center">
  <img src="https://via.placeholder.com/800x450.png?text=Mekawy+Invoices+Dashboard" alt="Dashboard" width="80%">
</p>

<p align="center">
  <table>
    <tr>
      <td><img src="https://via.placeholder.com/400x300.png?text=Products+Management" alt="Products Management"></td>
      <td><img src="https://via.placeholder.com/400x300.png?text=Invoice+Creation" alt="Invoice Creation"></td>
    </tr>
    <tr>
      <td><img src="https://via.placeholder.com/400x300.png?text=Invoice+PDF" alt="Invoice PDF"></td>
      <td><img src="https://via.placeholder.com/400x300.png?text=Mobile+Access" alt="Mobile Access"></td>
    </tr>
  </table>
</p>

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/hossmekawy/invoices_create-.git
cd invoices_create-
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## 🏗️ Project Structure

```
mekawy-invoices/
├── app.py                  # Main application file
├── database.py             # Database operations
├── invoice_generator.py    # PDF generation logic
├── requirements.txt        # Project dependencies
├── static/                 # Static files (CSS, JS, images)
│   ├── css/                # Stylesheets
│   ├── js/                 # JavaScript files
│   └── invoices/           # Generated invoice PDFs
└── templates/              # HTML templates
    ├── base.html           # Base template with common elements
    ├── index.html          # Dashboard/home page
    ├── products.html       # Products listing page
    ├── product_form.html   # Add/edit product form
    ├── invoices.html       # Invoices listing page
    ├── invoice_form.html   # Create invoice form
    └── invoice_view.html   # Invoice details view
```

## 🔧 Configuration

The application uses SQLite by default for simplicity. The database file will be created automatically in the project directory.

To customize the application settings, modify the following:

- **Database**: Edit `database.py` to change database settings
- **PDF Generation**: Modify `invoice_generator.py` to customize invoice appearance
- **Application Settings**: Update `app.py` for Flask configuration options

## 🌐 Deployment

For production deployment, consider the following:

1. Use a production WSGI server like Gunicorn or uWSGI
2. Set up a reverse proxy with Nginx or Apache
3. Configure proper security settings (HTTPS, etc.)
4. Set `debug=False` in the Flask application

Example deployment with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🛠️ Technologies Used

- **Backend**: Python, Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **PDF Generation**: pdfkit, wkhtmltopdf
- **QR Code**: qrcode, Pillow

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

Ahmed Hussein Elmekawy - hussienmekawy38@gmail.com

Project Link: [https://github.com/hossmekawy/invoices_create-.git](https://github.com/hossmekawy/invoices_create-.git)

---

<p align="center">
  Made with ❤️ for Mekawy Import & Export
</p>
