from flask import Blueprint, request, jsonify, current_app
from models.database import db, Crop, Recommendation
from datetime import datetime

recommendation_bp = Blueprint('recommendations', __name__)

@recommendation_bp.route('/<int:crop_id>/fertilizer', methods=['GET', 'POST'])
def fertilizer_recommendation(crop_id):
    """Get or generate fertilizer recommendation"""
    crop = Crop.query.get(crop_id)
    if not crop:
        return jsonify({'message': 'Crop not found'}), 404
    
    if request.method == 'POST':
        data = request.get_json()
        
        # Generate recommendation using AI
        result = current_app.fertilizer_recommender.recommend_fertilizer(
            crop.crop_name,
            data.get('soil_nitrogen', 20),
            data.get('soil_phosphorus', 15),
            data.get('soil_potassium', 150),
            data.get('growth_stage', 'vegetative')
        )
        
        if result:
            rec = Recommendation(
                crop_id=crop_id,
                recommendation_type='fertilizer',
                npk_nitrogen=result['nitrogen_kg'],
                npk_phosphorus=result['phosphorus_kg'],
                npk_potassium=result['potassium_kg'],
                fertilizer_name=result['recommended_fertilizer'],
                reason='Based on soil analysis and crop requirements',
                priority='high'
            )
            db.session.add(rec)
            db.session.commit()
            
            return jsonify({
                'recommendation_id': rec.id,
                'npk': result['npk_ratio'],
                'fertilizer': result['recommended_fertilizer'],
                'application_frequency': result['application_frequency']
            }), 201
    
    # GET recommendations
    recommendations = Recommendation.query.filter_by(
        crop_id=crop_id,
        recommendation_type='fertilizer'
    ).order_by(Recommendation.created_at.desc()).limit(5).all()
    
    return jsonify([{
        'id': r.id,
        'fertilizer': r.fertilizer_name,
        'npk': f"{r.npk_nitrogen}:{r.npk_phosphorus}:{r.npk_potassium}",
        'created_at': r.created_at.isoformat()
    } for r in recommendations])

@recommendation_bp.route('/<int:crop_id>/crop-change', methods=['GET'])
def crop_recommendation(crop_id):
    """Get crop change recommendations"""
    crop = Crop.query.get(crop_id)
    if not crop:
        return jsonify({'message': 'Crop not found'}), 404
    
    farm = crop.farm
    
    # Generate crop recommendations
    recommendations = current_app.crop_recommender.recommend_crops(
        farm.soil_type or 'loam',
        25,  # min temp
        32,  # max temp
        800  # rainfall mm
    )
    
    return jsonify({
        'crop_id': crop_id,
        'current_crop': crop.crop_name,
        'recommendations': recommendations[:3]
    })

@recommendation_bp.route('/<int:crop_id>/all', methods=['GET'])
def all_recommendations(crop_id):
    """Get all active recommendations for a crop"""
    recommendations = Recommendation.query.filter_by(crop_id=crop_id).order_by(
        Recommendation.created_at.desc()
    ).all()
    
    return jsonify([{
        'id': r.id,
        'type': r.recommendation_type,
        'reason': r.reason,
        'priority': r.priority,
        'created_at': r.created_at.isoformat()
    } for r in recommendations])
