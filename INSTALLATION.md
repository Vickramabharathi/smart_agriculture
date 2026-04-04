 # 📦 Installation & Setup Guide

## Tech Stack
- **Frontend:** HTML5 + CSS3 + JavaScript + Bootstrap 5
- **Backend:** Flask (Python)
- **Database:** MySQL
- **API:** RESTful with Flask blueprints

## Quick Install (5 minutes)

### Step 1: Navigate to Project
```bash
cd c:\Users\HP\OneDrive\Desktop\smart_agriculture
```

### Step 2: Create & Activate Virtual Environment
```bash
# For Windows
python -m venv .venv
.venv\Scripts\Activate.ps1

# For macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Database (MySQL)
```bash
# Set environment variable for MySQL connection
setx MYSQL_DATABASE_URL "mysql+pymysql://root:password@localhost:3306/smart_agriculture"

# Then restart terminal or use:
$env:MYSQL_DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/smart_agriculture"
```

### Step 5: Initialize Database
```bash
python -c "from app import create_app, db; app = create_app('development'); app.app_context().push(); db.create_all(); print('✅ Database tables created')"
```

### Step 6: Run Application
```bash
python app.py
```

**Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

Visit: **http://localhost:5000**

---

## 📚 Core Dependencies

### Web Framework & Backend
```
Flask==2.3.0                 # Web framework
Flask-SQLAlchemy==3.1.1      # Database ORM
Flask-JWT-Extended==4.4.0    # Authentication
Flask-CORS==4.0.0            # Cross-origin requests
```

### Database
```
SQLAlchemy==2.0.0            # ORM
PyMySQL==1.1.0               # MySQL adapter
```

### Frontend Support
```
Werkzeug==3.1.7              # WSGI utilities
Jinja2==3.1.6                # Template engine (HTML rendering)
```

### API & Connectivity
```
requests==2.31.0             # HTTP requests
paho-mqtt==1.6.1             # MQTT for sensors
twilio==8.2.0                # SMS notifications
```

### Data Processing
```
openpyxl==3.1.5              # Excel export
reportlab==4.4.10            # PDF generation
PyPDF2==3.0.0                # PDF utilities
numpy==2.4.4                 # Numerical computing
```

### Utilities
```
python-dotenv==1.0.0         # Environment variables
pytz==2023.3                 # Timezone handling
python-dateutil==2.8.0       # Date utilities
geopy==2.3.0                 # Location services
folium==0.14.0               # Map visualization
```

### Optional (Commented Out - Requires Rust)
```
# transformers==4.30.0       # NLP (install only if needed)
# scikit-learn==1.3.2        # Machine learning (optional)
# tensorflow==2.21.0         # Deep learning (optional)
# torch==2.11.0              # PyTorch (optional)
```

---

## 🔧 System Requirements

### Minimum
- Python 3.9+
- MySQL 5.7+ or 8.0+
- 1GB RAM
- 500MB disk space

### Recommended
- Python 3.10+
- MySQL 8.0+
- 2GB+ RAM
- SSD with 1GB+ space

### For Development
- VS Code or PyCharm
- MySQL Workbench (optional, for GUI DB management)
- Postman (optional, for API testing)

---

## 📥 Installation Variations

### Standard Installation (All Features)
```bash
pip install -r requirements.txt
```
Includes Flask backend, MySQL support, reporting, maps, and notifications.

### Lightweight Installation
```bash
pip install Flask Flask-SQLAlchemy Flask-JWT-Extended Flask-CORS
pip install PyMySQL SQLAlchemy
pip install requests python-dotenv
pip install Werkzeug Jinja2
```
Minimal setup - just web framework and MySQL.

### Production Installation
```bash
pip install -r requirements.txt
pip install gunicorn  # For production server
```

---

## 🐍 Python Version Compatibility

| Python | Status | Tested |
|--------|--------|--------|
| 3.8 | ✅ Supported | Yes |
| 3.9 | ✅ Supported | Yes |
| 3.10 | ✅ Supported | Yes |
| 3.11 | ✅ Supported | Yes |
| 3.12 | ⚠️ Partial | Limited |

---

## 🔍 Verify Installation

### Test Flask & Database
```bash
python -c "
from app import create_app, db
app = create_app('development')
with app.app_context():
    print('✓ Flask app created')
    print('✓ Database URI configured')
    print('✓ Ready to run')
"
```

### Test Database Connection
```bash
python -c "
from app import create_app, db
app = create_app('development')
with app.app_context():
    try:
        db.session.execute('SELECT 1')
        print('✓ MySQL connection successful')
    except Exception as e:
        print(f'✗ MySQL error: {e}')
"
```

### Run Development Server
```bash
python app.py
# Visit http://localhost:5000
```

---

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│              FRONTEND (HTML + CSS + JS)                 │
│  Bootstrap 5 | Responsive UI | Dashboard | Forms        │
└─────────────────┬───────────────────────────────────────┘
                  │ HTTP/AJAX
┌─────────────────▼───────────────────────────────────────┐
│         BACKEND (Flask Python)                          │
│  Routes | Authentication | Business Logic | APIs        │
└─────────────────┬───────────────────────────────────────┘
                  │ SQLAlchemy ORM
┌─────────────────▼───────────────────────────────────────┐
│         DATABASE (MySQL)                                │
│  Users | Farms | Crops | Sensors | Alerts              │
└─────────────────────────────────────────────────────────┘
```

## 🗂️ Project Structure

```
smart_agriculture/
├── app.py                    # Main Flask application
├── config/
│   └── config.py            # Configuration (DB, API keys)
├── models/
│   └── database.py          # SQLAlchemy models (13 tables)
├── apis/                    # Flask blueprints
│   ├── auth.py             # Login/Register
│   ├── farm.py             # Farm management
│   ├── sensor.py           # Sensor readings
│   ├── disease.py          # Disease detection
│   ├── irrigation.py        # Irrigation control
│   └── ... (more APIs)
├── utils/
│   └── helpers.py          # Auth, notifications, utilities
├── static/
│   ├── style.css           # Custom CSS
│   └── uploads/            # User file uploads
├── templates/
│   ├── index.html          # Homepage
│   ├── dashboard.html      # Main dashboard
│   ├── upload.html         # Image upload
│   ├── weather.html        # Weather page
│   └── result.html         # Results page
├── requirements.txt        # Python dependencies
└── README.md              # Documentation
```

---

## 🚀 Performance Optimization

### Speed Up Installation
```bash
pip install -r requirements.txt --no-cache-dir
```

### Production Deployment
```bash
# Using Gunicorn (production WSGI server)
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Or with Flask development server (development only)
python app.py
```

### Database Optimization
```bash
# Create indexes for frequently queried fields
# (Already included in SQLAlchemy models)

# To check MySQL connection:
mysql -h localhost -u root -p smart_agriculture
```

---

## 🔐 MySQL Database Setup

### Create Database
```sql
CREATE DATABASE smart_agriculture;
CREATE USER 'smart_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON smart_agriculture.* TO 'smart_user'@'localhost';
FLUSH PRIVILEGES;
```

### Connection String Formats
```bash
# Development (SQLite - no setup needed)
SQLALCHEMY_DATABASE_URI=sqlite:///smart_agriculture.db

# Production (MySQL)
MYSQL_DATABASE_URL=mysql+pymysql://user:password@localhost:3306/smart_agriculture

# Alternative MySQL format
mysql://user:password@localhost/smart_agriculture
```

### Set Environment Variable
```bash
# Windows
setx MYSQL_DATABASE_URL "mysql+pymysql://root:password@localhost:3306/smart_agriculture"

# Linux/Mac
export MYSQL_DATABASE_URL="mysql+pymysql://root:password@localhost:3306/smart_agriculture"
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'app'"
**Solution:** Ensure you're in the project root directory
```bash
cd c:\Users\HP\OneDrive\Desktop\smart_agriculture
python app.py
```

### Issue: "AttributeError: module 'sqlalchemy' has no attribute '__all__'"
**Solution:** Upgrade Flask-SQLAlchemy
```bash
pip install Flask-SQLAlchemy==3.1.1 --upgrade
```

### Issue: "MySQLdb._exceptions.OperationalError: (2003, "Can't connect to MySQL")"
**Solution:** Check MySQL is running and credentials are correct
```bash
# Check MySQL service (Windows)
Get-Service MySQL80

# Or test connection
mysql -h localhost -u root -p
```

### Issue: "No module named 'psycopg2'" (ignored - PostgreSQL optional)
**Solution:** Not needed for MySQL. Already removed from requirements.txt

### Issue: "pip install hangs"
**Solution:**
```bash
pip install --default-timeout=1000 -r requirements.txt --no-cache-dir
```

### Issue: "MYSQL_DATABASE_URL environment variable not set"
**Solution:**
```bash
# Temporarily set in current session
$env:MYSQL_DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/smart_agriculture"

# Or permanently
setx MYSQL_DATABASE_URL "mysql+pymysql://root:password@localhost:3306/smart_agriculture"
# Restart terminal after setx
```

---

## 📦 Requirements.txt Format

The `requirements.txt` file uses pinned versions for consistency:
```
Package==Version
```

To update versions:
```bash
# Generate new requirements from current environment
pip freeze > requirements.txt

# Update specific package
pip install --upgrade flask
pip freeze | grep Flask >> requirements.txt
```

---

## 🔄 Version Updates

### Check for outdated packages
```bash
pip list --outdated
```

### Update all packages
```bash
pip install -r requirements.txt --upgrade
```

### Update specific package
```bash
pip install --upgrade tensorflow
```

---

## 📝 Creating Custom Environments

### For Machine Learning Development
```bash
pip install tensorflow torch scikit-learn jupyter numpy pandas matplotlib
```

### For Web Development Only
```bash
pip install Flask Flask-SQLAlchemy Flask-CORS requests gunicorn
```

### For Production Deployment
```bash
pip install -r requirements.txt gunicorn psycopg2-binary python-dotenv
```

---

## 🔄 Next Steps After Installation

1. **Start MySQL Service**
   ```bash
   # Windows: Services app or command line
   net start MySQL80
   ```

2. **Create Database**
   ```bash
   mysql -h localhost -u root -p < initial_schema.sql
   # Or let Flask auto-create tables in Step 5 above
   ```

3. **Configure Environment Variables**
   ```bash
   setx MYSQL_DATABASE_URL "mysql+pymysql://root:password@localhost:3306/smart_agriculture"
   ```

4. **Initialize Database Tables**
   ```bash
   python -c "from app import create_app, db; app = create_app('development'); app.app_context().push(); db.create_all(); print('✅ Tables created')"
   ```

5. **Run the Application**
   ```bash
   python app.py
   # Visit http://localhost:5000
   ```

6. **Test API Endpoints**
   ```bash
   curl http://localhost:5000/weather
   curl http://localhost:5000/api/auth/register
   ```

7. **Read Documentation**
   - [QUICKSTART.md](QUICKSTART.md) - Get started quickly
   - [API_REFERENCE.md](API_REFERENCE.md) - API endpoints
   - [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) - Detailed guide

---

## 💡 Development Tips

- Use virtual environments (`.venv`) to isolate dependencies
- Keep `requirements.txt` updated as you add packages: `pip freeze > requirements.txt`
- For frontend changes, edit HTML templates in `templates/` folder
- For backend changes, edit Python files in root and `apis/` folder
- Flask development server auto-reloads on file changes
- Use MySQL Workbench to visually manage your database
- Test APIs with Postman before integrating into frontend

---

## 📞 Getting Help

If you encounter issues:

1. **Check Python version**: `python --version` (should be 3.9+)
2. **Upgrade pip**: `pip install --upgrade pip`
3. **Clear cache**: `pip cache purge`
4. **Check MySQL**: `mysql -h localhost -u root -p`
5. **View Flask logs**: Check terminal output when `python app.py` runs
6. **Check MYSQL_DATABASE_URL**: `echo %MYSQL_DATABASE_URL%` (Windows) or `echo $MYSQL_DATABASE_URL` (Mac/Linux)

---

**Last Updated:** April 2, 2026  
**Tech Stack:** Flask + MySQL + Bootstrap  
**Status:** Ready for Development  
**Estimated Setup Time:** 5-10 minutes
