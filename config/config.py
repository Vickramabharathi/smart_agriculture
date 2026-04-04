import os
from datetime import timedelta

def get_database_uri():
    """Get database URI from environment or use default"""
    # For production/Vercel, use environment variable
    if os.environ.get('DATABASE_URL'):
        db_url = os.environ.get('DATABASE_URL')
        # Convert DATABASE_URL format to SQLAlchemy format if needed
        if 'mysql://' in db_url:
            db_url = db_url.replace('mysql://', 'mysql+mysqlconnector://')
        elif 'mysql+pymysql://' in db_url:
            db_url = db_url.replace('mysql+pymysql://', 'mysql+mysqlconnector://')
        return db_url
    # Default for local development
    return 'mysql+mysqlconnector://root:1234@localhost:3306/smart_agriculture'

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    
    # Upload configuration
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
    
    # External APIs
    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY') or "1dc8367105e7083aeef7dd2f25a3ae32"
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID') or ""
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN') or ""
    TWILIO_PHONE = os.environ.get('TWILIO_PHONE') or ""
    
    # MQTT Configuration
    MQTT_BROKER = os.environ.get('MQTT_BROKER') or 'localhost'
    MQTT_PORT = int(os.environ.get('MQTT_PORT') or 1883)
    MQTT_TOPICS = ['sensors/moisture', 'sensors/temperature', 'sensors/humidity', 'sensors/ph', 'sensors/water_level']

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    # MySQL Configuration (using mysql-connector-python):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:1234@localhost:3306/smart_agriculture'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = get_database_uri()

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
