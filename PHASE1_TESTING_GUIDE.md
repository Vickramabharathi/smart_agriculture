# 🧪 PHASE 1 TESTING GUIDE

**Quick test checklist to verify all Phase 1 features are working**

---

## ✅ Quick Start (5 minutes)

```bash
# 1. Open terminal in project folder
cd c:\Users\HP\OneDrive\Desktop\smart_agriculture

# 2. Activate virtual environment
.venv\Scripts\activate

# 3. Start Flask app
python app.py

# 4. Open browser
# http://127.0.0.1:5000
```

You should see the **Smart Agriculture** homepage with a login button.

---

## 🔑 Testing Account

**Email:** test@example.com  
**Password:** password123  

Or create a new account by clicking "Register" on the auth page.

---

## ✨ Feature Testing Checklist

### 1️⃣ Dashboard (http://127.0.0.1:5000/dashboard)

- [ ] Page loads without errors
- [ ] Navbar shows "Dashboard" as active
- [ ] User name displays in top right
- [ ] 4 sensor stat cards visible:
  - [ ] Soil Moisture (%)
  - [ ] Temperature (°C)
  - [ ] Humidity (%)
  - [ ] pH Level
- [ ] 4 Chart.js graphs visible:
  - [ ] Soil Moisture Trend
  - [ ] Temperature Trend
  - [ ] Humidity Trend
  - [ ] pH Level Trend
- [ ] Crop Health section displays crops
- [ ] Quick Actions grid shows 4 buttons:
  - [ ] Add Crop
  - [ ] Add Farm
  - [ ] Check Weather
  - [ ] View Alerts
- [ ] Farm selector dropdown works
- [ ] Crop selector dropdown works
- [ ] Alert bell icon shows count (top right)

**Expected Result:** Dashboard fully loaded with charts and crop health cards

---

### 2️⃣ Farms (http://127.0.0.1:5000/farms)

- [ ] Page loads without errors
- [ ] Navbar shows "Farms" as active
- [ ] Add Farm button appears
- [ ] Existing farms displayed as cards
- [ ] Search box filters farms
- [ ] Click "Add Farm" button:
  - [ ] Modal opens
  - [ ] Form has fields: Farm Name, Location, Area, Notes
  - [ ] Submit button works
  - [ ] Farm added to list after submit

**Test Adding a Farm:**
```
Farm Name: Test Farm 1
Location: Delhi
Area: 50
Notes: Testing Phase 1
```

- [ ] Edit farm works (click Edit button)
- [ ] Delete farm works (with confirmation)
- [ ] Responsive design on mobile (resize browser)

**Expected Result:** Full CRUD operations working on farms

---

### 3️⃣ Crops (http://127.0.0.1:5000/crops) ✨ NEW

- [ ] Page loads without errors
- [ ] Navbar shows "Crops" as active
- [ ] Add Crop button appears
- [ ] Search box is functional
- [ ] Farm filter dropdown works
- [ ] Stage filter dropdown works (all options visible)
- [ ] Click "Add Crop" button:
  - [ ] Modal opens with title "Add Crop"
  - [ ] Farm selector populated
  - [ ] Form fields visible:
    - [ ] Farm (required)
    - [ ] Crop Name (required)
    - [ ] Variety
    - [ ] Planting Date (required)
    - [ ] Expected Harvest Date (required)
    - [ ] Area (m²)
    - [ ] Growth Stage (dropdown)
    - [ ] Notes
  - [ ] Submit button works

**Test Adding a Crop:**
```
Farm: Test Farm 1
Crop Name: Wheat
Variety: HD-2967
Planting Date: 2024-01-15
Harvest Date: 2024-05-15
Area: 20
Stage: Growing
Notes: High yield variety
```

- [ ] Crop appears in list after submit
- [ ] Crop card shows:
  - [ ] Crop name with farm icon
  - [ ] Health score as percentage
  - [ ] Progress bar visualization
  - [ ] All details (variety, stage, dates, area)
  - [ ] 3 action buttons (View, Edit, Delete)
- [ ] Edit crop works
- [ ] Delete crop works with confirmation
- [ ] Search filters crops by name
- [ ] Farm filter shows only selected farm crops
- [ ] Stage filter shows only selected stage crops

**Expected Result:** Full crop CRUD with filtering and search working

---

### 4️⃣ Alerts (http://127.0.0.1:5000/alerts) ✨ NEW

- [ ] Page loads without errors
- [ ] Navbar shows "Alerts" as active
- [ ] Page header shows title "Alerts Center"
- [ ] Two action buttons visible:
  - [ ] Mark All as Read
  - [ ] Clear All
- [ ] 4 Statistics cards visible:
  - [ ] Critical Alerts (number)
  - [ ] Warnings (number)
  - [ ] Total Alerts (number)
  - [ ] Unread (number)
- [ ] Filter bar visible with 3 dropdowns:
  - [ ] Severity (All, Critical, Warning, Info, Success)
  - [ ] Status (All, Unread, Read)
  - [ ] Type (All, Disease, Sensor, Irrigation, Weather, Recommendation)

**Test Filtering:**
```
1. Severity: Critical → only critical alerts show
2. Status: Unread → only unread alerts show
3. Type: Disease → only disease alerts show
4. Reset filters → all alerts show
```

**If alerts exist:**
- [ ] Alert items display with:
  - [ ] Severity icon (colored)
  - [ ] Severity badge
  - [ ] NEW badge for unread
  - [ ] Alert title
  - [ ] Alert message
  - [ ] Time ago display
  - [ ] Farm and Crop info
  - [ ] Mark as Read button (if unread)
  - [ ] Delete button

**Expected Result:** Alerts page fully functional with filtering

---

### 5️⃣ Navigation

- [ ] Navbar visible on all pages
- [ ] Logo links to dashboard
- [ ] All nav links work:
  - [ ] Dashboard
  - [ ] Farms
  - [ ] Crops
  - [ ] Weather
  - [ ] Alerts
- [ ] User menu works:
  - [ ] Profile link
  - [ ] Logout link
- [ ] Alert bell shows unread count

**Expected Result:** Navigation works across all pages

---

### 6️⃣ Authentication

**Test Login:**
- [ ] Navigate to /auth
- [ ] Login tab selected by default
- [ ] Email field accepts input
- [ ] Password field is masked
- [ ] Login button works
- [ ] JWT token stored in localStorage
- [ ] Redirected to dashboard after login

**Test Logout:**
- [ ] Click user menu → Logout
- [ ] Token removed from localStorage
- [ ] Redirected to auth page

**Test Register:**
- [ ] Click Register tab
- [ ] Email, password, confirm password fields
- [ ] Username field (optional)
- [ ] Register button works
- [ ] Account created successfully

**Expected Result:** Authentication working properly

---

### 7️⃣ Responsive Design

**Desktop (1920x1080):**
- [ ] Sidebar visible
- [ ] Full grid layouts
- [ ] Charts display properly

**Tablet (768x1024):**
- [ ] Mobile menu appears
- [ ] Content stacks appropriately
- [ ] Forms are usable

**Mobile (375x667):**
- [ ] Hamburger menu works
- [ ] Single column layout
- [ ] Touch targets are large enough
- [ ] Charts stack vertically
- [ ] Tables are scrollable

**Test Mobile:** Press F12 → Toggle Device Toolbar

**Expected Result:** Responsive design works on all screen sizes

---

## 🐛 Common Issues & Fixes

### Issue: "Page not found" on /crops or /alerts
**Solution:** Restart Flask app - routes need to be reloaded
```bash
# Stop: Ctrl+C
# Restart: python app.py
```

### Issue: Charts not loading on dashboard
**Solution:** Check browser console (F12) for JavaScript errors. Ensure Chart.js CDN is accessible.

### Issue: CORS errors
**Solution:** Make sure `CORS()` is initialized in app.py if needed

### Issue: 401 Unauthorized on API calls
**Solution:** 
1. Clear localStorage in DevTools
2. Log in again to get fresh token
3. Check token is being sent in headers

### Issue: Database errors
**Solution:** 
1. Check MySQL is running
2. Verify credentials in `config/config.py`
3. Ensure database exists

---

## 📊 Test Data Suggestions

### Test Farm
```
Name: Organic Greens Farm
Location: Pune, Maharashtra
Area: 75 hectares
Notes: Organic certification pending
```

### Test Crops (Add 3-4)
```
Crop 1: Tomatoes
  Variety: Himsona
  Planting: 2024-01-20
  Harvest: 2024-04-20
  Area: 5
  Stage: Growing

Crop 2: Wheat
  Variety: PBW 343
  Planting: 2023-11-15
  Harvest: 2024-04-15
  Area: 15
  Stage: Growing

Crop 3: Rice
  Variety: Basmati
  Planting: 2024-06-01
  Harvest: 2024-09-30
  Area: 25
  Stage: Seedling
```

---

## ✅ Final Verification

After testing all features, verify:

- [ ] Dashboard displays correctly with all components
- [ ] Crops page has full CRUD functionality
- [ ] Alerts page shows and filters alerts
- [ ] Navigation works across pages
- [ ] Authentication is secure
- [ ] Responsive design works
- [ ] No console errors (F12)
- [ ] Page load times are acceptable
- [ ] Buttons and forms are responsive
- [ ] Mobile experience is smooth

---

## 🎯 Success Criteria

✅ **Phase 1 is considered successful when:**

1. ✅ All 5 pages load without errors
2. ✅ Dashboard displays charts and sensor data
3. ✅ Crops page has working CRUD + filters
4. ✅ Alerts page shows and filters alerts
5. ✅ Navigation is working across pages
6. ✅ Authentication is functional
7. ✅ Responsive design works on all devices
8. ✅ No JavaScript errors in console
9. ✅ All quick action buttons work
10. ✅ User experience is smooth

---

## 📝 Test Report Template

**Date:** ___________  
**Tester:** ___________  
**Platform:** ___________  
**Browser:** ___________  

**Overall Status:** [ ] Pass [ ] Fail

**Component Test Results:**
- Dashboard: [ ] Pass [ ] Fail
- Crops: [ ] Pass [ ] Fail
- Alerts: [ ] Pass [ ] Fail
- Navigation: [ ] Pass [ ] Fail
- Auth: [ ] Pass [ ] Fail
- Responsive: [ ] Pass [ ] Fail

**Issues Found:**
```
1. 
2. 
3. 
```

**Notes:**
```


```

---

## 🚀 Ready for Phase 2?

When Phase 1 testing is complete and all items pass, the system is ready for:
- User feedback collection
- Performance optimization
- Phase 2 development (User Profile, Recommendations, Analytics)
- Deployment to staging environment

---

**Good luck with testing! 🎉**
