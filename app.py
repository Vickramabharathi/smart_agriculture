import os
import json
from flask import Flask, render_template, request, jsonify
from werkzeug.exceptions import HTTPException
from config.config import config
from models.database import db
from flask_cors import CORS
import requests
from datetime import datetime
import random

# Import blueprints
from apis.auth_api import auth_bp
from apis.farm_api import farm_bp
from apis.crop_api import crop_bp
from apis.sensor_api import sensor_bp
from apis.disease_api import disease_bp
from apis.recommendation_api import recommendation_bp
from apis.irrigation_api import irrigation_bp
from apis.chatbot_api import chatbot_bp
from apis.analytics_api import analytics_bp
from apis.weather_api import weather_bp
from apis.marketplace_api import marketplace_bp

# Initialize Flask app
def create_app(config_name=None):
    """Create Flask application with proper config detection"""
    # Auto-detect environment if not provided
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
        # If DATABASE_URL is set, use production config
        if os.environ.get('DATABASE_URL'):
            config_name = 'production'
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize CORS
    CORS(app)
    
    # Initialize database (dummy in-memory implementation)
    db.init_app(app)
    
    app.logger.info(f"Using config: {config_name}")
    app.logger.info("Running in database-free mode - all data is in-memory only")
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(farm_bp, url_prefix='/api/farms')
    app.register_blueprint(crop_bp, url_prefix='/api/crops')
    app.register_blueprint(sensor_bp, url_prefix='/api/sensors')
    app.register_blueprint(disease_bp, url_prefix='/api/disease')
    app.register_blueprint(recommendation_bp, url_prefix='/api/recommendations')
    app.register_blueprint(irrigation_bp, url_prefix='/api/irrigation')
    app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    app.register_blueprint(weather_bp, url_prefix='/api/weather')
    app.register_blueprint(marketplace_bp, url_prefix='/api/marketplace')

    @app.errorhandler(Exception)
    def handle_api_exceptions(error):
        if isinstance(error, HTTPException):
            status = error.code or 500
            message = error.description
        else:
            status = 500
            message = str(error)

        app.logger.exception('Unhandled exception')
        app.logger.error(f'Error details: {message}')
        app.logger.error(f'Request path: {request.path}')
        app.logger.error(f'Request method: {request.method}')

        if request.path.startswith('/api/'):
            return jsonify({'message': 'Server error', 'details': message}), status
        return render_template('index.html'), status
    
    # Original routes
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/auth')
    def auth():
        return render_template('auth.html')

    @app.route('/farms')
    def farms_page():
        return render_template('farms.html')

    @app.route('/dashboard')
    def dashboard():
        data = {
            "moisture": random.randint(20, 80),
            "temperature": random.randint(25, 40),
            "humidity": random.randint(40, 90)
        }
        advice = irrigation_advice(data['moisture'], data['temperature'])
        return render_template('dashboard.html', data=data, advice=advice)

    @app.route('/crops')
    def crops_page():
        return render_template('crops.html')

    @app.route('/alerts')
    def alerts_page():
        return render_template('alerts.html')

    @app.route('/upload', methods=['GET','POST'])
    def upload():
        if request.method == 'POST':
            file = request.files['image']
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)
            return jsonify({'status': 'success', 'image': file.filename, 'prediction': 'Demo Result'})
        return render_template('upload.html')

    @app.route('/weather', methods=['GET','POST'])
    def weather():
        if request.method == 'POST':
            city = request.form['city']
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={app.config['OPENWEATHER_API_KEY']}&units=metric"
            
            try:
                data = requests.get(url).json()
                if data.get("cod") != 200:
                    return f"Error: {data.get('message')}"
                return render_template('weather.html', weather=data)
            except:
                return f"Error: Could not fetch weather data"
        return render_template('weather.html', weather=None)

    @app.route('/chatbot')
    def chatbot():
        return render_template('chatbot.html')

    @app.route('/map')
    def map_page():
        return render_template('map.html')

    @app.route('/market')
    def market_page():
        return render_template('market.html')

    @app.route('/reports')
    def reports_page():
        return render_template('reports.html')

    @app.route('/analytics')
    def analytics_page():
        return render_template('analytics.html')

    def irrigation_advice(m, t):
        if m < 30:
            return "Water crops"
        elif t > 35:
            return "Increase watering"
        return "All good"
        if m < 30:
            return "Water crops"
        elif t > 35:
            return "Increase watering"
        return "All good"
    
    return app

# Only create app here if running directly (development)
if __name__ == "__main__":
    app = create_app(os.environ.get('FLASK_ENV', 'development'))
    app.run(debug=True, host='0.0.0.0', port=5000)