"""
In-memory database models - no database required
All data is stored in memory and will be lost on app restart
"""
from datetime import datetime
from enum import Enum
import json

# Dummy database for compatibility with Flask-SQLAlchemy free imports
class DummyDB:
    def init_app(self, app):
        pass

db = DummyDB()

class UserRole(Enum):
    FARMER = "farmer"
    ADMIN = "admin"
    EXPERT = "expert"

# Dummy model classes for API compatibility (no database)
class User:
    def __init__(self, username, email, password_hash, role=UserRole.FARMER, phone=None, address=None):
        self.id = 1
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.phone = phone
        self.address = address
        self.created_at = datetime.utcnow()
        self.farms = []
        self.alerts = []

class Farm:
    def __init__(self, user_id, name, location, latitude=None, longitude=None, area=None, soil_type=None):
        self.id = 1
        self.user_id = user_id
        self.name = name
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.area = area
        self.soil_type = soil_type
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.crops = []
        self.sensor_readings = []

class Crop:
    def __init__(self, farm_id, crop_name, variety=None, planting_date=None, expected_harvest=None, area=None):
        self.id = 1
        self.farm_id = farm_id
        self.crop_name = crop_name
        self.variety = variety
        self.planting_date = planting_date
        self.expected_harvest = expected_harvest
        self.area = area
        self.current_health_score = 100.0
        self.created_at = datetime.utcnow()
        self.disease_history = []
        self.recommendations = []

class SensorReading:
    def __init__(self, farm_id, sensor_type, value, unit=None, location=None):
        self.id = 1
        self.farm_id = farm_id
        self.sensor_type = sensor_type
        self.value = value
        self.unit = unit
        self.location = location
        self.timestamp = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': self.id,
            'sensor_type': self.sensor_type,
            'value': self.value,
            'unit': self.unit,
            'location': self.location,
            'timestamp': self.timestamp.isoformat()
        }

class DiseaseDetection:
    def __init__(self, crop_id, disease_name=None, disease_confidence=None, severity='mild'):
        self.id = 1
        self.crop_id = crop_id
        self.image_path = None
        self.disease_name = disease_name
        self.disease_confidence = disease_confidence
        self.pest_detected = False
        self.pest_type = None
        self.severity = severity
        self.treatment_recommendation = None
        self.detected_at = datetime.utcnow()
        self.status = 'active'

class Recommendation:
    def __init__(self, crop_id, recommendation_type, reason=None, priority='medium'):
        self.id = 1
        self.crop_id = crop_id
        self.recommendation_type = recommendation_type
        self.npk_nitrogen = None
        self.npk_phosphorus = None
        self.npk_potassium = None
        self.fertilizer_name = None
        self.irrigation_amount = None
        self.irrigation_schedule = None
        self.recommended_crop = None
        self.compatibility_score = None
        self.reason = reason
        self.priority = priority
        self.created_at = datetime.utcnow()

class Alert:
    def __init__(self, user_id, alert_type, title, message, severity='info', farm_id=None):
        self.id = 1
        self.user_id = user_id
        self.farm_id = farm_id
        self.alert_type = alert_type
        self.title = title
        self.message = message
        self.severity = severity
        self.is_predictive = False
        self.prediction_days = None
        self.is_read = False
        self.is_sent_sms = False
        self.is_sent_email = False
        self.created_at = datetime.utcnow()

class IrrigationControl:
    def __init__(self, farm_id, is_automated=False, moisture_threshold=40.0):
        self.id = 1
        self.farm_id = farm_id
        self.is_automated = is_automated
        self.moisture_threshold = moisture_threshold
        self.max_water_per_day = None
        self.is_motor_on = False
        self.motor_on_time = None
        self.motor_off_time = None
        self.last_irrigation = None
        self.updated_at = datetime.utcnow()

class MarketData:
    def __init__(self, crop_name, location, current_price=None):
        self.id = 1
        self.crop_name = crop_name
        self.location = location
        self.current_price = current_price
        self.min_price_30days = None
        self.max_price_30days = None
        self.avg_price_30days = None
        self.trend = 'stable'
        self.volume_available = None
        self.quality_grade = 'A'
        self.last_updated = datetime.utcnow()

class YieldPrediction:
    def __init__(self, crop_id, predicted_yield=None, confidence_score=0.0):
        self.id = 1
        self.crop_id = crop_id
        self.predicted_yield = predicted_yield
        self.confidence_score = confidence_score
        self.prediction_model = 'default'
        self.factors = '{}'
        self.predicted_on = datetime.utcnow()

class ChatHistory:
    def __init__(self, user_id, user_message, bot_response, intent=None):
        self.id = 1
        self.user_id = user_id
        self.user_message = user_message
        self.bot_response = bot_response
        self.intent = intent
        self.confidence = 0.0
        self.timestamp = datetime.utcnow()
