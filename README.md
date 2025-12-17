# General Store Management System

A robust and user-friendly Point of Sale (POS) and Inventory Management System built with Django. This application is designed to help small businesses manage their daily operations, including sales, product inventory, customers, and reporting.

## 🚀 Features

- **Dashboard**: Real-time insights into today's revenue, profit, sales count, and low stock alerts.
- **Point of Sale (POS)**: Efficient billing interface for quick transaction processing.
- **Product Management**: 
  - Add, edit, and delete products.
  - Track stock levels and set minimum stock alerts.
- **Sales & Invoicing**: 
  - View detailed sales history.
  - Generate and print invoices.
- **Customer Management**: Maintain a database of customers for loyalty and tracking.
- **Reports**: Generate sales and stock reports for better decision making.
- **Admin Panel**: Secure administrative interface for advanced configurations.
- **Responsive Design**: Mobile-friendly interface built with Bootstrap 5.

## 🛠️ Tech Stack

- **Backend**: Python, Django 5
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (Default)
- **Icons**: FontAwesome

## 💻 Installation Guide

Follow these steps to set up the project locally.

### Prerequisites
- Python 3.8 or higher installed.
- Git installed.

### Steps

1. **Clone the Repository**
   ```bash
   git clone <your-repo-url>
   cd general-store
   ```

2. **Create a Virtual Environment**
   It is recommended to use a virtual environment to manage dependencies.
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare the Database** (Fresh Install)
   Initialize a new database and apply migrations:
   ```bash
   python manage.py migrate
   ```

5. **Load Static Files** (Optional)
   If styles or icons are missing, run this command:
   ```bash
   python manage.py collectstatic
   ```
   *Type `yes` if prompted.*

6. **Create Admin User**
   Since this is a fresh installation, you need to create an admin user:
   ```bash
   python create_admin.py
   ```
   *This will set the default credentials: `admin` / `password123`*

7. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

   The application will be accessible at `http://127.0.0.1:8000/`.

## 🔐 Default Login Credentials

Use the following credentials to access the system:


### Administrator
*Django Admin Panel for backend management*
- **Username**: `admin`
- **Password**: `password123`
- **URL**: `http://127.0.0.1:8000/admin/`

> **Note**: You can change the admin password via the Admin Panel or by modifying `create_admin.py`.

## 📂 Project Structure

```
general-store/
├── GeneralStore/       # Project configuration settings
├── store/              # Main application logic (Models, Views, URLs)
├── templates/          # HTML Templates
├── static/             # Static files (CSS, JS, Images)
├── create_admin.py     # Script to create superuser
├── manage.py           # Django command-line utility
└── requirements.txt    # Project dependencies
```

## 🤝 Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

## 📄 License

This project is proprietary and intended for personal use or internal business management.
