# NEXLINK – Smart URL Shortener & Analytics

A modern, full-stack URL shortener built with Python and Flask, featuring user authentication, URL management, click tracking, and analytics.

## 🚀 Features

- User Registration and Login
- Secure Password Authentication
- Short URL Generation
- Automatic URL Redirection
- Click Tracking and Analytics
- Personal URL Dashboard
- Search and Pagination
- URL Copy and Delete
- Interactive Analytics Charts
- IST-Based Click History
- Responsive and Modern UI

## 🛠️ Tech Stack

**Backend:** Python, Flask  
**Frontend:** HTML, CSS, JavaScript  
**Database:** SQLite, Flask-SQLAlchemy  
**Authentication:** Flask-Login  
**Database Migrations:** Flask-Migrate  
**Charts:** Chart.js

##  Project Structure:

```text
smart_url_shortener/
│
├── app/
│   ├── auth/
│   ├── dashboard/
│   ├── urls/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── extensions.py
│   └── __init__.py
│
├── migrations/
├── config.py
├── run.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Sujal-Suthar/NEXLINK.git
```

### 2. Navigate to the project

```bash
cd smart_url_shortener
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure environment variables

Create a `.env` file and add the environment variables required by your application.

Never upload your secret key or private credentials to GitHub.

### 7. Run database migrations

```bash
flask db upgrade
```

### 8. Start the application

```bash
python run.py
```

Open your browser:

```text
http://127.0.0.1:5000
```

## 📊 Analytics Dashboard

NEXLINK provides an analytics dashboard to monitor URL performance, track clicks, and view click history.

## 🔐 Security

- Password hashing
- User-specific URL management
- Environment-based configuration
- Protected authentication routes

## 👨‍💻 Developer

**Sujal Suthar**

Python | Flask | Full-Stack Development

---

⭐ If you find this project interesting, consider giving it a star!