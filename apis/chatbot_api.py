from flask import Blueprint, request, jsonify
from models.database import db, ChatHistory, User

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/query', methods=['POST'])
def chatbot_query():
    """Handle farmer queries via NLP chatbot"""
    data = request.get_json()
    user_id = data.get('user_id')
    query = data.get('message')
    
    if not user_id or not query:
        return jsonify({'message': 'Missing user_id or message'}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # AI-based response generation (placeholder)
    response, intent, confidence = generate_bot_response(query)
    
    # Save to chat history
    chat = ChatHistory(
        user_id=user_id,
        user_message=query,
        bot_response=response,
        intent=intent,
        confidence=confidence
    )
    db.session.add(chat)
    db.session.commit()
    
    return jsonify({
        'chat_id': chat.id,
        'user_message': query,
        'bot_response': response,
        'intent': intent,
        'confidence': confidence
    }), 201

@chatbot_bp.route('/history/<int:user_id>', methods=['GET'])
def chat_history(user_id):
    """Get chat history for user"""
    chats = ChatHistory.query.filter_by(user_id=user_id).all()
    chats = sorted(chats, key=lambda c: c.timestamp, reverse=True)[:50]
    
    return jsonify([{
        'id': c.id,
        'user_message': c.user_message,
        'bot_response': c.bot_response,
        'intent': c.intent,
        'timestamp': c.timestamp.isoformat()
    } for c in chats])

def generate_bot_response(query):
    """
    Generate response using NLP
    In production, use BERT/Transformers from Hugging Face
    """
    query_lower = query.lower()
    
    # Simple intent detection
    if any(word in query_lower for word in ['yellow leaf', 'brown spot', 'disease', 'infection']):
        intent = 'disease_diagnosis'
        response = """I detect you're asking about crop disease. 
        - Yellow leaves often indicate nitrogen deficiency
        - Brown spots may suggest fungal infection
        
        Please upload a photo of the affected leaf for AI analysis. 
        I recommend:
        1. Scout your fields daily
        2. Remove infected leaves
        3. Apply appropriate fungicide if confirmed
        
        Would you like me to analyze an image?"""
        confidence = 0.85
    
    elif any(word in query_lower for word in ['fertilizer', 'npk', 'nutrient', 'soil']):
        intent = 'fertilizer_recommendation'
        response = """For fertilizer recommendations, I'll need:
        1. Your soil test results (N, P, K levels)
        2. Current crop type and growth stage
        3. Previous crop history
        
        Based on standard practices:
        - Rice: NPK 100:40:40
        - Wheat: NPK 120:50:40
        - Cotton: NPK 150:75:75
        
        Do you have soil test data available?"""
        confidence = 0.80
    
    elif any(word in query_lower for word in ['water', 'irrigation', 'moisture', 'dry']):
        intent = 'irrigation_advice'
        response = """Irrigation recommendations:
        - Soil moisture should be 40-70% for most crops
        - Water when soil moisture drops below 35%
        - Avoid over-watering (>80% moisture)
        
        Optimal irrigation frequency:
        - Summer: Every 2-3 days
        - Winter: Every 5-7 days
        
        Check your soil moisture sensors for real-time data."""
        confidence = 0.82
    
    elif any(word in query_lower for word in ['pest', 'insect', 'worm', 'bug']):
        intent = 'pest_management'
        response = """For pest management:
        Common pests and solutions:
        - Stem borer: Neem oil spray, remove infected stems
        - Whitefly: Yellow traps, insecticidal soap
        - Bollworm: Pheromone traps, Bt spray
        
        Preventive measures:
        1. Field sanitation
        2. Crop rotation
        3. Remove crop residues
        
        What pest symptoms are you observing?"""
        confidence = 0.78
    
    else:
        intent = 'general_agriculture'
        response = """I'm your Smart Agriculture Assistant! I can help with:
        - Crop disease diagnosis
        - Fertilizer recommendations
        - Irrigation scheduling
        - Pest management
        - Yield predictions
        - Market information
        
        Please describe your farming challenge, and I'll provide specific guidance."""
        confidence = 0.60
    
    return response, intent, confidence
