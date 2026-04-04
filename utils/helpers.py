from functools import wraps
from flask import jsonify, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from enum import Enum

def token_required(f):
    """JWT token decorator for API endpoints"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            token = token.split(" ")[1]  # Extract token from "Bearer <token>"
            data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        return f(current_user_id, *args, **kwargs)
    
    return decorated

def role_required(required_roles):
    """Check if user has required role"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Get user from token and check role
            # Implementation depends on your auth system
            return f(*args, **kwargs)
        return decorated
    return decorator

def hash_password(password):
    """Hash password using werkzeug"""
    return generate_password_hash(password)

def check_password(hashed_password, password):
    """Verify password against hash"""
    return check_password_hash(hashed_password, password)

def generate_token(user_id, expires_in=86400):
    """Generate JWT token"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=expires_in)
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class AlertType(Enum):
    """Alert types"""
    DISEASE = "disease"
    PEST = "pest"
    WEATHER = "weather"
    SENSOR = "sensor"
    AUTOMATION = "automation"
    MARKET = "market"

def send_sms_alert(phone_number, message):
    """Send SMS alert using Twilio"""
    try:
        from twilio.rest import Client
        from flask import current_app
        
        account_sid = current_app.config.get('TWILIO_ACCOUNT_SID')
        auth_token = current_app.config.get('TWILIO_AUTH_TOKEN')
        twilio_phone = current_app.config.get('TWILIO_PHONE')
        
        if not all([account_sid, auth_token, twilio_phone]):
            print("Twilio credentials not configured")
            return False
        
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message[:160],  # SMS limit
            from_=twilio_phone,
            to=phone_number
        )
        return True
    except Exception as e:
        print(f"SMS Error: {str(e)}")
        return False

def send_email_alert(email, subject, body):
    """Send email alert"""
    try:
        from flask_mail import Mail, Message
        from flask import current_app
        
        mail = Mail(current_app)
        msg = Message(subject, recipients=[email], body=body)
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Email Error: {str(e)}")
        return False

def get_sensor_statistics(sensor_readings):
    """Calculate statistics from sensor readings"""
    if not sensor_readings:
        return None
    
    values = [reading.value for reading in sensor_readings]
    
    return {
        'min': min(values),
        'max': max(values),
        'avg': sum(values) / len(values),
        'latest': values[-1],
        'count': len(values)
    }

def format_recommendation(recommendation):
    """Format recommendation for display"""
    if recommendation.recommendation_type == 'fertilizer':
        return {
            'type': 'Fertilizer Application',
            'npk': f"{recommendation.npk_nitrogen}:{recommendation.npk_phosphorus}:{recommendation.npk_potassium}",
            'fertilizer': recommendation.fertilizer_name,
            'reason': recommendation.reason,
            'priority': recommendation.priority
        }
    elif recommendation.recommendation_type == 'irrigation':
        return {
            'type': 'Irrigation Schedule',
            'amount': f"{recommendation.irrigation_amount}L",
            'schedule': recommendation.irrigation_schedule,
            'reason': recommendation.reason,
            'priority': recommendation.priority
        }
    elif recommendation.recommendation_type == 'crop_change':
        return {
            'type': 'Crop Recommendation',
            'suggested_crop': recommendation.recommended_crop,
            'compatibility': f"{recommendation.compatibility_score * 100:.1f}%",
            'reason': recommendation.reason
        }
    
    return recommendation.to_dict() if hasattr(recommendation, 'to_dict') else {}

def validate_file_upload(file, allowed_extensions):
    """Validate uploaded file"""
    if file.filename == '':
        return False, 'No file selected'
    
    if not file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
        return False, f'File type not allowed. Allowed: {", ".join(allowed_extensions)}'
    
    return True, 'Valid file'

def calculate_crop_health_score(disease_confidence, pest_detected, soil_moisture, temperature):
    """Calculate overall crop health score (0-100)"""
    score = 100
    
    # Deduct based on disease
    score -= (disease_confidence * 30) if disease_confidence > 0.5 else 0
    
    # Deduct for pest
    score -= 20 if pest_detected else 0
    
    # Adjust for soil moisture
    if soil_moisture < 30 or soil_moisture > 80:
        score -= 15
    
    # Adjust for temperature
    if temperature < 10 or temperature > 40:
        score -= 10
    
    return max(0, min(100, score))

def get_crop_growth_stage(planting_date):
    """Determine crop growth stage based on days since planting"""
    days_since = (datetime.utcnow() - planting_date).days
    
    if days_since < 30:
        return 'seedling'
    elif days_since < 60:
        return 'vegetative'
    elif days_since < 90:
        return 'flowering'
    else:
        return 'fruiting'
