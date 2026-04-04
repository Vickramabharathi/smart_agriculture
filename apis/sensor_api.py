from flask import Blueprint, request, jsonify
from models.database import db, SensorReading
from datetime import datetime, timedelta
import random

sensor_bp = Blueprint('sensors', __name__)

@sensor_bp.route('/<int:farm_id>/read', methods=['GET'])
def get_sensor_readings(farm_id):
    """Get all sensor readings for a farm"""
    hours = request.args.get('hours', 24, type=int)
    since = datetime.utcnow() - timedelta(hours=hours)
    
    readings = SensorReading.query.filter(
        SensorReading.farm_id == farm_id,
        SensorReading.timestamp >= since
    ).order_by(SensorReading.timestamp.desc()).all()
    
    return jsonify({
        'farm_id': farm_id,
        'readings': [{
            'id': r.id,
            'sensor_type': r.sensor_type,
            'value': r.value,
            'unit': r.unit,
            'location': r.location,
            'timestamp': r.timestamp.isoformat()
        } for r in readings]
    })

@sensor_bp.route('/<int:farm_id>/simulate', methods=['POST'])
def simulate_sensors(farm_id):
    """Simulate sensor data (for testing IoT integration)"""
    sensors = ['moisture', 'temperature', 'humidity', 'ph', 'water_level']
    ranges = {
        'moisture': (20, 80),
        'temperature': (15, 35),
        'humidity': (30, 90),
        'ph': (5, 8),
        'water_level': (10, 100)
    }
    
    new_readings = []
    for sensor_type in sensors:
        min_val, max_val = ranges[sensor_type]
        value = random.uniform(min_val, max_val)
        
        reading = SensorReading(
            farm_id=farm_id,
            sensor_type=sensor_type,
            value=round(value, 2),
            unit={'moisture': '%', 'temperature': '°C', 'humidity': '%', 'ph': 'pH', 'water_level': 'mm'}.get(sensor_type),
            location='Field A'
        )
        db.session.add(reading)
        new_readings.append(reading)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Sensor data simulated',
        'farm_id': farm_id,
        'readings': [r.to_dict() for r in new_readings]
    }), 201
