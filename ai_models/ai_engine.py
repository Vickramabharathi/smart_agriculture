import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import json

class DiseaseDetectionModel:
    """CNN-based disease detection using TensorFlow"""
    def __init__(self):
        self.model = None
        self.classes = ['healthy', 'leaf_spot', 'blight', 'rust', 'powdery_mildew', 'unknown']
    
    def predict_disease(self, image_path):
        """
        Predict disease from image
        Returns: disease_name, confidence_score
        """
        # Placeholder - In production, load TensorFlow model and preprocess image
        return {
            'disease': self.classes[0],
            'confidence': 0.95,
            'pest_detected': False,
            'severity': 'none'
        }

class CropRecommendationEngine:
    """Recommend best crops based on soil, climate, and weather"""
    def __init__(self):
        self.crop_database = {
            'rice': {'min_temp': 20, 'max_temp': 35, 'rainfall': 1000, 'soil_types': ['clay', 'loam']},
            'wheat': {'min_temp': 0, 'max_temp': 25, 'rainfall': 400, 'soil_types': ['loam', 'sandy_loam']},
            'sugarcane': {'min_temp': 20, 'max_temp': 35, 'rainfall': 750, 'soil_types': ['clay', 'loam']},
            'cotton': {'min_temp': 15, 'max_temp': 35, 'rainfall': 500, 'soil_types': ['loam', 'sandy_loam']},
            'maize': {'min_temp': 10, 'max_temp': 35, 'rainfall': 500, 'soil_types': ['loam', 'sandy_loam']},
            'groundnut': {'min_temp': 15, 'max_temp': 35, 'rainfall': 400, 'soil_types': ['sandy_loam', 'loam']},
        }
    
    def recommend_crops(self, soil_type, temp_min, temp_max, rainfall):
        """Recommend crops based on conditions"""
        recommendations = []
        
        for crop, requirements in self.crop_database.items():
            score = 0
            
            # Temperature score
            if requirements['min_temp'] <= temp_min and temp_max <= requirements['max_temp']:
                score += 40
            
            # Rainfall score
            if abs(rainfall - requirements['rainfall']) < requirements['rainfall'] * 0.3:
                score += 40
            
            # Soil score
            if soil_type in requirements['soil_types']:
                score += 20
            
            if score > 0:
                recommendations.append({
                    'crop': crop,
                    'score': score / 100.0,
                    'rationale': self._get_rationale(crop, score)
                })
        
        return sorted(recommendations, key=lambda x: x['score'], reverse=True)
    
    def _get_rationale(self, crop, score):
        if score >= 80:
            return f"{crop.capitalize()} is highly suitable for your farm conditions"
        elif score >= 60:
            return f"{crop.capitalize()} is moderately suitable for your farm"
        else:
            return f"{crop.capitalize()} might work but optimal conditions not met"

class FertilizerRecommendationEngine:
    """Recommend NPK-based fertilizer"""
    def __init__(self):
        self.crop_npk = {
            'rice': {'n': 100, 'p': 40, 'k': 40},
            'wheat': {'n': 120, 'p': 50, 'k': 40},
            'cotton': {'n': 150, 'p': 75, 'k': 75},
            'maize': {'n': 150, 'p': 60, 'k': 40},
            'sugarcane': {'n': 150, 'p': 75, 'k': 75},
        }
    
    def recommend_fertilizer(self, crop_name, soil_nitrogen, soil_phosphorus, soil_potassium, growth_stage):
        """
        Recommend fertilizer based on soil nutrients and crop stage
        growth_stage: 'seedling', 'vegetative', 'flowering', 'fruiting'
        """
        if crop_name not in self.crop_npk:
            return None
        
        required = self.crop_npk[crop_name]
        deficit = {
            'n': max(0, required['n'] - soil_nitrogen),
            'p': max(0, required['p'] - soil_phosphorus),
            'k': max(0, required['k'] - soil_potassium)
        }
        
        # Stage-wise adjustment
        stage_multiplier = {
            'seedling': 0.5,
            'vegetative': 1.0,
            'flowering': 1.2,
            'fruiting': 0.8
        }
        
        multiplier = stage_multiplier.get(growth_stage, 1.0)
        
        return {
            'npk_ratio': f"{int(deficit['n'])}:{int(deficit['p'])}:{int(deficit['k'])}",
            'nitrogen_kg': round(deficit['n'] * multiplier / 100, 2),
            'phosphorus_kg': round(deficit['p'] * multiplier / 100, 2),
            'potassium_kg': round(deficit['k'] * multiplier / 100, 2),
            'recommended_fertilizer': self._get_fertilizer_name(deficit),
            'application_frequency': 'bi-weekly' if growth_stage == 'vegetative' else 'weekly'
        }
    
    def _get_fertilizer_name(self, deficit):
        """Recommend specific fertilizer based on deficit"""
        if deficit['n'] > deficit['p'] and deficit['n'] > deficit['k']:
            return "Urea (46% N)"
        elif deficit['p'] > deficit['k']:
            return "DAP (18:46:0)"
        else:
            return "MOP (Muriate of Potash, 0:0:60)"

class YieldPredictionModel:
    """Predict crop yield using regression models"""
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
    
    def predict_yield(self, crop_name, moisture_avg, temp_avg, humidity_avg, rainfall, days_since_planting):
        """
        Predict yield based on environmental factors
        Returns: predicted_yield_tons, confidence_score
        """
        # Placeholder implementation
        # In production, would use trained ML model
        
        # Simple heuristic model for demonstration
        base_yield = {'rice': 5, 'wheat': 4, 'maize': 8, 'cotton': 2}.get(crop_name, 3)
        
        # Adjust based on conditions (0.7 to 1.3 multiplier)
        moisture_factor = 1.2 if 40 <= moisture_avg <= 70 else 0.8
        temp_factor = 1.1 if 25 <= temp_avg <= 32 else 0.9
        humidity_factor = 1.0 if 50 <= humidity_avg <= 80 else 0.9
        
        predicted_yield = base_yield * moisture_factor * temp_factor * humidity_factor
        
        return {
            'predicted_yield_tons': round(predicted_yield, 2),
            'confidence_score': 0.75,
            'factors_used': ['moisture', 'temperature', 'humidity', 'rainfall', 'crop_age']
        }

class IrrigationOptimizer:
    """Optimize irrigation schedule"""
    def __init__(self):
        self.crop_water_needs = {
            'rice': 1000,  # mm
            'wheat': 400,
            'cotton': 700,
            'maize': 500,
            'sugarcane': 1200,
        }
    
    def calculate_irrigation_schedule(self, crop_name, soil_moisture, rainfall_forecast, days_since_planting):
        """Calculate optimal irrigation schedule"""
        if crop_name not in self.crop_water_needs:
            return None
        
        total_needed = self.crop_water_needs[crop_name]
        current_water_deficit = max(0, total_needed - (soil_moisture * 10))  # rough calculation
        
        if rainfall_forecast > 20:  # mm
            return {
                'irrigate_now': False,
                'reason': f'Rain forecast of {rainfall_forecast}mm expected',
                'next_check': 2
            }
        
        if soil_moisture < 40:
            return {
                'irrigate_now': True,
                'water_amount': round(current_water_deficit, 2),
                'frequency': 'Every 2 days',
                'urgency': 'HIGH'
            }
        elif soil_moisture < 50:
            return {
                'irrigate_now': True,
                'water_amount': round(current_water_deficit * 0.5, 2),
                'frequency': 'Every 3 days',
                'urgency': 'MEDIUM'
            }
        else:
            return {
                'irrigate_now': False,
                'reason': 'Soil moisture adequate',
                'next_check': 3
            }

class PestPredictionModel:
    """Predict pest attack risk"""
    def __init__(self):
        pass
    
    def predict_pest_risk(self, crop_name, temperature, humidity, rainfall_30days):
        """
        Predict pest attack probability in next 3-7 days
        Returns: risk_level, pest_types, preventive_measures
        """
        # High humidity and moderate temp favor many pests
        risk_score = 0
        
        if 25 <= temperature <= 32 and humidity >= 70:
            risk_score += 40
        if rainfall_30days > 100:
            risk_score += 30
        
        risk_level = 'low' if risk_score < 30 else 'medium' if risk_score < 60 else 'high'
        
        pest_types = {
            'rice': ['stem_borer', 'leaf_folder', 'brown_plant_hopper'],
            'cotton': ['bollworm', 'whitefly', 'spider_mite'],
            'maize': ['stem_borer', 'fall_armyworm']
        }
        
        return {
            'risk_level': risk_level,
            'risk_score': min(100, risk_score),
            'predicted_pests': pest_types.get(crop_name, []),
            'preventive_measures': self._get_preventive_measures(risk_level)
        }
    
    def _get_preventive_measures(self, risk_level):
        if risk_level == 'high':
            return ['Scout fields daily', 'Consider spray of recommended pesticide', 'Monitor crop closely']
        elif risk_level == 'medium':
            return ['Scout fields regularly', 'Keep pesticides ready', 'Monitor weather']
        else:
            return ['Normal monitoring', 'Maintain field hygiene', 'Remove crop residues']
