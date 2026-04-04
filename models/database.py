from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum
import json

db = SQLAlchemy()

class UserRole(Enum):
    FARMER = "farmer"
    ADMIN = "admin"
    EXPERT = "expert"

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.FARMER)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    farms = db.relationship('Farm', backref='owner', lazy=True, cascade='all, delete-orphan')
    alerts = db.relationship('Alert', backref='user', lazy=True, cascade='all, delete-orphan')

class Farm(db.Model):
    __tablename__ = 'farms'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    area = db.Column(db.Float)  # in hectares
    soil_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    crops = db.relationship('Crop', backref='farm', lazy=True, cascade='all, delete-orphan')
    sensor_readings = db.relationship('SensorReading', backref='farm', lazy=True, cascade='all, delete-orphan')

class Crop(db.Model):
    __tablename__ = 'crops'
    
    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    crop_name = db.Column(db.String(100), nullable=False)
    variety = db.Column(db.String(100))
    planting_date = db.Column(db.DateTime)
    expected_harvest = db.Column(db.DateTime)
    area = db.Column(db.Float)  # in hectares
    current_health_score = db.Column(db.Float, default=100.0)  # 0-100
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    disease_history = db.relationship('DiseaseDetection', backref='crop', lazy=True, cascade='all, delete-orphan')
    recommendations = db.relationship('Recommendation', backref='crop', lazy=True, cascade='all, delete-orphan')

class SensorReading(db.Model):
    __tablename__ = 'sensor_readings'
    
    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    sensor_type = db.Column(db.String(50), nullable=False)  # moisture, temperature, humidity, ph, water_level
    value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20))  # %, °C, pH, mm
    location = db.Column(db.String(255))  # zone A, zone B, etc
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'sensor_type': self.sensor_type,
            'value': self.value,
            'unit': self.unit,
            'location': self.location,
            'timestamp': self.timestamp.isoformat()
        }

class DiseaseDetection(db.Model):
    __tablename__ = 'disease_detections'
    
    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id'), nullable=False)
    image_path = db.Column(db.String(255))
    disease_name = db.Column(db.String(100))
    disease_confidence = db.Column(db.Float)  # 0-1
    pest_detected = db.Column(db.Boolean, default=False)
    pest_type = db.Column(db.String(100))
    severity = db.Column(db.String(20))  # mild, moderate, severe
    treatment_recommendation = db.Column(db.Text)
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # active, treated, resolved

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id'), nullable=False)
    recommendation_type = db.Column(db.String(50))  # irrigation, fertilizer, pesticide, crop_change
    
    # Fertilizer specific
    npk_nitrogen = db.Column(db.Float)
    npk_phosphorus = db.Column(db.Float)
    npk_potassium = db.Column(db.Float)
    fertilizer_name = db.Column(db.String(100))
    
    # Irrigation specific
    irrigation_amount = db.Column(db.Float)  # liters
    irrigation_schedule = db.Column(db.String(100))  # daily, 2 days, weekly, etc
    
    # Crop recommendation
    recommended_crop = db.Column(db.String(100))
    compatibility_score = db.Column(db.Float)
    
    reason = db.Column(db.Text)
    priority = db.Column(db.String(20))  # low, medium, high
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Alert(db.Model):
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'))
    alert_type = db.Column(db.String(50))  # disease, pest, weather, sensor, automation
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20))  # info, warning, critical
    is_predictive = db.Column(db.Boolean, default=False)  # True if predicted future risk
    prediction_days = db.Column(db.Integer)  # predict X days in advance
    is_read = db.Column(db.Boolean, default=False)
    is_sent_sms = db.Column(db.Boolean, default=False)
    is_sent_email = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class IrrigationControl(db.Model):
    __tablename__ = 'irrigation_control'
    
    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    is_automated = db.Column(db.Boolean, default=False)
    moisture_threshold = db.Column(db.Float, default=40.0)  # trigger irrigation below this %
    max_water_per_day = db.Column(db.Float)  # liters
    is_motor_on = db.Column(db.Boolean, default=False)
    motor_on_time = db.Column(db.DateTime)
    motor_off_time = db.Column(db.DateTime)
    last_irrigation = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MarketData(db.Model):
    __tablename__ = 'market_data'
    
    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    current_price = db.Column(db.Float)  # per kg or per unit
    min_price_30days = db.Column(db.Float)
    max_price_30days = db.Column(db.Float)
    avg_price_30days = db.Column(db.Float)
    trend = db.Column(db.String(20))  # up, down, stable
    volume_available = db.Column(db.Float)
    quality_grade = db.Column(db.String(10))  # A, B, C, etc
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

class YieldPrediction(db.Model):
    __tablename__ = 'yield_predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id'), nullable=False)
    predicted_yield = db.Column(db.Float)  # in tons/kg
    confidence_score = db.Column(db.Float)  # 0-1
    prediction_model = db.Column(db.String(50))  # model used for prediction
    factors = db.Column(db.Text)  # JSON string of factors affecting yield
    predicted_on = db.Column(db.DateTime, default=datetime.utcnow)

class ChatHistory(db.Model):
    __tablename__ = 'chat_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    intent = db.Column(db.String(50))  # disease_diagnosis, pest_help, fertilizer, irrigation, etc
    confidence = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
