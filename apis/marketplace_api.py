from flask import Blueprint, request, jsonify
from models.database import db, MarketData
from datetime import datetime, timedelta
import requests
import random
import os
from config.config import Config

marketplace_bp = Blueprint('marketplace', __name__)

# API Configuration
MARKET_API_KEY = Config.MARKET_API_KEY
MARKET_API_BASE_URL = "https://api.marketdata.com/v1"  # Replace with actual API URL
FALLBACK_TO_MOCK = True  # Set to False in production

# Mock market data for Indian crops (fallback when API is unavailable)
MOCK_MARKET_DATA = {
    # Cereals/Grains
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
    'maize': {
        'current_price': 1800,
        'trend': 'stable',
        'change_percent': -0.5,
        'best_selling_months': ['June', 'July', 'August'],
        'demand': 'medium'
    },
    'barley': {
        'current_price': 1600,
        'trend': 'stable',
        'change_percent': 1.2,
        'best_selling_months': ['April', 'May', 'June'],
        'demand': 'medium'
    },
    'bajra': {
        'current_price': 1400,
        'trend': 'up',
        'change_percent': 1.8,
        'best_selling_months': ['September', 'October', 'November'],
        'demand': 'medium'
    },
    'jowar': {
        'current_price': 1300,
        'trend': 'stable',
        'change_percent': 0.5,
        'best_selling_months': ['January', 'February', 'March'],
        'demand': 'medium'
    },
    'ragi': {
        'current_price': 1500,
        'trend': 'up',
        'change_percent': 2.1,
        'best_selling_months': ['December', 'January', 'February'],
        'demand': 'medium'
    },

    # Pulses
    'chickpea': {
        'current_price': 4800,
        'trend': 'up',
        'change_percent': 3.2,
        'best_selling_months': ['January', 'February', 'March'],
        'demand': 'high'
    },
    'pigeon_pea': {
        'current_price': 5200,
        'trend': 'stable',
        'change_percent': 1.5,
        'best_selling_months': ['November', 'December', 'January'],
        'demand': 'high'
    },
    'lentil': {
        'current_price': 4500,
        'trend': 'up',
        'change_percent': 2.8,
        'best_selling_months': ['December', 'January', 'February'],
        'demand': 'high'
    },
    'peas': {
        'current_price': 3200,
        'trend': 'stable',
        'change_percent': 0.9,
        'best_selling_months': ['January', 'February', 'March'],
        'demand': 'medium'
    },
    'kidney_beans': {
        'current_price': 3800,
        'trend': 'up',
        'change_percent': 1.7,
        'best_selling_months': ['February', 'March', 'April'],
        'demand': 'medium'
    },
    'black_gram': {
        'current_price': 4200,
        'trend': 'stable',
        'change_percent': 1.1,
        'best_selling_months': ['January', 'February', 'March'],
        'demand': 'high'
    },
    'green_gram': {
        'current_price': 3800,
        'trend': 'up',
        'change_percent': 2.3,
        'best_selling_months': ['March', 'April', 'May'],
        'demand': 'medium'
    },

    # Oilseeds
    'soybean': {
        'current_price': 4200,
        'trend': 'up',
        'change_percent': 1.8,
        'best_selling_months': ['February', 'March', 'April'],
        'demand': 'high'
    },
    'groundnut': {
        'current_price': 5500,
        'trend': 'stable',
        'change_percent': 0.7,
        'best_selling_months': ['September', 'October', 'November'],
        'demand': 'high'
    },
    'mustard': {
        'current_price': 4800,
        'trend': 'up',
        'change_percent': 2.5,
        'best_selling_months': ['March', 'April', 'May'],
        'demand': 'high'
    },
    'sunflower': {
        'current_price': 4200,
        'trend': 'stable',
        'change_percent': 1.2,
        'best_selling_months': ['December', 'January', 'February'],
        'demand': 'medium'
    },
    'sesame': {
        'current_price': 6800,
        'trend': 'up',
        'change_percent': 1.9,
        'best_selling_months': ['January', 'February', 'March'],
        'demand': 'medium'
    },

    # Cash Crops
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
    'tobacco': {
        'current_price': 12000,
        'trend': 'stable',
        'change_percent': 0.8,
        'best_selling_months': ['January', 'February', 'March'],
        'demand': 'medium'
    },
    'jute': {
        'current_price': 3800,
        'trend': 'up',
        'change_percent': 2.1,
        'best_selling_months': ['July', 'August', 'September'],
        'demand': 'medium'
    },

    # Major Fruits
    'mango': {
        'current_price': 2500,
        'trend': 'up',
        'change_percent': 4.2,
        'best_selling_months': ['April', 'May', 'June'],
        'demand': 'high'
    },
    'banana': {
        'current_price': 1800,
        'trend': 'stable',
        'change_percent': 1.3,
        'best_selling_months': ['January', 'February', 'March'],
        'demand': 'high'
    },
    'apple': {
        'current_price': 3500,
        'trend': 'up',
        'change_percent': 2.7,
        'best_selling_months': ['August', 'September', 'October'],
        'demand': 'high'
    },
    'orange': {
        'current_price': 2200,
        'trend': 'stable',
        'change_percent': 0.9,
        'best_selling_months': ['December', 'January', 'February'],
        'demand': 'medium'
    },
    'grapes': {
        'current_price': 2800,
        'trend': 'up',
        'change_percent': 3.5,
        'best_selling_months': ['February', 'March', 'April'],
        'demand': 'high'
    },
    'pineapple': {
        'current_price': 1600,
        'trend': 'stable',
        'change_percent': 1.1,
        'best_selling_months': ['March', 'April', 'May'],
        'demand': 'medium'
    },
    'papaya': {
        'current_price': 1200,
        'trend': 'up',
        'change_percent': 2.2,
        'best_selling_months': ['January', 'February', 'March'],
        'demand': 'medium'
    },
    'guava': {
        'current_price': 1800,
        'trend': 'stable',
        'change_percent': 1.4,
        'best_selling_months': ['May', 'June', 'July'],
        'demand': 'medium'
    },
    'pomegranate': {
        'current_price': 3200,
        'trend': 'up',
        'change_percent': 2.9,
        'best_selling_months': ['September', 'October', 'November'],
        'demand': 'high'
    },

    # Major Vegetables
    'potato': {
        'current_price': 800,
        'trend': 'stable',
        'change_percent': 0.6,
        'best_selling_months': ['January', 'February', 'March'],
        'demand': 'high'
    },
    'tomato': {
        'current_price': 1200,
        'trend': 'up',
        'change_percent': 3.8,
        'best_selling_months': ['November', 'December', 'January'],
        'demand': 'high'
    },
    'onion': {
        'current_price': 1500,
        'trend': 'up',
        'change_percent': 4.1,
        'best_selling_months': ['January', 'February', 'March'],
        'demand': 'high'
    },
    'garlic': {
        'current_price': 2500,
        'trend': 'stable',
        'change_percent': 1.2,
        'best_selling_months': ['April', 'May', 'June'],
        'demand': 'medium'
    },
    'ginger': {
        'current_price': 2800,
        'trend': 'up',
        'change_percent': 2.4,
        'best_selling_months': ['January', 'February', 'March'],
        'demand': 'high'
    },

    # Major Spices
    'chili': {
        'current_price': 4500,
        'trend': 'up',
        'change_percent': 5.2,
        'best_selling_months': ['November', 'December', 'January'],
        'demand': 'high'
    },
    'turmeric': {
        'current_price': 5800,
        'trend': 'stable',
        'change_percent': 1.5,
        'best_selling_months': ['February', 'March', 'April'],
        'demand': 'high'
    },
    'coriander': {
        'current_price': 3200,
        'trend': 'up',
        'change_percent': 2.6,
        'best_selling_months': ['January', 'February', 'March'],
        'demand': 'medium'
    },
    'cumin': {
        'current_price': 6800,
        'trend': 'stable',
        'change_percent': 1.8,
        'best_selling_months': ['March', 'April', 'May'],
        'demand': 'high'
    },
    'fenugreek': {
        'current_price': 4200,
        'trend': 'up',
        'change_percent': 2.1,
        'best_selling_months': ['January', 'February', 'March'],
        'demand': 'medium'
    }
}

def fetch_real_market_data():
    """Fetch real market data from external API"""
    try:
        headers = {
            'Authorization': f'Bearer {MARKET_API_KEY}',
            'Content-Type': 'application/json'
        }

        # Fetch current prices for major crops
        response = requests.get(f"{MARKET_API_BASE_URL}/commodities/prices", headers=headers, timeout=10)

        if response.status_code == 200:
            api_data = response.json()
            return process_api_data(api_data)
        else:
            print(f"Market API error: {response.status_code} - {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Market API request failed: {str(e)}")
        return None
    except Exception as e:
        print(f"Market API processing error: {str(e)}")
        return None

def process_api_data(api_data):
    """Process raw API data into our format"""
    processed_data = {}

    # Map API crop names to our crop names
    crop_mapping = {
        # Cereals/Grains
        'wheat': ['wheat', 'गेहूं', 'गेहूं'],
        'rice': ['rice', 'धान', 'चावल'],
        'maize': ['maize', 'मक्का', 'मक्का'],
        'barley': ['barley', 'जौ'],
        'bajra': ['bajra', 'बाजरा'],
        'jowar': ['jowar', 'ज्वार'],
        'ragi': ['ragi', 'रागी'],

        # Pulses
        'chickpea': ['chickpea', 'chana', 'चना'],
        'pigeon_pea': ['pigeon_pea', 'tur', 'arhar', 'तूर', 'अरहर'],
        'lentil': ['lentil', 'masoor', 'मसूर'],
        'peas': ['peas', 'मटर'],
        'kidney_beans': ['kidney_beans', 'rajma', 'राजमा'],
        'black_gram': ['black_gram', 'urad', 'उड़द'],
        'green_gram': ['green_gram', 'moong', 'मूंग'],

        # Oilseeds
        'soybean': ['soybean', 'सोयाबीन'],
        'groundnut': ['groundnut', 'मूंगफली'],
        'mustard': ['mustard', 'सरसों'],
        'sunflower': ['sunflower', 'सूरजमुखी'],
        'sesame': ['sesame', 'तिल'],

        # Cash Crops
        'cotton': ['cotton', 'कपास'],
        'sugarcane': ['sugarcane', 'गन्ना'],
        'tobacco': ['tobacco', 'तंबाकू'],
        'jute': ['jute', 'जूट'],

        # Fruits
        'mango': ['mango', 'आम'],
        'banana': ['banana', 'केला'],
        'apple': ['apple', 'सेब'],
        'orange': ['orange', 'संतरा'],
        'grapes': ['grapes', 'अंगूर'],
        'pineapple': ['pineapple', 'अनानास'],
        'papaya': ['papaya', 'पपीता'],
        'guava': ['guava', 'अमरूद'],
        'pomegranate': ['pomegranate', 'अनार'],

        # Vegetables
        'potato': ['potato', 'आलू'],
        'tomato': ['tomato', 'टमाटर'],
        'onion': ['onion', 'प्याज'],
        'garlic': ['garlic', 'लहसुन'],
        'ginger': ['ginger', 'अदरक'],

        # Spices
        'chili': ['chili', 'मिर्च'],
        'turmeric': ['turmeric', 'हल्दी'],
        'coriander': ['coriander', 'धनिया'],
        'cumin': ['cumin', 'जीरा'],
        'fenugreek': ['fenugreek', 'मेथी']
    }

    for our_crop, api_names in crop_mapping.items():
        for api_name in api_names:
            if api_name in api_data:
                processed_data[our_crop] = {
                    'current_price': api_data[api_name].get('price', MOCK_MARKET_DATA.get(our_crop, {}).get('current_price', 0)),
                    'trend': api_data[api_name].get('trend', 'stable'),
                    'change_percent': api_data[api_name].get('change_percent', 0),
                    'best_selling_months': MOCK_MARKET_DATA.get(our_crop, {}).get('best_selling_months', []),
                    'demand': api_data[api_name].get('demand', 'medium')
                }
                break

    # Fill missing crops with mock data
    for crop in MOCK_MARKET_DATA:
        if crop not in processed_data:
            processed_data[crop] = MOCK_MARKET_DATA[crop]

    return processed_data

def get_market_data():
    """Get market data - real API first, fallback to mock"""
    if FALLBACK_TO_MOCK:
        return MOCK_MARKET_DATA

    real_data = fetch_real_market_data()
    if real_data:
        return real_data
    else:
        print("Falling back to mock market data")
        return MOCK_MARKET_DATA

@marketplace_bp.route('/status', methods=['GET'])
def get_api_status():
    """Check market API connection status"""
    try:
        real_data = fetch_real_market_data()
        if real_data:
            return jsonify({
                'status': 'connected',
                'message': 'Market API is working correctly',
                'using_real_data': True,
                'crops_available': list(real_data.keys()),
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'status': 'fallback',
                'message': 'Using mock data - API connection failed',
                'using_real_data': False,
                'crops_available': list(MOCK_MARKET_DATA.keys()),
                'timestamp': datetime.now().isoformat()
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'API check failed: {str(e)}',
            'using_real_data': False,
            'crops_available': list(MOCK_MARKET_DATA.keys()),
            'timestamp': datetime.now().isoformat()
        })

@marketplace_bp.route('/prices', methods=['GET'])
def get_crop_prices():
    """Get current market prices for all crops"""
    market_data = get_market_data()
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'prices': market_data,
        'currency': 'INR per quintal',
        'source': 'real_api' if not FALLBACK_TO_MOCK else 'mock_data'
    })

@marketplace_bp.route('/prices/<crop_name>', methods=['GET'])
def get_crop_price(crop_name):
    """Get detailed price information for a specific crop"""
    crop_name = crop_name.lower()
    market_data = get_market_data()

    if crop_name not in market_data:
        return jsonify({'error': f'Price data not available for {crop_name}'}), 404

    data = market_data[crop_name]

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
        'last_updated': datetime.now().isoformat(),
        'source': 'real_api' if not FALLBACK_TO_MOCK else 'mock_data'
    })

@marketplace_bp.route('/trends', methods=['GET'])
def get_market_trends():
    """Get overall market trends and insights"""
    market_data = get_market_data()

    # Calculate average changes
    total_change = sum(data['change_percent'] for data in market_data.values())
    avg_change = total_change / len(market_data)

    # Count trends
    trends = {'up': 0, 'down': 0, 'stable': 0}
    for data in market_data.values():
        trends[data['trend']] += 1

    # Get top performing crops
    top_performers = sorted(
        market_data.items(),
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
        'timestamp': datetime.now().isoformat(),
        'source': 'real_api' if not FALLBACK_TO_MOCK else 'mock_data'
    })

@marketplace_bp.route('/recommendations/<crop_name>', methods=['GET'])
def get_selling_recommendations(crop_name):
    """Get selling recommendations for a specific crop"""
    crop_name = crop_name.lower()
    market_data = get_market_data()

    if crop_name not in market_data:
        return jsonify({'error': f'No recommendations available for {crop_name}'}), 404

    data = market_data[crop_name]
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
        'timestamp': datetime.now().isoformat(),
        'source': 'real_api' if not FALLBACK_TO_MOCK else 'mock_data'
    })

@marketplace_bp.route('/alerts', methods=['GET'])
def get_market_alerts():
    """Get important market alerts and notifications"""
    market_data = get_market_data()
    alerts = []

    # Generate alerts based on trends
    for crop, data in market_data.items():
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
    for crop, data in market_data.items():
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
        'timestamp': datetime.now().isoformat(),
        'source': 'real_api' if not FALLBACK_TO_MOCK else 'mock_data'
    })