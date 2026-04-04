from flask import Blueprint, request, jsonify
from models.database import db, MarketData
from datetime import datetime, timedelta
import requests
import random

marketplace_bp = Blueprint('marketplace', __name__)

# Mock market data for Indian crops (in production, integrate with real APIs)
MOCK_MARKET_DATA = {
    'wheat': {
        'current_price': 2200,  # per quintal
        'trend': 'up',
        'change_percent': 2.5,
        'best_selling_months': ['March', 'April', 'May'],
        'demand': 'high'
    },
    'rice': {
        'current_price': 2800,
        'trend': 'stable',
        'change_percent': 0.8,
        'best_selling_months': ['October', 'November', 'December'],
        'demand': 'high'
    },
    'cotton': {
        'current_price': 6500,
        'trend': 'down',
        'change_percent': -1.2,
        'best_selling_months': ['January', 'February', 'March'],
        'demand': 'medium'
    },
    'sugarcane': {
        'current_price': 320,
        'trend': 'up',
        'change_percent': 3.1,
        'best_selling_months': ['November', 'December', 'January'],
        'demand': 'high'
    },
    'maize': {
        'current_price': 1800,
        'trend': 'stable',
        'change_percent': -0.5,
        'best_selling_months': ['June', 'July', 'August'],
        'demand': 'medium'
    },
    'soybean': {
        'current_price': 4200,
        'trend': 'up',
        'change_percent': 1.8,
        'best_selling_months': ['February', 'March', 'April'],
        'demand': 'high'
    }
}

@marketplace_bp.route('/prices', methods=['GET'])
def get_crop_prices():
    """Get current market prices for all crops"""
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'prices': MOCK_MARKET_DATA,
        'currency': 'INR per quintal'
    })

@marketplace_bp.route('/prices/<crop_name>', methods=['GET'])
def get_crop_price(crop_name):
    """Get detailed price information for a specific crop"""
    crop_name = crop_name.lower()

    if crop_name not in MOCK_MARKET_DATA:
        return jsonify({'error': f'Price data not available for {crop_name}'}), 404

    data = MOCK_MARKET_DATA[crop_name]

    # Generate historical price data (last 30 days)
    historical_prices = []
    base_price = data['current_price']
    current_date = datetime.now()

    for i in range(30, 0, -1):
        date = current_date - timedelta(days=i)
        # Add some random variation
        variation = random.uniform(-0.1, 0.1)  # ±10%
        price = base_price * (1 + variation)
        historical_prices.append({
            'date': date.strftime('%Y-%m-%d'),
            'price': round(price, 2)
        })

    return jsonify({
        'crop': crop_name,
        'current_price': data['current_price'],
        'trend': data['trend'],
        'change_percent': data['change_percent'],
        'best_selling_months': data['best_selling_months'],
        'demand': data['demand'],
        'historical_prices': historical_prices,
        'currency': 'INR per quintal',
        'last_updated': datetime.now().isoformat()
    })

@marketplace_bp.route('/trends', methods=['GET'])
def get_market_trends():
    """Get overall market trends and insights"""
    # Calculate average changes
    total_change = sum(data['change_percent'] for data in MOCK_MARKET_DATA.values())
    avg_change = total_change / len(MOCK_MARKET_DATA)

    # Count trends
    trends = {'up': 0, 'down': 0, 'stable': 0}
    for data in MOCK_MARKET_DATA.values():
        trends[data['trend']] += 1

    # Get top performing crops
    top_performers = sorted(
        MOCK_MARKET_DATA.items(),
        key=lambda x: x[1]['change_percent'],
        reverse=True
    )[:3]

    return jsonify({
        'overall_trend': 'bullish' if avg_change > 0 else 'bearish',
        'average_change_percent': round(avg_change, 2),
        'trend_distribution': trends,
        'top_performers': [
            {'crop': crop, 'change_percent': data['change_percent']}
            for crop, data in top_performers
        ],
        'market_insights': [
            "Wheat and sugarcane showing strong upward trends",
            "Cotton prices slightly down due to increased supply",
            "Rice maintaining stable prices with high demand",
            "Consider selling wheat in March-May for best returns"
        ],
        'timestamp': datetime.now().isoformat()
    })

@marketplace_bp.route('/recommendations/<crop_name>', methods=['GET'])
def get_selling_recommendations(crop_name):
    """Get selling recommendations for a specific crop"""
    crop_name = crop_name.lower()

    if crop_name not in MOCK_MARKET_DATA:
        return jsonify({'error': f'No recommendations available for {crop_name}'}), 404

    data = MOCK_MARKET_DATA[crop_name]
    current_month = datetime.now().strftime('%B')

    recommendations = []

    # Price-based recommendations
    if data['trend'] == 'up':
        recommendations.append(f"📈 {crop_name.title()} prices are trending upward. Consider holding for better returns.")
    elif data['trend'] == 'down':
        recommendations.append(f"📉 {crop_name.title()} prices are declining. Consider selling soon to avoid further losses.")
    else:
        recommendations.append(f"➡️ {crop_name.title()} prices are stable. Good time for planned sales.")

    # Seasonal recommendations
    if current_month in data['best_selling_months']:
        recommendations.append(f"🌟 Currently in peak season for {crop_name}. Excellent time to sell!")
    else:
        next_best_month = data['best_selling_months'][0]
        recommendations.append(f"⏰ Best selling months: {', '.join(data['best_selling_months'])}. Next optimal period starts in {next_best_month}.")

    # Demand-based recommendations
    if data['demand'] == 'high':
        recommendations.append(f"🔥 High demand for {crop_name}. Prices likely to remain strong.")
    elif data['demand'] == 'medium':
        recommendations.append(f"⚖️ Moderate demand for {crop_name}. Monitor market closely.")
    else:
        recommendations.append(f"📊 Low demand for {crop_name}. Consider storage or alternative markets.")

    return jsonify({
        'crop': crop_name,
        'recommendations': recommendations,
        'current_price': data['current_price'],
        'trend': data['trend'],
        'best_selling_months': data['best_selling_months'],
        'current_month': current_month,
        'timestamp': datetime.now().isoformat()
    })

@marketplace_bp.route('/alerts', methods=['GET'])
def get_market_alerts():
    """Get important market alerts and notifications"""
    alerts = []

    # Generate some mock alerts based on trends
    for crop, data in MOCK_MARKET_DATA.items():
        if data['change_percent'] > 2:
            alerts.append({
                'type': 'price_increase',
                'crop': crop,
                'message': f"{crop.title()} prices increased by {data['change_percent']}%",
                'priority': 'high'
            })
        elif data['change_percent'] < -2:
            alerts.append({
                'type': 'price_decrease',
                'crop': crop,
                'message': f"{crop.title()} prices decreased by {abs(data['change_percent'])}%",
                'priority': 'medium'
            })

    # Seasonal alerts
    current_month = datetime.now().strftime('%B')
    for crop, data in MOCK_MARKET_DATA.items():
        if current_month in data['best_selling_months']:
            alerts.append({
                'type': 'seasonal_opportunity',
                'crop': crop,
                'message': f"Peak selling season for {crop} - maximize profits now!",
                'priority': 'high'
            })

    return jsonify({
        'alerts': alerts,
        'total_alerts': len(alerts),
        'timestamp': datetime.now().isoformat()
    })