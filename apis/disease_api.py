from flask import Blueprint, request, jsonify, current_app
from models.database import db, DiseaseDetection, Crop

disease_bp = Blueprint('disease', __name__)

@disease_bp.route('/<int:crop_id>/detect', methods=['POST'])
def detect_disease(crop_id):
    """Detect disease from image"""
    crop = Crop.query.get(crop_id)
    if not crop:
        return jsonify({'message': 'Crop not found'}), 404
    
    file = request.files.get('image')
    if not file:
        return jsonify({'message': 'No image provided'}), 400
    
    # Save image and run detection
    filename = f"disease_{crop_id}_{int(__import__('time').time())}.jpg"
    filepath = f"static/uploads/{filename}"
    file.save(filepath)
    
    # Use AI model for detection
    result = current_app.disease_model.predict_disease(filepath)
    
    # Save detection to database
    detection = DiseaseDetection(
        crop_id=crop_id,
        image_path=filename,
        disease_name=result.get('disease'),
        disease_confidence=result.get('confidence'),
        pest_detected=result.get('pest_detected'),
        severity=result.get('severity'),
        status='active'
    )
    
    db.session.add(detection)
    
    # Update crop health score
    if result.get('confidence', 0) > 0.5:
        crop.current_health_score = max(0, crop.current_health_score - (result.get('confidence', 0) * 30))
    
    db.session.commit()
    
    return jsonify({
        'detection_id': detection.id,
        'disease': result.get('disease'),
        'confidence': result.get('confidence'),
        'severity': result.get('severity'),
        'pest_detected': result.get('pest_detected'),
        'crop_health_updated': crop.current_health_score
    }), 201

@disease_bp.route('/<int:crop_id>/history', methods=['GET'])
def disease_history(crop_id):
    """Get disease detection history"""
    detections = DiseaseDetection.query.filter_by(crop_id=crop_id).all()
    detections = sorted(detections, key=lambda d: d.detected_at, reverse=True)
    
    return jsonify([{
        'id': d.id,
        'disease': d.disease_name,
        'confidence': d.disease_confidence,
        'severity': d.severity,
        'detected_at': d.detected_at.isoformat(),
        'status': d.status
    } for d in detections])
