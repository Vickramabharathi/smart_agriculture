from flask import Blueprint, request, jsonify, current_app
from models.database import db, Farm, Crop, SensorReading, YieldPrediction, MarketData
from datetime import datetime, timedelta
from sqlalchemy import func

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/<int:farm_id>/overview', methods=['GET'])
def farm_overview(farm_id):
    """Get comprehensive farm analytics"""
    farm = Farm.query.get(farm_id)
    if not farm:
        return jsonify({'message': 'Farm not found'}), 404
    
    crops = Crop.query.filter_by(farm_id=farm_id).all()
    
    # Get average sensor readings from last 7 days
    week_ago = datetime.utcnow() - timedelta(days=7)
    sensors = SensorReading.query.filter(
        SensorReading.farm_id == farm_id,
        SensorReading.timestamp >= week_ago
    ).all()
    
    # Calculate averages by sensor type
    sensor_stats = {}
    for sensor_type in ['moisture', 'temperature', 'humidity', 'ph', 'water_level']:
        readings = [s.value for s in sensors if s.sensor_type == sensor_type]
        if readings:
            sensor_stats[sensor_type] = {
                'avg': round(sum(readings) / len(readings), 2),
                'min': min(readings),
                'max': max(readings),
                'latest': readings[-1]
            }
    
    avg_health = sum([c.current_health_score for c in crops]) / len(crops) if crops else 0
    
    return jsonify({
        'farm_id': farm_id,
        'farm_name': farm.name,
        'total_crops': len(crops),
        'avg_health_score': round(avg_health, 2),
        'sensor_statistics': sensor_stats,
        'area_hectares': farm.area
    })

@analytics_bp.route('/<int:crop_id>/yield-prediction', methods=['GET'])
def yield_forecast(crop_id):
    """Get yield prediction for a crop"""
    crop = Crop.query.get(crop_id)
    if not crop:
        return jsonify({'message': 'Crop not found'}), 404
    
    # Get sensor data for past 30 days
    month_ago = datetime.utcnow() - timedelta(days=30)
    sensors = SensorReading.query.filter(
        SensorReading.farm_id == crop.farm_id,
        SensorReading.timestamp >= month_ago
    ).all()
    
    # Extract averages
    moisture_readings = [s.value for s in sensors if s.sensor_type == 'moisture']
    temp_readings = [s.value for s in sensors if s.sensor_type == 'temperature']
    humidity_readings = [s.value for s in sensors if s.sensor_type == 'humidity']
    
    moisture_avg = sum(moisture_readings) / len(moisture_readings) if moisture_readings else 50
    temp_avg = sum(temp_readings) / len(temp_readings) if temp_readings else 25
    humidity_avg = sum(humidity_readings) / len(humidity_readings) if humidity_readings else 60
    
    days_since_planting = (datetime.utcnow() - crop.planting_date).days if crop.planting_date else 45
    
    # Use AI model for prediction
    prediction = current_app.yield_predictor.predict_yield(
        crop.crop_name,
        moisture_avg,
        temp_avg,
        humidity_avg,
        600,  # rainfall mm
        days_since_planting
    )
    
    # Save prediction
    yield_pred = YieldPrediction(
        crop_id=crop_id,
        predicted_yield=prediction['predicted_yield_tons'],
        confidence_score=prediction['confidence_score'],
        prediction_model='RandomForest',
        factors=str(prediction['factors_used'])
    )
    db.session.add(yield_pred)
    db.session.commit()
    
    return jsonify({
        'crop_id': crop_id,
        'crop_name': crop.crop_name,
        'predicted_yield_tons': prediction['predicted_yield_tons'],
        'confidence': prediction['confidence_score'],
        'factors': prediction['factors_used'],
        'prediction_id': yield_pred.id
    }), 201

@analytics_bp.route('/<int:crop_id>/market-info', methods=['GET'])
def market_intelligence(crop_id):
    """Get market information for a crop"""
    crop = Crop.query.get(crop_id)
    if not crop:
        return jsonify({'message': 'Crop not found'}), 404
    
    # Get market data for this crop
    market_data = MarketData.query.filter_by(crop_name=crop.crop_name).order_by(
        MarketData.last_updated.desc()
    ).first()
    
    if not market_data:
        # Return sample data
        return jsonify({
            'crop': crop.crop_name,
            'status': 'no_data',
            'message': 'Market data not available for this crop'
        })
    
    # Provide selling recommendations
    recommendation = 'Hold' if market_data.trend == 'down' else 'Sell' if market_data.trend == 'up' else 'Monitor'
    
    return jsonify({
        'crop': crop.crop_name,
        'current_price': f"₹{market_data.current_price}/kg",
        'price_range_30days': f"₹{market_data.min_price_30days} - ₹{market_data.max_price_30days}",
        'trend': market_data.trend,
        'recommendation': recommendation,
        'volume_available': market_data.volume_available,
        'quality_grade': market_data.quality_grade,
        'last_updated': market_data.last_updated.isoformat()
    })

@analytics_bp.route('/<int:farm_id>/alerts-summary', methods=['GET'])
def alerts_summary(farm_id):
    """Get summary of active alerts"""
    from models.database import Alert
    
    farm = Farm.query.get(farm_id)
    if not farm:
        return jsonify({'message': 'Farm not found'}), 404
    
    alerts = Alert.query.filter_by(farm_id=farm_id).order_by(
        Alert.created_at.desc()
    ).limit(10).all()
    
    return jsonify({
        'farm_id': farm_id,
        'total_alerts': len(alerts),
        'recent_alerts': [{
            'id': a.id,
            'type': a.alert_type,
            'title': a.title,
            'severity': a.severity,
            'is_predictive': a.is_predictive,
            'is_read': a.is_read,
            'created_at': a.created_at.isoformat()
        } for a in alerts[:5]]
    })

@analytics_bp.route('/<int:farm_id>/pest-risk', methods=['GET'])
def pest_risk_assessment(farm_id):
    """Get pest attack risk prediction"""
    farm = Farm.query.get(farm_id)
    if not farm:
        return jsonify({'message': 'Farm not found'}), 404
    
    crop = Crop.query.filter_by(farm_id=farm_id).first()
    if not crop:
        return jsonify({'message': 'No crop found'}), 404
    
    # Get current weather conditions
    week_ago = datetime.utcnow() - timedelta(days=7)
    sensors = SensorReading.query.filter(
        SensorReading.farm_id == farm_id,
        SensorReading.timestamp >= week_ago
    ).all()
    
    temp_readings = [s.value for s in sensors if s.sensor_type == 'temperature']
    humidity_readings = [s.value for s in sensors if s.sensor_type == 'humidity']
    
    temp_avg = sum(temp_readings) / len(temp_readings) if temp_readings else 25
    humidity_avg = sum(humidity_readings) / len(humidity_readings) if humidity_readings else 60
    
    # Pest risk prediction
    risk = current_app.pest_predictor.predict_pest_risk(
        crop.crop_name,
        temp_avg,
        humidity_avg,
        150  # rainfall mm
    )
    
    return jsonify({
        'farm_id': farm_id,
        'crop': crop.crop_name,
        'risk_level': risk['risk_level'],
        'risk_score': risk['risk_score'],
        'predicted_pests': risk['predicted_pests'],
        'preventive_measures': risk['preventive_measures'],
        'current_temp': temp_avg,
        'current_humidity': humidity_avg
    })
