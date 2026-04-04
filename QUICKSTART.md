# 🚜 Smart Agriculture - Quick Start Guide

## What's Been Built (✅ Complete)

Your Smart Agriculture application now includes:

### Core Systems
1. **AI & Deep Learning Engine** - 6 intelligent models
2. **Database System** - 13 comprehensive models
3. **REST APIs** - 8 blueprint modules with 20+ endpoints
4. **Authentication** - JWT-based security with roles
5. **Chatbot** - NLP farmer assistant
6. **Automation** - Smart irrigation control

### Key Capabilities
- 🤖 Disease detection from crop images
- 🌾 Smart crop recommendations
- 🧪 NPK-based fertilizer suggestions
- 📈 Yield prediction using ML
- 💧 Automatic irrigation scheduling
- 🐛 Pest attack risk prediction
- 💬 AI chatbot for farmer queries
- 💰 Market price tracking & sell recommendations
- 📊 Real-time sensor data processing
- 🎯 Role-based access control

---

## 📁 Project Structure

```
smart_agriculture/
├── app.py                          # Main Flask app
├── requirements.txt                # All dependencies
├── IMPLEMENTATION_GUIDE.md         # Full documentation
├── QUICKSTART.md                  # This file
│
├── config/
│   └── config.py                  # Configuration management
│
├── models/
│   └── database.py                # Database models (13 models)
│
├── ai_models/
│   └── ai_engine.py               # AI algorithms
│
├── apis/
│   ├── auth_api.py                # Authentication
│   ├── farm_api.py                # Farm management
│   ├── crop_api.py                # Crop management
│   ├── sensor_api.py              # Sensor data
│   ├── disease_api.py             # Disease detection
│   ├── recommendation_api.py       # Recommendations
│   ├── irrigation_api.py           # Smart irrigation
│   ├── chatbot_api.py             # AI chatbot
│   └── analytics_api.py           # Analytics & insights
│
├── utils/
│   └── helpers.py                 # Helper functions
│
├── static/
│   ├── style.css                  # Styling
│   └── uploads/                   # User uploads
│
└── templates/
    ├── index.html
    ├── dashboard.html
    ├── weather.html
    ├── upload.html
    └── result.html
```

---

## 🚀 Getting Started (3 Steps)

### Step 1: Install Dependencies
```bash
# Navigate to your project folder
cd c:\Users\HP\OneDrive\Desktop\smart_agriculture

# Install all packages
pip install -r requirements.txt
```

**What installs:**
- Flask & web framework
- TensorFlow & deep learning
- scikit-learn & ML models
- SQLAlchemy & database
- Twilio for SMS alerts
- And 15+ more libraries

### Step 2: Start the Application
```bash
python app.py
```

**Output:**
```
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:5000
```

### Step 3: Test the APIs

Open a new terminal and try:

```bash
# 1. Register a farmer account
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "farmer1",
    "email": "farmer@example.com",
    "password": "secure_password",
    "phone": "9876543210",
    "role": "farmer"
  }'

# Response:
# {
#   "message": "User registered successfully",
#   "user_id": 1,
#   "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
# }
```

---

## 🎮 Live API Testing Examples

### 1. Create a Farm
```bash
curl -X POST http://localhost:5000/api/farms \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "name": "Green Valley Farm",
    "location": "Bangalore",
    "latitude": 12.9716,
    "longitude": 77.5946,
    "area": 15.5,
    "soil_type": "loam"
  }'
```

### 2. Simulate Sensor Data
```bash
curl -X POST http://localhost:5000/api/sensors/1/simulate
```

**Response:**
```json
{
  "message": "Sensor data simulated",
  "farm_id": 1,
  "readings": [
    {"sensor_type": "moisture", "value": 52.3, "unit": "%", "timestamp": "..."},
    {"sensor_type": "temperature", "value": 28.5, "unit": "°C", "timestamp": "..."},
    {"sensor_type": "humidity", "value": 65.2, "unit": "%", "timestamp": "..."}
  ]
}
```

### 3. Add a Crop
```bash
curl -X POST http://localhost:5000/api/crops/1 \
  -H "Content-Type: application/json" \
  -d '{
    "crop_name": "rice",
    "variety": "Basmati",
    "area": 5
  }'
```

### 4. Get Fertilizer Recommendation
```bash
curl -X POST http://localhost:5000/api/recommendations/1/fertilizer \
  -H "Content-Type: application/json" \
  -d '{
    "soil_nitrogen": 20,
    "soil_phosphorus": 15,
    "soil_potassium": 150,
    "growth_stage": "vegetative"
  }'
```

**Response:**
```json
{
  "recommendation_id": 1,
  "npk": "40.00:13.00:8.00",
  "fertilizer": "Urea (46% N)",
  "application_frequency": "bi-weekly"
}
```

### 5. Query the Chatbot
```bash
curl -X POST http://localhost:5000/api/chatbot/query \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "message": "My rice leaves are turning yellow, what should I do?"
  }'
```

### 6. Get Irrigation Schedule
```bash
curl -X GET http://localhost:5000/api/irrigation/1/status
```

**Response:**
```json
{
  "farm_id": 1,
  "current_moisture": 45.2,
  "threshold": 40,
  "needs_irrigation": false,
  "motor_status": "OFF",
  "automated_mode": true
}
```

### 7. Pest Risk Assessment
```bash
curl -X GET http://localhost:5000/api/analytics/1/pest-risk
```

---

## 🎯 Common Workflows

### Workflow 1: Disease Detection
1. Upload crop image via `/api/disease/<crop_id>/detect`
2. AI analyzes and returns disease name + confidence
3. Recommendations auto-generated
4. Alert sent if severity is high

### Workflow 2: Smart Irrigation
1. Farmer sets moisture threshold: `40%`
2. System monitors soil moisture in real-time
3. When moisture < 40%, motor auto-activates
4. Farmer gets notification
5. Motor stops when adequate moisture restored

### Workflow 3: Crop Recommendation
1. Farmer inputs soil type, temperature, rainfall
2. AI recommends best crops for conditions
3. System shows compatibility score
4. Farmer selects preferred crop
5. Gets full management plan (fertilizer, water, pest control)

### Workflow 4: Chat with AI Assistant
1. Farmer asks: "Yellow leaves on my cotton crop"
2. Chatbot detects intent: "disease_diagnosis"
3. System provides:
   - Likely causes (nitrogen deficiency, disease)
   - Treatment options
   - Prevention measures
   - Recommendation to upload image for AI analysis

---

## 📊 Database Models Included

| Model | Purpose |
|-------|---------|
| User | Farmer/Admin/Expert profiles |
| Farm | Farm details with location |
| Crop | Crop tracking per farm |
| SensorReading | IoT sensor data (moisture, temp, humidity, pH, water level) |
| DiseaseDetection | Disease detection history |
| Recommendation | Auto-generated recommendations |
| Alert | Multi-channel notifications |
| IrrigationControl | Smart irrigation settings |
| MarketData | Crop price tracking |
| YieldPrediction | ML yield forecasts |
| ChatHistory | Farmer queries & AI responses |

---

## 🧠 AI Models Included

1. **Disease Detection Model**
   - Identifies: leaf_spot, blight, rust, powdery_mildew
   - Returns: disease name, confidence score, severity

2. **Crop Recommendation Engine**
   - Inputs: soil type, temperature, rainfall
   - Outputs: ranked crop suggestions with scores

3. **Fertilizer Recommendation Engine**
   - Inputs: soil NPK levels, crop, growth stage
   - Outputs: NPK ratio, specific fertilizer, frequency

4. **Yield Prediction Model**
   - Inputs: moisture, temperature, humidity, rainfall, days since planting
   - Outputs: predicted yield (tons), confidence score

5. **Irrigation Optimizer**
   - Inputs: soil moisture, rainfall forecast, crop
   - Outputs: irrigation schedule, amount, frequency, urgency

6. **Pest Prediction Model**
   - Inputs: temperature, humidity, rainfall
   - Outputs: pest risk level, likely pests, preventive measures

---

## 🔧 Configuration

Edit `config/config.py` to customize:

```python
# Weather API
OPENWEATHER_API_KEY = "your_api_key_here"

# SMS Alerts (Twilio)
TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_PHONE = "+1234567890"

# MQTT (IoT Sensors)
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPICS = ['sensors/moisture', 'sensors/temperature', ...]

# Database
SQLALCHEMY_DATABASE_URI = 'sqlite:///smart_agriculture.db'
```

---

## 🐛 Troubleshooting

### Issue: Import errors for libraries
**Solution:** Run `pip install -r requirements.txt` again

### Issue: Database not creating tables
**Solution:** 
```python
from app import app, db
with app.app_context():
    db.create_all()
```

### Issue: API returns 404
**Solution:** Check URL path and method (GET/POST/PUT/DELETE)

### Issue: CORS errors in frontend
**Solution:** Already configured in app - ensure frontend sends proper headers

---

## 📚 API Documentation

Full API documentation available in `IMPLEMENTATION_GUIDE.md`

Quick reference:
```
/api/auth/          - User authentication
/api/farms/         - Farm management
/api/crops/         - Crop tracking
/api/sensors/       - Sensor data
/api/disease/       - Disease detection
/api/recommendations/ - AI recommendations
/api/irrigation/    - Smart irrigation
/api/chatbot/       - AI assistant
/api/analytics/     - Data analytics & insights
```

---

## 🎨 Next: Build Frontend Dashboard

After APIs are tested, create a dashboard using:
- **Chart.js** - Real-time charts
- **Leaflet** - Farm mapping
- **Bootstrap/Tailwind** - UI components

Example dashboard features:
- Real-time sensor graphs
- Crop health status
- Alert notifications
- Irrigation automation toggle
- Market prices
- Yield predictions

---

## 📱 Mobile App Ready

All APIs are mobile-friendly. Build iOS/Android app with:
- React Native
- Flutter
- Native iOS/Android SDK

---

## 🚀 Production Deployment

When ready for production:

1. **Database**: Switch from SQLite to PostgreSQL
2. **Server**: Use Gunicorn instead of Flask dev server
3. **Security**: Generate new JWT_SECRET_KEY
4. **HTTPS**: Set up SSL certificates
5. **Monitoring**: Add error logging & analytics
6. **Backup**: Implement automated backups

```bash
# Production run
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 📞 Support Features Included

✅ Role-based access (Farmer, Admin, Expert)
✅ User authentication & token management
✅ Password hashing with bcrypt
✅ Error handling with status codes
✅ Database transactions & data integrity
✅ Logging & debugging support

---

## 🎯 Success Metrics

Track these to measure impact:
- 📊 Crop yield increase (%)
- 💰 Cost reduction (fertilizer, water)
- 🐛 Disease detection accuracy
- ⏱️ Time saved on manual monitoring
- 💧 Water savings (%)

---

## 📖 Learn More

- TensorFlow: https://tensorflow.org
- scikit-learn: https://scikit-learn.org
- Flask: https://flask.palletsprojects.com
- MQTT: https://mqtt.org
- OpenWeatherMap: https://openweathermap.org

---

**Version:** 1.0  
**Last Updated:** April 2, 2026  
**Status:** Ready for Development & Deployment

Happy Farming! 🌾👨‍🌾
