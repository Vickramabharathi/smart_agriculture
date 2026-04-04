from flask import Blueprint, request, jsonify, current_app
from models.database import db, Farm, IrrigationControl, SensorReading
from datetime import datetime
from sqlalchemy import desc

irrigation_bp = Blueprint('irrigation', __name__)

@irrigation_bp.route('/<int:farm_id>/config', methods=['GET', 'POST'])
def irrigation_config(farm_id):
    """Get or set irrigation configuration"""
    farm = Farm.query.get(farm_id)
    if not farm:
        return jsonify({'message': 'Farm not found'}), 404
    
    config = IrrigationControl.query.filter_by(farm_id=farm_id).first()
    
    if request.method == 'POST':
        data = request.get_json()
        
        if not config:
            config = IrrigationControl(farm_id=farm_id)
        
        config.is_automated = data.get('is_automated', False)
        config.moisture_threshold = data.get('moisture_threshold', 40.0)
        config.max_water_per_day = data.get('max_water_per_day', 5000)
        config.updated_at = datetime.utcnow()
        
        db.session.add(config)
        db.session.commit()
        
        return jsonify({
            'message': 'Configuration updated',
            'farm_id': farm_id
        }), 200
    
    if not config:
        return jsonify({'message': 'No configuration found'}), 404
    
    return jsonify({
        'farm_id': farm_id,
        'is_automated': config.is_automated,
        'moisture_threshold': config.moisture_threshold,
        'max_water_per_day': config.max_water_per_day,
        'is_motor_on': config.is_motor_on
    })

@irrigation_bp.route('/<int:farm_id>/status', methods=['GET'])
def irrigation_status(farm_id):
    """Get irrigation system status"""
    config = IrrigationControl.query.filter_by(farm_id=farm_id).first()
    
    # Get latest moisture reading
    latest_moisture = SensorReading.query.filter_by(
        farm_id=farm_id,
        sensor_type='moisture'
    ).order_by(desc(SensorReading.timestamp)).first()
    
    if not config:
        return jsonify({'message': 'No configuration found'}), 404
    
    moisture_value = latest_moisture.value if latest_moisture else 50
    
    # Determine if irrigation needed
    needs_irrigation = moisture_value < config.moisture_threshold
    
    return jsonify({
        'farm_id': farm_id,
        'current_moisture': moisture_value,
        'threshold': config.moisture_threshold,
        'needs_irrigation': needs_irrigation,
        'motor_status': 'ON' if config.is_motor_on else 'OFF',
        'last_irrigation': config.last_irrigation.isoformat() if config.last_irrigation else None,
        'automated_mode': config.is_automated
    })

@irrigation_bp.route('/<int:farm_id>/control', methods=['POST'])
def control_motor(farm_id):
    """Manual motor control"""
    data = request.get_json()
    action = data.get('action')  # 'ON' or 'OFF'
    
    config = IrrigationControl.query.filter_by(farm_id=farm_id).first()
    if not config:
        return jsonify({'message': 'Configuration not found'}), 404
    
    if action == 'ON':
        config.is_motor_on = True
        config.motor_on_time = datetime.utcnow()
        config.last_irrigation = datetime.utcnow()
    elif action == 'OFF':
        config.is_motor_on = False
        config.motor_off_time = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'message': f'Motor turned {action}',
        'farm_id': farm_id,
        'motor_status': action
    })

@irrigation_bp.route('/<int:farm_id>/schedule', methods=['GET'])
def irrigation_schedule(farm_id):
    """Get AI-optimized irrigation schedule"""
    from models.database import Crop
    
    farm = Farm.query.get(farm_id)
    if not farm:
        return jsonify({'message': 'Farm not found'}), 404
    
    crop = Crop.query.filter_by(farm_id=farm_id).first()
    if not crop:
        return jsonify({'message': 'No crop found'}), 404
    
    # Get latest sensor readings
    moisture = SensorReading.query.filter_by(
        farm_id=farm_id, sensor_type='moisture'
    ).order_by(desc(SensorReading.timestamp)).first()
    
    schedule = current_app.irrigation_optimizer.calculate_irrigation_schedule(
        crop.crop_name,
        moisture.value if moisture else 50,
        20,  # rainfall forecast mm
        (datetime.utcnow() - crop.planting_date).days if crop.planting_date else 30
    )
    
    return jsonify({
        'farm_id': farm_id,
        'crop': crop.crop_name,
        'schedule': schedule
    })
