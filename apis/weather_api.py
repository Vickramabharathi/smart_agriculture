from flask import Blueprint, request, jsonify
import requests
from datetime import datetime

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/current/<city>', methods=['GET'])
def get_current_weather(city):
    """Get current weather for a city"""
    api_key = "1dc8367105e7083aeef7dd2f25a3ae32"  # Should be from config
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return jsonify({
                'city': data['name'],
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed'],
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'error': 'City not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@weather_bp.route('/forecast/<city>', methods=['GET'])
def get_weather_forecast(city):
    """Get 5-day weather forecast"""
    api_key = "1dc8367105e7083aeef7dd2f25a3ae32"
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            forecast = []
            for item in data['list'][:8]:  # Next 24 hours (3-hour intervals)
                forecast.append({
                    'datetime': item['dt_txt'],
                    'temperature': item['main']['temp'],
                    'humidity': item['main']['humidity'],
                    'description': item['weather'][0]['description'],
                    'wind_speed': item['wind']['speed']
                })
            return jsonify({
                'city': data['city']['name'],
                'forecast': forecast
            })
        else:
            return jsonify({'error': 'City not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500