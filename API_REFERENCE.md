# 📚 Smart Agriculture API Reference Card

## Base URL
`http://localhost:5000/api`

## Authentication Header
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

---

## 🔐 AUTHENTICATION ENDPOINTS

### Register User
```
POST /auth/register
Body: {
  "username": "farmer1",
  "email": "farmer@email.com",
  "password": "pass123",
  "phone": "9876543210",
  "role": "farmer"  // farmer, admin, expert
}
Response: { "user_id": 1, "token": "jwt_token", ... }
```

### Login
```
POST /auth/login
Body: {
  "username": "farmer1",
  "password": "pass123"
}
Response: { "user_id": 1, "token": "jwt_token", "role": "farmer" }
```

### Get Profile
```
GET /auth/profile
Headers: Authorization: Bearer <token>
Response: { user profile data }
```

---

## 🌾 FARM MANAGEMENT ENDPOINTS

### Get All Farms
```
GET /farms/
Response: [
  {
    "id": 1,
    "name": "Green Farm",
    "location": "Bangalore",
    "area": 15.5
  },
  ...
]
```

### Create Farm
```
POST /farms/
Body: {
  "user_id": 1,
  "name": "Green Farm",
  "location": "Bangalore",
  "latitude": 12.9716,
  "longitude": 77.5946,
  "area": 15.5,
  "soil_type": "loam"
}
Response: { "message": "Farm created", "farm_id": 1 }
```

### Farm Dashboard
```
GET /farms/<farm_id>/dashboard
Response: {
  "farm_id": 1,
  "farm_name": "Green Farm",
  "location": "Bangalore",
  "soil_type": "loam",
  "recent_sensors": [
    { "type": "moisture", "value": 52.3, "unit": "%" },
    ...
  ]
}
```

---

## 🌱 CROP MANAGEMENT ENDPOINTS

### Get Crops
```
GET /crops/<farm_id>
Response: [
  { "id": 1, "name": "rice", "variety": "Basmati", "health_score": 92.5 },
  ...
]
```

### Create Crop
```
POST /crops/<farm_id>
Body: {
  "crop_name": "rice",
  "variety": "Basmati",
  "area": 5
}
Response: { "message": "Crop created", "crop_id": 1 }
```

### Crop Health Status
```
GET /crops/<crop_id>/health
Response: {
  "crop_id": 1,
  "crop_name": "rice",
  "health_score": 92.5,
  "active_issues": [
    { "disease": "leaf_spot", "confidence": 0.87, "severity": "mild" }
  ]
}
```

---

## 📡 SENSOR DATA ENDPOINTS

### Get Sensor Readings
```
GET /sensors/<farm_id>/read?hours=24
Response: {
  "farm_id": 1,
  "readings": [
    {
      "id": 1,
      "sensor_type": "moisture",
      "value": 52.3,
      "unit": "%",
      "location": "Field A",
      "timestamp": "2026-04-02T14:30:00"
    },
    ...
  ]
}
```

### Simulate Sensors (Testing)
```
POST /sensors/<farm_id>/simulate
Response: {
  "message": "Sensor data simulated",
  "readings": [
    { "sensor_type": "moisture", "value": 45.2, ... },
    { "sensor_type": "temperature", "value": 28.5, ... },
    ...
  ]
}
```

**Available Sensors:**
- `moisture` (%)
- `temperature` (°C)
- `humidity` (%)
- `ph` (pH level)
- `water_level` (mm)

---

## 🦠 DISEASE DETECTION ENDPOINTS

### Detect Disease
```
POST /disease/<crop_id>/detect
Form-data: image=@leaf_photo.jpg
Response: {
  "detection_id": 1,
  "disease": "leaf_spot",
  "confidence": 0.87,
  "severity": "mild",
  "pest_detected": false,
  "crop_health_updated": 85.2
}
```

### Disease History
```
GET /disease/<crop_id>/history
Response: [
  {
    "id": 1,
    "disease": "leaf_spot",
    "confidence": 0.87,
    "severity": "mild",
    "detected_at": "2026-04-02T10:00:00",
    "status": "active"
  },
  ...
]
```

**Detected Diseases:**
- healthy
- leaf_spot
- blight
- rust
- powdery_mildew
- unknown

---

## 💡 RECOMMENDATION ENDPOINTS

### Fertilizer Recommendation
```
POST /recommendations/<crop_id>/fertilizer
Body: {
  "soil_nitrogen": 20,
  "soil_phosphorus": 15,
  "soil_potassium": 150,
  "growth_stage": "vegetative"
}
Response: {
  "recommendation_id": 1,
  "npk": "40.00:13.00:8.00",
  "fertilizer": "Urea (46% N)",
  "application_frequency": "bi-weekly"
}
```

**Growth Stages:**
- seedling
- vegetative
- flowering
- fruiting

### Get Crop Recommendations
```
GET /recommendations/<crop_id>/crop-change
Response: {
  "crop_id": 1,
  "current_crop": "rice",
  "recommendations": [
    { "crop": "wheat", "score": 0.85, "rationale": "..." },
    { "crop": "maize", "score": 0.72, "rationale": "..." }
  ]
}
```

### All Recommendations
```
GET /recommendations/<crop_id>/all
Response: [
  {
    "id": 1,
    "type": "fertilizer",
    "reason": "Nitrogen deficiency detected",
    "priority": "high",
    "created_at": "2026-04-02T12:00:00"
  },
  ...
]
```

---

## 💧 IRRIGATION CONTROL ENDPOINTS

### Get Irrigation Config
```
GET /irrigation/<farm_id>/config
Response: {
  "farm_id": 1,
  "is_automated": true,
  "moisture_threshold": 40.0,
  "max_water_per_day": 5000,
  "is_motor_on": false
}
```

### Set Irrigation Config
```
POST /irrigation/<farm_id>/config
Body: {
  "is_automated": true,
  "moisture_threshold": 40.0,
  "max_water_per_day": 5000
}
Response: { "message": "Configuration updated" }
```

### Irrigation Status
```
GET /irrigation/<farm_id>/status
Response: {
  "farm_id": 1,
  "current_moisture": 45.2,
  "threshold": 40.0,
  "needs_irrigation": false,
  "motor_status": "OFF",
  "last_irrigation": "2026-04-02T08:00:00",
  "automated_mode": true
}
```

### Motor Control
```
POST /irrigation/<farm_id>/control
Body: { "action": "ON" }  // or "OFF"
Response: { "message": "Motor turned ON", "motor_status": "ON" }
```

### Irrigation Schedule
```
GET /irrigation/<farm_id>/schedule
Response: {
  "farm_id": 1,
  "crop": "rice",
  "schedule": {
    "irrigate_now": true,
    "water_amount": 2500,
    "frequency": "Every 2 days",
    "urgency": "HIGH"
  }
}
```

---

## 🤖 CHATBOT ENDPOINTS

### Send Query
```
POST /chatbot/query
Body: {
  "user_id": 1,
  "message": "My rice leaves are turning yellow, what should I do?"
}
Response: {
  "chat_id": 5,
  "user_message": "My rice leaves are turning yellow...",
  "bot_response": "Yellow leaves often indicate nitrogen deficiency...",
  "intent": "disease_diagnosis",
  "confidence": 0.85
}
```

### Chat History
```
GET /chatbot/history/<user_id>
Response: [
  {
    "id": 5,
    "user_message": "My rice leaves are turning yellow...",
    "bot_response": "Yellow leaves often indicate...",
    "intent": "disease_diagnosis",
    "timestamp": "2026-04-02T14:00:00"
  },
  ...
]
```

**Intent Types:**
- disease_diagnosis
- fertilizer_recommendation
- irrigation_advice
- pest_management
- general_agriculture

---

## 📊 ANALYTICS ENDPOINTS

### Farm Overview
```
GET /analytics/<farm_id>/overview
Response: {
  "farm_id": 1,
  "farm_name": "Green Farm",
  "total_crops": 3,
  "avg_health_score": 87.5,
  "sensor_statistics": {
    "moisture": { "avg": 52.3, "min": 40.1, "max": 75.2, "latest": 52.3 },
    "temperature": { "avg": 28.5, "min": 18.2, "max": 35.8, "latest": 28.5 },
    ...
  },
  "area_hectares": 15.5
}
```

### Yield Prediction
```
GET /analytics/<crop_id>/yield-prediction
Response: {
  "crop_id": 1,
  "crop_name": "rice",
  "predicted_yield_tons": 5.8,
  "confidence": 0.75,
  "factors": ["moisture", "temperature", "humidity", "rainfall"],
  "prediction_id": 1
}
```

### Market Information
```
GET /analytics/<crop_id>/market-info
Response: {
  "crop": "rice",
  "current_price": "₹45/kg",
  "price_range_30days": "₹40 - ₹50",
  "trend": "up",
  "recommendation": "Sell",
  "volume_available": 1000,
  "quality_grade": "A",
  "last_updated": "2026-04-02T10:00:00"
}
```

### Alerts Summary
```
GET /analytics/<farm_id>/alerts-summary
Response: {
  "farm_id": 1,
  "total_alerts": 5,
  "recent_alerts": [
    {
      "id": 1,
      "type": "disease",
      "title": "Leaf spot detected on rice",
      "severity": "warning",
      "is_predictive": false,
      "is_read": false,
      "created_at": "2026-04-02T10:00:00"
    },
    ...
  ]
}
```

### Pest Risk Assessment
```
GET /analytics/<farm_id>/pest-risk
Response: {
  "farm_id": 1,
  "crop": "rice",
  "risk_level": "medium",
  "risk_score": 45,
  "predicted_pests": ["stem_borer", "leaf_folder", "brown_plant_hopper"],
  "preventive_measures": [
    "Scout fields regularly",
    "Keep pesticides ready",
    "Monitor weather"
  ],
  "current_temp": 28.5,
  "current_humidity": 65.2
}
```

---

## 🔍 HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Missing/invalid token |
| 404 | Not Found - Resource doesn't exist |
| 500 | Server Error |

---

## 🔄 Response Format

**Success:**
```json
{
  "message": "Operation successful",
  "data": { ... }
}
```

**Error:**
```json
{
  "message": "Error description"
}
```

---

## 💾 Data Types

| Type | Format | Example |
|------|--------|---------|
| String | Text | "rice" |
| Number | Integer/Float | 45.2, 100 |
| Boolean | true/false | true |
| DateTime | ISO 8601 | "2026-04-02T14:30:00" |
| Enum | Predefined values | "mild", "warning" |

---

## 🧪 Quick Test Script

Save as `test_api.sh`:
```bash
#!/bin/bash

BASE_URL="http://localhost:5000/api"

# Register
TOKEN=$(curl -s -X POST $BASE_URL/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","password":"123"}' \
  | grep -o '"token":"[^"]*' | cut -d'"' -f4)

# Create farm
curl -X POST $BASE_URL/farms \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"name":"Test","location":"City","area":10,"soil_type":"loam"}'

# Simulate sensors
curl -X POST $BASE_URL/sensors/1/simulate

echo "API Test Complete!"
```

---

**Last Updated:** April 2, 2026  
**Version:** 1.0  
**Reference:** Complete API endpoint documentation
