from flask import Blueprint, request, jsonify, current_app
from models.database import db, Crop, Recommendation, DiseaseDetection

crop_bp = Blueprint('crops', __name__)

@crop_bp.route('/<int:farm_id>', methods=['GET', 'POST'])
def manage_crops(farm_id):
    """Get or create crops for a farm"""
    if request.method == 'POST':
        data = request.get_json()
        crop = Crop(
            farm_id=farm_id,
            crop_name=data.get('crop_name'),
            variety=data.get('variety'),
            area=data.get('area')
        )
        db.session.add(crop)
        db.session.commit()
        return jsonify({'message': 'Crop created', 'crop_id': crop.id}), 201
    
    crops = Crop.query.filter_by(farm_id=farm_id).all()
    return jsonify([{
        'id': c.id,
        'name': c.crop_name,
        'variety': c.variety,
        'health_score': c.current_health_score
    } for c in crops])

@crop_bp.route('/<int:crop_id>/health', methods=['GET'])
def crop_health(crop_id):
    """Get crop health score and metrics"""
    crop = Crop.query.get(crop_id)
    if not crop:
        return jsonify({'message': 'Crop not found'}), 404
    
    # Get recent disease detections
    diseases = DiseaseDetection.query.filter_by(
        crop_id=crop_id, status='active'
    ).all()
    diseases = sorted(diseases, key=lambda d: d.detected_at, reverse=True)[:3]
    
    return jsonify({
        'crop_id': crop.id,
        'crop_name': crop.crop_name,
        'health_score': crop.current_health_score,
        'active_issues': [{
            'disease': d.disease_name,
            'confidence': d.disease_confidence,
            'severity': d.severity
        } for d in diseases]
    })
