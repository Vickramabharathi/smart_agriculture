from flask import Blueprint, request, jsonify
from models.database import db, Farm, SensorReading

farm_bp = Blueprint('farms', __name__)

@farm_bp.route('/', methods=['GET', 'POST'])
def manage_farms():
    """Get all farms or create new farm"""
    if request.method == 'POST':
        data = request.get_json() or {}
        user_id = data.get('user_id')
        name = data.get('name')
        location = data.get('location')

        if not user_id or not name or not location:
            return jsonify({'message': 'Missing required fields: user_id, name, location'}), 400

        farm = Farm(
            user_id=user_id,
            name=name,
            location=location,
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            area=data.get('area'),
            soil_type=data.get('soil_type')
        )
        db.session.add(farm)
        db.session.commit()
        return jsonify({'message': 'Farm created', 'farm_id': farm.id}), 201

    farms = Farm.query.all()
    return jsonify([{
        'id': f.id,
        'name': f.name,
        'location': f.location,
        'area': f.area,
        'soil_type': f.soil_type,
        'latitude': f.latitude,
        'longitude': f.longitude,
        'user_id': f.user_id
    } for f in farms])

@farm_bp.route('/<int:farm_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_farm(farm_id):
    farm = Farm.query.get(farm_id)
    if not farm:
        return jsonify({'message': 'Farm not found'}), 404

    if request.method == 'GET':
        return jsonify({
            'id': farm.id,
            'user_id': farm.user_id,
            'name': farm.name,
            'location': farm.location,
            'latitude': farm.latitude,
            'longitude': farm.longitude,
            'area': farm.area,
            'soil_type': farm.soil_type
        })

    if request.method == 'PUT':
        data = request.get_json() or {}
        farm.name = data.get('name', farm.name)
        farm.location = data.get('location', farm.location)
        farm.latitude = data.get('latitude', farm.latitude)
        farm.longitude = data.get('longitude', farm.longitude)
        farm.area = data.get('area', farm.area)
        farm.soil_type = data.get('soil_type', farm.soil_type)
        db.session.commit()
        return jsonify({'message': 'Farm updated', 'farm_id': farm.id})

    # DELETE
    db.session.delete(farm)
    db.session.commit()
    return jsonify({'message': 'Farm deleted'})

@farm_bp.route('/<int:farm_id>/dashboard', methods=['GET'])
def farm_dashboard(farm_id):
    """Get farm dashboard data"""
    farm = Farm.query.get(farm_id)
    if not farm:
        return jsonify({'message': 'Farm not found'}), 404

    sensors = SensorReading.query.filter_by(farm_id=farm_id).all()
    sensors = sorted(sensors, key=lambda s: s.timestamp, reverse=True)[:5]

    return jsonify({
        'farm_id': farm.id,
        'farm_name': farm.name,
        'location': farm.location,
        'soil_type': farm.soil_type,
        'recent_sensors': [{
            'type': s.sensor_type,
            'value': s.value,
            'unit': s.unit,
            'timestamp': s.timestamp.isoformat()
        } for s in sensors]
    })
