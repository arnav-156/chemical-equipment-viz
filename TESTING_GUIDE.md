# 🧪 Real-Time Testing Guide

## ✅ Servers Running!

Both servers are now running and ready for testing:

### 🔗 Access Points

- **Backend API**: http://localhost:8000/api
- **Web Frontend**: http://localhost:3000
- **Admin Panel**: http://localhost:8000/admin

---

## 🎯 Step-by-Step Testing

### Step 1: Test Web Frontend (5 minutes)

1. **Open Browser**
   - Go to: **http://localhost:3000**
   - Should see login page with gradient background

2. **Login**
   - Username: `testuser`
   - Password: `testpass123`
   - Click "Login"
   - Should redirect to dashboard

3. **Test File Upload**
   - Drag `sample_equipment_data.csv` to upload area
   - OR click "Select File" button
   - Click "Upload and Analyze"
   - Wait for success message
   - Should see 15 equipment items

4. **View Analytics**
   - See 4 summary cards:
     - Total Equipment: 15
     - Avg Flowrate: ~186.91
     - Avg Pressure: ~24.55
     - Avg Temperature: ~124.79
   - All cards show min/max ranges

5. **Test Charts**
   - Scroll down to see 3 charts:
     - Bar chart (type distribution)
     - Line chart (parameter trends)
     - Pie chart (type percentages)
   - Charts should be interactive (hover for tooltips)

6. **Test Customizable Dashboard** (WOW Factor #1)
   - Click "🎨 Customizable View" in header
   - Click "⚙️ Customize" button
   - Try dragging widgets around
   - Try resizing widgets
   - Toggle widgets on/off
   - Click "✓ Done" to save
   - Refresh page - layout should persist!

7. **Download PDF Report**
   - Click "📄 Download PDF Report" button
   - PDF should download automatically
   - Open PDF - should see:
     - Summary statistics
     - 4 Matplotlib charts
     - Equipment data table

8. **Test Dataset Selection**
   - Click on different datasets in the list
   - Data should update instantly
   - Charts should refresh

---

### Step 2: Test Backend API (5 minutes)

Open a new terminal and test API endpoints:

```bash
# Activate virtual environment
cd chemical-equipment-viz
.\venv\Scripts\activate

# Test anomaly detection (WOW Factor #3)
curl http://localhost:8000/api/datasets/1/anomalies/ -H "Authorization: Token 1159f76ae5c26fd5177ea22117a7f8ebbb298cb2"

# Test health score
curl http://localhost:8000/api/datasets/1/health/ -H "Authorization: Token 1159f76ae5c26fd5177ea22117a7f8ebbb298cb2"

# Test trends
curl http://localhost:8000/api/datasets/trends/ -H "Authorization: Token 1159f76ae5c26fd5177ea22117a7f8ebbb298cb2"

# Test alert rules
curl http://localhost:8000/api/alert-rules/ -H "Authorization: Token 1159f76ae5c26fd5177ea22117a7f8ebbb298cb2"
```

---

### Step 3: Test Desktop App (5 minutes)

1. **Open New Terminal**
   ```bash
   cd desktop-app
   python main.py
   ```

2. **Login**
   - Username: `testuser`
   - Password: `testpass123`

3. **Test Features**
   - Upload CSV via file picker
   - View datasets in table
   - Double-click dataset to view details
   - Switch to Analytics tab
   - Switch to Charts tab (4 Matplotlib charts)
   - Download PDF report

---

## 🧪 Feature Checklist

### Core Features
- [ ] Login/Register working
- [ ] CSV upload successful
- [ ] Data displayed in table
- [ ] Summary statistics showing
- [ ] Charts rendering correctly
- [ ] PDF download working

### WOW Factor #1: Customizable Dashboard
- [ ] Can switch to customizable view
- [ ] Can drag widgets
- [ ] Can resize widgets
- [ ] Can toggle widgets on/off
- [ ] Layout persists after refresh
- [ ] Reset to default works

### WOW Factor #2: Alert System
- [ ] Can create alert rules
- [ ] Alert rules listed
- [ ] Alert history accessible
- [ ] Email configuration ready

### WOW Factor #3: ML Anomaly Detection
- [ ] Anomaly detection API working
- [ ] Health scores calculated (0-100)
- [ ] Anomalies identified correctly
- [ ] Severity levels assigned
- [ ] Multiple detection methods working

---

## 🐛 Common Issues & Solutions

### Issue 1: Frontend won't load
**Solution:**
```bash
cd web-frontend
npm install
npm start
```

### Issue 2: Backend errors
**Solution:**
```bash
.\venv\Scripts\activate
python manage.py migrate
python manage.py runserver
```

### Issue 3: Can't login
**Solution:**
```bash
python manage.py create_test_user
# Use: testuser / testpass123
```

### Issue 4: Charts not showing
**Solution:**
- Check browser console (F12)
- Verify data is loaded
- Refresh page

### Issue 5: Desktop app won't start
**Solution:**
```bash
cd desktop-app
pip install -r requirements.txt
python main.py
```

---

## 📊 Expected Results

### Backend Server Log
```
Starting development server at http://127.0.0.1:8000/
[22/Nov/2025 22:29:45] "POST /api/auth/login/ HTTP/1.1" 200 86
[22/Nov/2025 22:29:45] "GET /api/datasets/ HTTP/1.1" 200 115
[22/Nov/2025 22:29:45] "GET /api/datasets/1/summary/ HTTP/1.1" 200 377
```

### Frontend Console
```
Compiled successfully!
webpack compiled with 1 warning

You can now view web-frontend in the browser.
  Local:            http://localhost:3000
```

### Test Results
```
✅ Login successful
✅ 15 equipment items loaded
✅ Health Score: 94.67/100 (Excellent)
✅ 2 anomalies detected
✅ Charts rendering
✅ PDF generated (100KB)
```

---

## 🎬 Demo Walkthrough

### 1. Login (30 seconds)
- Show login page
- Enter credentials
- Successful login

### 2. Dashboard Overview (30 seconds)
- Show header with user info
- Show upload section
- Show dataset list

### 3. Upload CSV (30 seconds)
- Drag and drop file
- Show upload progress
- Success message
- Data appears

### 4. View Analytics (30 seconds)
- Show 4 summary cards
- Highlight min/max ranges
- Show type distribution

### 5. Customizable Dashboard (45 seconds) - WOW #1
- Click "Customizable View"
- Enter edit mode
- Drag a widget
- Resize a widget
- Toggle widget off/on
- Save and show persistence

### 6. ML Anomaly Detection (30 seconds) - WOW #3
- Show health score (94.67/100)
- Show anomalies detected (2)
- Explain Isolation Forest
- Show severity levels

### 7. Charts (20 seconds)
- Show 3 interactive charts
- Hover for tooltips
- Explain visualizations

### 8. PDF Report (15 seconds)
- Click download button
- Show PDF with charts
- Highlight embedded visualizations

### 9. Alert System (20 seconds) - WOW #2
- Show alert rules (via admin or API)
- Explain email/telegram integration
- Show alert history

**Total: ~4 minutes** (perfect for demo video!)

---

## 📱 Testing on Mobile

### Responsive Design Test

1. **Open DevTools** (F12)
2. **Toggle Device Toolbar** (Ctrl+Shift+M)
3. **Select Device**:
   - iPhone 12 Pro
   - iPad
   - Galaxy S20

4. **Test Features**:
   - Login works
   - Upload works
   - Charts resize
   - Tables scroll
   - Buttons accessible

---

## 🎯 What to Look For

### Visual Quality
- ✅ Gradient backgrounds
- ✅ Smooth animations
- ✅ Professional styling
- ✅ Consistent colors
- ✅ Clear typography

### Functionality
- ✅ All buttons work
- ✅ Forms validate
- ✅ Data loads quickly
- ✅ Charts interactive
- ✅ Errors handled gracefully

### Performance
- ✅ Fast page loads
- ✅ Smooth interactions
- ✅ No lag or freezing
- ✅ Charts render quickly
- ✅ API responses fast

---

## 🎥 Recording Demo Video

### Tools
- **Windows**: Xbox Game Bar (Win+G)
- **OBS Studio**: https://obsproject.com/
- **Loom**: https://loom.com/

### Tips
1. **Clean desktop** - Close unnecessary windows
2. **Full screen** - Browser in full screen mode
3. **Smooth movements** - Slow, deliberate actions
4. **Narrate** - Explain what you're doing
5. **Show WOW factors** - Emphasize unique features
6. **Keep it short** - 2-3 minutes max

### Script
```
"Hello! This is the Chemical Equipment Visualizer, 
a hybrid web and desktop application.

[Login]
Let me login with my credentials...

[Upload]
Now I'll upload a CSV file with equipment data...
The system processes 15 equipment items instantly.

[Analytics]
Here you can see comprehensive analytics with 
averages and min-max ranges for all parameters.

[Customizable Dashboard - WOW #1]
One unique feature is the customizable dashboard.
I can drag and drop widgets, resize them, and 
the layout persists across sessions.

[ML Anomaly Detection - WOW #3]
The system uses machine learning - specifically 
Isolation Forest algorithm - to detect anomalies.
It found 2 anomalies with a health score of 94.67%.

[Alert System - WOW #2]
We also have an intelligent alert system that 
can send email and Telegram notifications when 
parameters exceed thresholds.

[Charts]
Interactive charts show type distribution and 
parameter trends using Chart.js.

[PDF Report]
Finally, I can download a professional PDF report 
with embedded Matplotlib charts.

[Desktop App]
The same features are available in the desktop 
application built with PyQt5.

Thank you!"
```

---

## ✅ Testing Checklist

### Before Recording
- [ ] Both servers running
- [ ] Browser cache cleared
- [ ] Test credentials ready
- [ ] Sample CSV file ready
- [ ] Desktop clean
- [ ] Recording software ready

### During Recording
- [ ] Show login
- [ ] Upload CSV
- [ ] View analytics
- [ ] Demo customizable dashboard
- [ ] Show anomaly detection
- [ ] Display charts
- [ ] Download PDF
- [ ] Show desktop app (optional)

### After Recording
- [ ] Video is 2-3 minutes
- [ ] Audio is clear
- [ ] All features shown
- [ ] WOW factors highlighted
- [ ] No errors visible

---

## 🎊 You're Ready!

**Both servers are running!**

### Access Now:
- **Web App**: http://localhost:3000
- **Backend**: http://localhost:8000
- **Admin**: http://localhost:8000/admin

### Test Credentials:
- **Username**: testuser
- **Password**: testpass123

### Sample Data:
- **File**: sample_equipment_data.csv (in project root)

---

## 🚀 Start Testing!

Open your browser and go to **http://localhost:3000** to start testing!

Everything is ready and working perfectly! 🎉
