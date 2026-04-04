# ⚡ PHASE 1 QUICK START - 5 MINUTE SETUP

**Get the Smart Agriculture platform running in 5 minutes**

---

## 🚀 Start the App (3 minutes)

```bash
# 1. Open PowerShell/CMD
# 2. Go to project folder
cd c:\Users\HP\OneDrive\Desktop\smart_agriculture

# 3. Activate environment
.venv\Scripts\activate

# 4. Start Flask
python app.py

# 5. You should see:
# * Running on http://127.0.0.1:5000
```

**✅ App is running!**

---

## 🌐 Open in Browser

Click this link or paste in your browser:
```
http://127.0.0.1:5000
```

**You should see the Smart Agriculture homepage**

---

## 🔐 Login (1 minute)

Click **Login** button and use:

```
Email:    test@example.com
Password: password123
```

Click **Login** → You're in! 🎉

---

## 📱 What to Check (1 minute)

### 1. Dashboard
**Click Dashboard** in the navbar
- ✅ See 4 charts (Moisture, Temp, Humidity, pH)
- ✅ See sensor stats cards
- ✅ See crop health cards
- ✅ See Quick Actions buttons

### 2. Crops ✨ NEW
**Click Crops** in the navbar
- ✅ Click "Add Crop" button
- ✅ Fill in: Crop Name, Farm, Dates, Stage
- ✅ Click Save
- ✅ Crop appears in list with health score
- ✅ Search and filter crops

### 3. Alerts ✨ NEW
**Click Alerts** in the navbar
- ✅ See alert list with severity badges
- ✅ Use filters (Severity, Status, Type)
- ✅ Click "Mark All as Read"
- ✅ See statistics update

---

## 🎯 Page Navigation

| Page | URL | What to See |
|------|-----|------------|
| **Home** | / | Welcome page |
| **Auth** | /auth | Login/Register |
| **Dashboard** | /dashboard | Charts & overview |
| **Farms** | /farms | Farm management |
| **Crops** | /crops | Crop CRUD (NEW) |
| **Weather** | /weather | Weather forecast |
| **Alerts** | /alerts | Alert center (NEW) |

---

## 📊 Quick Features Demo

### Add a Test Farm
1. Go to **Farms**
2. Click "Add Farm"
3. Enter:
   - Name: `Test Farm`
   - Location: `Mumbai`
   - Area: `50`
4. Click Save ✅

### Add a Test Crop
1. Go to **Crops**
2. Click "Add Crop"
3. Enter:
   - Farm: `Test Farm`
   - Crop Name: `Wheat`
   - Planting Date: `2024-01-15`
   - Harvest Date: `2024-05-15`
   - Stage: `Growing`
4. Click Save ✅

### View Alerts
1. Go to **Alerts**
2. See all alerts (if any)
3. Filter by severity or status
4. Mark as read or delete ✅

---

## 🛠️ Troubleshooting

### Flask won't start?
```bash
# Kill any existing Flask process
# (Ctrl+C if running)

# Restart with fresh activation:
.venv\Scripts\deactivate
.venv\Scripts\activate
python app.py
```

### Can't access http://127.0.0.1:5000?
- ✅ Check Flask is running (you should see "Running on..." message)
- ✅ Try `http://localhost:5000` instead
- ✅ Check port 5000 is not blocked

### Login not working?
- ✅ Check email/password are correct (test@example.com / password123)
- ✅ Open DevTools (F12) to see error messages
- ✅ Try creating a new account with Register button

### Pages not loading?
- ✅ Refresh browser (F5)
- ✅ Clear cache (Ctrl+Shift+Del)
- ✅ Restart Flask app

---

## 💾 File Structure

All Phase 1 files are here:
```
templates/
  ├── dashboard.html    (898 lines - Charts!)
  ├── crops.html        (730 lines - NEW!)
  ├── alerts.html       (640 lines - NEW!)
  ├── farms.html        (450 lines)
  ├── auth.html         (340 lines)
  └── weather.html      (280 lines)

app.py                  (Updated with /crops and /alerts routes)
```

---

## ✨ Phase 1 Features Summary

✅ **Dashboard** - Real-time charts with Chart.js
✅ **Crops** - Full CRUD management with health scoring  
✅ **Alerts** - Alert center with filtering and statistics
✅ **Farms** - Farm management system
✅ **Auth** - Secure JWT authentication
✅ **API** - 55+ working endpoints
✅ **Database** - 13 models, fully functional
✅ **Responsive** - Works on desktop, tablet, mobile

---

## 🎯 Next Steps

1. **Test the features** - Follow testing guide (PHASE1_TESTING_GUIDE.md)
2. **Add more test data** - Create farms and crops
3. **Check alerts** - See if any alerts appear
4. **Try mobile view** - Resize browser to test responsiveness
5. **Read docs** - Check PHASE1_COMPLETE.md for details

---

## 📚 Documentation Files

- **PHASE1_COMPLETE.md** - Full build report (features, hours, stats)
- **PHASE1_TESTING_GUIDE.md** - Detailed testing checklist
- **BUILD_GUIDE.md** - Roadmap for all 11 pages
- **FEATURES_ROADMAP.md** - Your 16 features mapped to implementation
- **START_HERE.md** - Main documentation index

---

## 🚪 Logout

To logout, click the **user icon** (top right) → **Logout**

---

## ✅ You're All Set!

You now have a fully functional Smart Agriculture platform with:
- 📊 Real-time monitoring dashboard
- 🌾 Crop management system
- 🔔 Alert notifications center
- 👥 User authentication
- 📱 Responsive mobile design

**Enjoy! 🎉**

Questions? Check the documentation or review the code in the templates folder.

---

**Need help?** Check the browser console (F12) for error messages.
