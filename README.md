# 🏭 Chemical Equipment Visualizer

A modern, full-stack Progressive Web App for visualizing and analyzing chemical equipment data with ML-powered insights. Features offline functionality, advanced visualizations, and a beautiful industrial-themed UI.

[![React](https://img.shields.io/badge/React-19.2.0-61DAFB?logo=react)](https://reactjs.org/)
[![Django](https://img.shields.io/badge/Django-5.1-092E20?logo=django)](https://www.djangoproject.com/)
[![PWA](https://img.shields.io/badge/PWA-Enabled-5A0FC8?logo=pwa)](https://web.dev/progressive-web-apps/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ Key Features

### 🎨 Modern UI/UX
- **Industrial Poetry Theme** - Dark, neon-accented design inspired by industrial aesthetics
- **Smooth Animations** - Framer Motion, GSAP, and custom particle effects
- **Aurora Background** - Dynamic gradient effects with Lenis smooth scrolling
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile

### 📊 Advanced Visualizations
- **Interactive Charts** - Bar, line, scatter, and pie charts with Chart.js
- **Network Graph** - D3.js-powered equipment relationship visualization
- **Comparison Mode** - Side-by-side dataset comparison with synchronized charts
- **Customizable Dashboard** - Drag-and-drop widget layout with react-grid-layout

### 🤖 ML-Powered Features
- **Anomaly Detection** - Isolation Forest algorithm identifies outliers
- **Smart Alerts** - Automatic threshold-based notifications
- **Predictive Analytics** - Statistical analysis and trend detection

### 📵 PWA Capabilities
- **Works Offline** - Full functionality without internet connection
- **Installable** - Install as native app on desktop and mobile
- **Service Worker** - Intelligent caching and background sync
- **Auto-Sync** - Syncs offline changes when connection restored

### 🚀 Additional Features
- User authentication with JWT tokens
- CSV file upload and parsing
- PDF report generation
- Dataset history management
- Real-time data validation
- Export functionality

## 🏗️ Tech Stack

### Frontend
- **React 19.2.0** - Modern UI library
- **React Router 7** - Client-side routing
- **Chart.js** - Data visualization
- **D3.js** - Network graph visualization
- **Framer Motion** - Smooth animations
- **GSAP** - Advanced animations
- **Lenis** - Smooth scrolling
- **Axios** - HTTP client

### Backend
- **Django 5.1** - Web framework
- **Django REST Framework** - API development
- **Pandas** - Data processing
- **Scikit-learn** - Machine learning
- **ReportLab** - PDF generation
- **SQLite** - Database

### PWA
- **Service Workers** - Offline functionality
- **IndexedDB** - Local data storage
- **Web App Manifest** - Installation support

## 📁 Project Structure

```
chemical-equipment-viz/
├── equipment/                    # Django app
│   ├── models.py                # Data models
│   ├── views.py                 # API endpoints
│   ├── serializers.py           # DRF serializers
│   ├── anomaly_detection.py     # ML algorithms
│   └── alerts.py                # Alert system
├── web-frontend/                # React PWA
│   ├── public/
│   │   ├── sw.js               # Service Worker
│   │   └── manifest.json       # PWA manifest
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── Charts.js
│   │   │   ├── ComparisonMode.js
│   │   │   ├── EquipmentNetworkGraph.js
│   │   │   ├── CustomizableDashboard.js
│   │   │   ├── OnlineStatus.js
│   │   │   └── InstallButton.js
│   │   ├── pages/              # Page components
│   │   │   ├── Login.js
│   │   │   ├── Dashboard.js
│   │   │   └── Features.js
│   │   ├── services/           # API & storage
│   │   │   ├── api.js
│   │   │   └── offlineStorage.js
│   │   └── styles/             # CSS files
│   └── package.json
├── desktop-app/                 # PyQt5 desktop app
├── requirements.txt             # Python dependencies
└── manage.py                    # Django management
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### 1. Clone Repository
```bash
git clone https://github.com/arnav-156/chemical-equipment-viz.git
cd chemical-equipment-viz
```

### 2. Backend Setup

**Create virtual environment:**
```bash
python -m venv venv
```

**Activate virtual environment:**
```bash
# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Run migrations:**
```bash
python manage.py migrate
```

**Create test user:**
```bash
python manage.py create_test_user
```
This creates a user: `test@example.com` / `testpass123`

**Start backend server:**
```bash
python manage.py runserver
```
Backend runs at: `http://localhost:8000`

### 3. Frontend Setup

**Open new terminal and navigate to frontend:**
```bash
cd web-frontend
```

**Install dependencies:**
```bash
npm install
```

**Start development server:**
```bash
npm start
```
Frontend runs at: `http://localhost:3000`

### 4. Access Application

1. Open browser to `http://localhost:3000`
2. Login with: `test@example.com` / `testpass123`
3. Upload CSV file from `sample_equipment_data.csv`
4. Explore features!

### 5. Test PWA Features

**Test Offline Mode:**
1. Open DevTools (F12)
2. Go to Network tab
3. Check "Offline" checkbox
4. Refresh page - app still works!

**Install as App:**
1. Look for install button (📱 Install App) in bottom-right
2. Click to install
3. App opens in standalone window

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout

### Datasets
- `GET /api/datasets/` - List datasets (last 5)
- `POST /api/datasets/upload/` - Upload CSV file
- `GET /api/datasets/<id>/` - Get dataset details
- `GET /api/datasets/<id>/summary/` - Get analytics summary
- `GET /api/datasets/<id>/report/` - Generate PDF report
- `GET /api/datasets/<id>/anomalies/` - Detect anomalies
- `GET /api/datasets/<id>/alerts/` - Get alerts

### Equipment
- `GET /api/equipment/` - List all equipment
- `GET /api/equipment/<id>/` - Get equipment details

## 🎨 Features Showcase

### Dashboard
- Upload CSV files with drag-and-drop
- View summary statistics cards
- Interactive charts (bar, line, scatter, pie)
- Dataset history with quick access
- Customizable widget layout

### Network Graph
- D3.js force-directed graph
- Shows equipment relationships
- Interactive nodes and links
- Zoom and pan controls
- Color-coded by equipment type

### Comparison Mode
- Compare two datasets side-by-side
- Synchronized chart interactions
- Difference highlighting
- Export comparison reports

### Anomaly Detection
- Isolation Forest algorithm
- Automatic outlier detection
- Visual anomaly highlighting
- Configurable sensitivity

### Offline Mode
- Works without internet
- Local data storage (IndexedDB)
- Background sync when online
- Visual online/offline indicator

## 📊 Sample Data

Use `sample_equipment_data.csv` for testing. Required CSV columns:
- **Equipment Name** - Unique identifier
- **Type** - Equipment category (Pump, Valve, Tank, etc.)
- **Flowrate** - Flow rate value
- **Pressure** - Pressure value
- **Temperature** - Temperature value

## 🔐 Authentication

Token-based authentication using Django REST Framework.

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'
```

**Use token in requests:**
```bash
curl http://localhost:8000/api/datasets/ \
  -H "Authorization: Token <your-token>"
```

## 🧪 Testing

### Test Backend
```bash
python manage.py test
```

### Test Frontend
```bash
cd web-frontend
npm test
```

### Test PWA
See `TEST_PWA_OFFLINE.md` for comprehensive PWA testing guide.

## 📚 Documentation

- **QUICKSTART.md** - Quick setup guide
- **DEPLOYMENT_GUIDE.md** - Deploy to production
- **PWA_COMPLETE.md** - PWA features and testing
- **TESTING_GUIDE.md** - Comprehensive testing
- **QUICK_DEMO_GUIDE.md** - 60-second demo script

## 🎯 Development Status

- ✅ Phase 1: Backend Setup & API
- ✅ Phase 2: Backend Enhancements (ML, Alerts, Caching)
- ✅ Phase 3: React Web Frontend
- ✅ Phase 4: Industrial Poetry Theme
- ✅ Phase 5: Advanced Visualizations (Network Graph, Comparison)
- ✅ Phase 6: PWA Implementation (Offline Mode)
- ✅ Phase 7: Desktop App (PyQt5)

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License - see LICENSE file for details

## 👨‍💻 Author

**Arnav**
- GitHub: [@arnav-156](https://github.com/arnav-156)

## 🙏 Acknowledgments

- React team for amazing framework
- Django team for robust backend
- Chart.js and D3.js for visualizations
- All open-source contributors

---

**⭐ Star this repo if you find it useful!**
