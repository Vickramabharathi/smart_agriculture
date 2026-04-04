# 🔨 BUILD GUIDE - What To Create Next

## Phase 1: Critical UI (This Week)

### 1. Login/Register Page
**File:** `templates/auth.html`  
**Time:** 4 hours  
**Difficulty:** Easy  

**What to create:**
```html
<!-- Login form -->
<form method="POST" action="/api/auth/login">
  <input type="email" name="email" placeholder="Email">
  <input type="password" name="password" placeholder="Password">
  <button type="submit">Login</button>
  <a href="#register">Register here</a>
</form>

<!-- Register form -->
<form method="POST" action="/api/auth/register">
  <input type="text" name="username" placeholder="Username">
  <input type="email" name="email" placeholder="Email">
  <input type="password" name="password" placeholder="Password">
  <input type="text" name="phone" placeholder="Phone">
  <select name="role">
    <option>Farmer</option>
    <option>Admin</option>
    <option>Expert</option>
  </select>
  <button type="submit">Register</button>
</form>
```

**API Endpoints Ready:**
- `POST /api/auth/register`
- `POST /api/auth/login`

**Notes:**
- Use Bootstrap form styling
- Store JWT token in localStorage
- Redirect to dashboard after login
- Add form validation (client-side)

---

### 2. Farm Management Page
**File:** `templates/farms.html`  
**Time:** 6 hours  
**Difficulty:** Medium  

**What to create:**

#### Farm List View
- Display all farms as Bootstrap cards
- Show: name, location, soil_type, area
- Buttons: Edit, Delete, View

#### Add Farm Form
- Form fields: name, location, latitude, longitude, soil_type, area
- Submit to `POST /api/farms`

#### Edit Farm Form
- Pre-populate with current farm data
- Submit to `PUT /api/farms/<id>`

**API Endpoints Ready:**
- `GET /api/farms`
- `POST /api/farms`
- `PUT /api/farms/<id>`
- `DELETE /api/farms/<id>`

**HTML Structure:**
```html
<!-- Farm List -->
<div class="row">
  {% for farm in farms %}
  <div class="col-md-4">
    <div class="card">
      <div class="card-body">
        <h5>{{ farm.name }}</h5>
        <p>{{ farm.location }}</p>
        <small>Soil: {{ farm.soil_type }} | Area: {{ farm.area }}ha</small>
        <button class="btn btn-sm btn-primary" onclick="editFarm({{ farm.id }})">Edit</button>
        <button class="btn btn-sm btn-danger" onclick="deleteFarm({{ farm.id }})">Delete</button>
      </div>
    </div>
  </div>
  {% endfor %}
</div>

<!-- Add Farm Form -->
<form method="POST" action="/api/farms">
  <input type="text" name="name" placeholder="Farm Name" required>
  <input type="text" name="location" placeholder="Location" required>
  <input type="number" name="latitude" placeholder="Latitude">
  <input type="number" name="longitude" placeholder="Longitude">
  <input type="text" name="soil_type" placeholder="Soil Type">
  <input type="number" name="area" placeholder="Area (hectares)">
  <button type="submit" class="btn btn-primary">Add Farm</button>
</form>
```

---

### 3. Enhanced Dashboard
**File:** `templates/dashboard.html` (modify existing)  
**Time:** 8 hours  
**Difficulty:** Medium  

**What to add:**

#### 1. Sensor Data Charts (Chart.js)
```html
<div class="row">
  <div class="col-md-6">
    <canvas id="moistureChart"></canvas>
  </div>
  <div class="col-md-6">
    <canvas id="temperatureChart"></canvas>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
<script>
  // Fetch sensor data from API
  fetch('/api/sensors/readings')
    .then(r => r.json())
    .then(data => {
      // Create moisture trend chart
      const ctx = document.getElementById('moistureChart').getContext('2d');
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: data.map(d => d.timestamp),
          datasets: [{
            label: 'Soil Moisture (%)',
            data: data.map(d => d.value),
            borderColor: '#2ecc71',
            fill: false
          }]
        }
      });
    });
</script>
```

#### 2. Crop Health Cards
```html
<div class="row">
  {% for crop in crops %}
  <div class="col-md-4">
    <div class="card">
      <div class="card-body">
        <h5>{{ crop.crop_name }}</h5>
        <div class="progress">
          <div class="progress-bar bg-success" 
               style="width: {{ crop.current_health_score }}%">
            {{ crop.current_health_score }}%
          </div>
        </div>
        <small>Health Score</small>
      </div>
    </div>
  </div>
  {% endfor %}
</div>
```

#### 3. Alert Bell Icon
```html
<div class="navbar-text">
  <button class="btn btn-link" onclick="toggleAlerts()">
    <i class="fas fa-bell"></i>
    <span id="alertCount" class="badge bg-danger">{{ unread_alerts }}</span>
  </button>
  <div id="alertDropdown" style="display:none;">
    {% for alert in recent_alerts %}
    <div class="alert alert-{{ alert.severity }}">
      {{ alert.message }}
    </div>
    {% endfor %}
  </div>
</div>

<script>
  function toggleAlerts() {
    const dropdown = document.getElementById('alertDropdown');
    dropdown.style.display = dropdown.style.display === 'none' ? 'block' : 'none';
  }
</script>
```

#### 4. Farm/Crop Selector
```html
<div class="mb-3">
  <label>Select Farm:</label>
  <select id="farmSelector" onchange="loadFarmDashboard()">
    <option value="">-- All Farms --</option>
    {% for farm in farms %}
    <option value="{{ farm.id }}">{{ farm.name }}</option>
    {% endfor %}
  </select>
</div>
```

**API Endpoints Ready:**
- `GET /api/sensors/readings`
- `GET /api/sensors/stats`
- `GET /api/crops`
- `GET /api/alerts`

---

## Phase 2: Advanced Features (Week 2)

### 4. Crop Management Page
**File:** `templates/crops.html`  
**Time:** 6 hours  
**Difficulty:** Medium  

Similar to farms.html but for crops:
- List crops per farm
- Add/edit/delete crop forms
- Show crop health score
- Display planting/harvest dates

**API Endpoints Ready:**
- `GET /api/crops`
- `POST /api/crops`
- `PUT /api/crops/<id>`
- `DELETE /api/crops/<id>`

---

### 5. Alerts/Notifications Center
**File:** `templates/alerts.html`  
**Time:** 5 hours  
**Difficulty:** Easy  

- Display all alerts in a table/list
- Filter by severity (info, warning, critical)
- Filter by read/unread
- Mark as read button
- Delete old alerts

**API Endpoints Ready:**
- `GET /api/alerts`
- `PUT /api/alerts/<id>/read`

---

### 6. Irrigation Control Widget
**Add to dashboard or separate page:**
- Display current moisture level
- Show ON/OFF button for motor
- Display water usage (liters)
- Show last irrigation time
- Allow threshold adjustment (40-80%)

**API Endpoints Ready:**
- `GET /api/irrigation/status`
- `POST /api/irrigation/control`
- `PUT /api/irrigation/settings`

---

### 7. Chatbot Widget
**File:** `templates/chat.html` or embed in all pages  
**Time:** 6 hours  
**Difficulty:** Medium  

```html
<div class="chat-widget">
  <div class="chat-header">Farm Assistant</div>
  <div class="chat-body" id="chatMessages"></div>
  <div class="chat-footer">
    <input type="text" id="chatInput" placeholder="Ask a question...">
    <button onclick="sendMessage()">Send</button>
  </div>
</div>

<script>
  function sendMessage() {
    const message = document.getElementById('chatInput').value;
    fetch('/api/chatbot/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message: message})
    })
    .then(r => r.json())
    .then(data => {
      // Display user message
      // Display bot response
      // Add to chat history
    });
  }
</script>
```

---

### 8. Market Intelligence Page
**File:** `templates/market.html`  
**Time:** 6 hours  
**Difficulty:** Medium  

- Display crop prices
- Show price trends (chart)
- Display best selling indicators
- Compare prices across locations
- Historical price data

**API Endpoints Need Creation:**
- `GET /api/market/prices`
- `GET /api/market/trends`

---

### 9. Farm Map Visualization
**File:** `templates/map.html`  
**Time:** 8 hours  
**Difficulty:** Hard  

```html
<div id="map" style="height: 600px;"></div>

<script src="https://leafletjs.com/dist/leaflet.js"></script>
<link rel="stylesheet" href="https://leafletjs.com/dist/leaflet.css" />

<script>
  // Load farms and display on map
  fetch('/api/farms')
    .then(r => r.json())
    .then(farms => {
      const map = L.map('map').setView([20, 78], 5);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
      
      farms.forEach(farm => {
        L.marker([farm.latitude, farm.longitude])
          .bindPopup(`<b>${farm.name}</b><br>${farm.location}`)
          .addTo(map);
      });
    });
</script>
```

---

## Phase 3: Reports & Advanced Analytics (Week 3)

### 10. Reports Builder
**File:** `templates/reports.html`  
**Time:** 10 hours  
**Difficulty:** Hard  

- Select report type (sensor, crop, yield, water usage)
- Select date range
- Choose export format (PDF, Excel, CSV)
- Display preview
- Download button

**API Endpoints Need Creation:**
- `POST /api/reports/generate`
- `POST /api/reports/export`

---

### 11. Predictive Analytics Dashboard
**File:** `templates/analytics.html`  
**Time:** 6 hours  
**Difficulty:** Medium  

- Display yield prediction chart
- Show pest outbreak risk
- Display soil condition forecast
- Risk level indicators

**API Endpoints Already Have:**
- `POST /api/analytics/yield-prediction`

---

## Quick Reference: All Missing Pages

| Page | File | API Ready | Time | Priority |
|------|------|-----------|------|----------|
| Login/Register | `auth.html` | ✅ | 4h | 🔴 CRITICAL |
| Farm Management | `farms.html` | ✅ | 6h | 🔴 CRITICAL |
| Dashboard Enhancement | `dashboard.html` | ✅ | 8h | 🔴 CRITICAL |
| Crop Management | `crops.html` | ✅ | 6h | 🟠 HIGH |
| Alerts Center | `alerts.html` | ✅ | 5h | 🟠 HIGH |
| Irrigation Control | (dashboard widget) | ✅ | 4h | 🟠 HIGH |
| Chatbot | `chat.html` | ✅ | 6h | 🟡 MEDIUM |
| Market Prices | `market.html` | 🔄 | 6h | 🟡 MEDIUM |
| Farm Map | `map.html` | 🔄 | 8h | 🟡 MEDIUM |
| Reports | `reports.html` | ❌ | 10h | 🟡 MEDIUM |
| Yield Analytics | `analytics.html` | ✅ | 6h | 🟡 MEDIUM |

---

## Development Checklist

### Before starting any page:
- [ ] Check if API endpoints exist
- [ ] Review database models
- [ ] Plan Bootstrap layout
- [ ] Create form fields
- [ ] Add JavaScript for AJAX calls
- [ ] Test API with Postman first

### While building:
- [ ] Use Bootstrap 5 classes
- [ ] Make it mobile-responsive
- [ ] Add error handling
- [ ] Show loading states
- [ ] Validate form inputs
- [ ] Test with real API data

### After completing:
- [ ] Test all CRUD operations
- [ ] Check mobile layout
- [ ] Test error scenarios
- [ ] Add success/error messages
- [ ] Update navigation links
- [ ] Document any new routes

---

**Total Time Estimate:**
- Phase 1 (Critical): 18 hours
- Phase 2 (Advanced): 45 hours
- Phase 3 (Polish): 26 hours
- **Total: ~90 hours** (2-3 weeks at 40h/week)

**Start with Phase 1** - After that, you'll have a fully functional app!
