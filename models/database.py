"""
In-memory database models - no database required
All data is stored in memory and will be lost on app restart
"""
from datetime import datetime
from enum import Enum

# In-memory storage
_storage = {
    'users': [],
    'farms': [],
    'crops': [],
    'sensor_readings': [],
    'disease_detections': [],
    'recommendations': [],
    'alerts': [],
    'irrigation_control': [],
    'market_data': [],
    'yield_predictions': [],
    'chat_history': []
}

# Session-like object for compatibility
class MockSession:
    """Mock SQLAlchemy session for in-memory operations"""
    def add(self, obj):
        """Add object to storage"""
        table_name = getattr(obj.__class__, '__tablename__', obj.__class__.__name__.lower())
        if not any(x.id == obj.id for x in _storage.get(table_name, [])):
            _storage.setdefault(table_name, []).append(obj)
    
    def commit(self):
        """Commit changes (no-op in memory)"""
        pass
    
    def rollback(self):
        """Rollback changes (no-op in memory)"""
        pass
    
    def delete(self, obj):
        """Delete object from storage"""
        table_name = getattr(obj.__class__, '__tablename__', obj.__class__.__name__.lower())
        if table_name in _storage:
            _storage[table_name] = [x for x in _storage[table_name] if x.id != obj.id]

# Query proxy for model classes
class QueryProxy:
    """Provides SQLAlchemy-like query interface for models"""
    def __init__(self, model_class, results=None):
        self.model_class = model_class
        self.table_name = getattr(model_class, '__tablename__', model_class.__name__.lower())
        self._results = results
    
    def filter_by(self, **kwargs):
        """Filter by column values"""
        results = _storage.get(self.table_name, [])
        for key, value in kwargs.items():
            results = [obj for obj in results if getattr(obj, key, None) == value]
        return QueryProxy(self.model_class, results)
    
    def filter(self, *args):
        """Generic filter (simplified - returns all for now)"""
        return QueryProxy(self.model_class, _storage.get(self.table_name, []))
    
    def get(self, obj_id):
        """Get object by ID"""
        results = _storage.get(self.table_name, [])
        for obj in results:
            if obj.id == obj_id:
                return obj
        return None
    
    def first(self):
        """Get first result"""
        results = self._results if self._results is not None else _storage.get(self.table_name, [])
        return results[0] if results else None
    
    def all(self):
        """Get all results"""
        return self._results if self._results is not None else _storage.get(self.table_name, [])
    
    def order_by(self, *args):
        """Order by (simplified - returns self for chaining)"""
        return self
    
    def __iter__(self):
        """Allow iteration over results"""
        return iter(self._results if self._results is not None else _storage.get(self.table_name, []))


# Dummy database for compatibility with Flask-SQLAlchemy free imports
class DummyDB:
    def __init__(self):
        self.session = MockSession()
    
    def init_app(self, app):
        pass

db = DummyDB()

class UserRole(Enum):
    FARMER = "farmer"
    ADMIN = "admin"
    EXPERT = "expert"

# Base model class with .query support
class ModelBase:
    """Base class for all models with .query support"""
    __tablename__ = None
    _id_counter = {}
    
    def __init__(self, **kwargs):
        if self.__class__.__name__ not in self._id_counter:
            self._id_counter[self.__class__.__name__] = 0
        self._id_counter[self.__class__.__name__] += 1
        self.id = self._id_counter[self.__class__.__name__]
        
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}


class User(ModelBase):
    __tablename__ = 'users'
    
    def __init__(self, username, email, password_hash, role=UserRole.FARMER, phone=None, address=None):
        super().__init__()
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.phone = phone
        self.address = address
        self.created_at = datetime.utcnow()
        self.farms = []
        self.alerts = []

User.query = QueryProxy(User)


class Farm(ModelBase):
    __tablename__ = 'farms'
    
    def __init__(self, user_id, name, location, latitude=None, longitude=None, area=None, soil_type=None):
        super().__init__()
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

Farm.query = QueryProxy(Farm)


class Crop(ModelBase):
    __tablename__ = 'crops'
    
    def __init__(self, farm_id, crop_name, variety=None, planting_date=None, expected_harvest=None, area=None):
        super().__init__()
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

Crop.query = QueryProxy(Crop)


class SensorReading(ModelBase):
    __tablename__ = 'sensor_readings'
    
    def __init__(self, farm_id, sensor_type, value, unit=None, location=None):
        super().__init__()
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

SensorReading.query = QueryProxy(SensorReading)


class DiseaseDetection(ModelBase):
    __tablename__ = 'disease_detections'
    
    def __init__(self, crop_id, disease_name=None, disease_confidence=None, severity='mild'):
        super().__init__()
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

DiseaseDetection.query = QueryProxy(DiseaseDetection)


class Recommendation(ModelBase):
    __tablename__ = 'recommendations'
    
    def __init__(self, crop_id, recommendation_type, reason=None, priority='medium'):
        super().__init__()
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

Recommendation.query = QueryProxy(Recommendation)


class Alert(ModelBase):
    __tablename__ = 'alerts'
    
    def __init__(self, user_id, alert_type, title, message, severity='info', farm_id=None):
        super().__init__()
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

Alert.query = QueryProxy(Alert)


class IrrigationControl(ModelBase):
    __tablename__ = 'irrigation_control'
    
    def __init__(self, farm_id, is_automated=False, moisture_threshold=40.0):
        super().__init__()
        self.farm_id = farm_id
        self.is_automated = is_automated
        self.moisture_threshold = moisture_threshold
        self.max_water_per_day = None
        self.is_motor_on = False
        self.motor_on_time = None
        self.motor_off_time = None
        self.last_irrigation = None
        self.updated_at = datetime.utcnow()

IrrigationControl.query = QueryProxy(IrrigationControl)


class MarketData(ModelBase):
    __tablename__ = 'market_data'
    
    def __init__(self, crop_name, location, current_price=None):
        super().__init__()
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

MarketData.query = QueryProxy(MarketData)


class YieldPrediction(ModelBase):
    __tablename__ = 'yield_predictions'
    
    def __init__(self, crop_id, predicted_yield=None, confidence_score=0.0):
        super().__init__()
        self.crop_id = crop_id
        self.predicted_yield = predicted_yield
        self.confidence_score = confidence_score
        self.prediction_model = 'default'
        self.factors = '{}'
        self.predicted_on = datetime.utcnow()

YieldPrediction.query = QueryProxy(YieldPrediction)


class ChatHistory(ModelBase):
    __tablename__ = 'chat_history'
    
    def __init__(self, user_id, user_message, bot_response, intent=None):
        super().__init__()
        self.user_id = user_id
        self.user_message = user_message
        self.bot_response = bot_response
        self.intent = intent
        self.confidence = 0.0
        self.timestamp = datetime.utcnow()

ChatHistory.query = QueryProxy(ChatHistory)
