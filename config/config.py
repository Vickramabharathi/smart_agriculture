import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    
    # Upload configuration
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
    
    # External APIs
    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY') or "1dc8367105e7083aeef7dd2f25a3ae32"
    MARKET_API_KEY = os.environ.get('MARKET_API_KEY') or "579b464db66ec23bdd000001dee7d21cee8745ba48a11146d3a34910"
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

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
