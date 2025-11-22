# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Start the Backend Server

**Windows:**
```bash
start_backend.bat
```

**Manual (all platforms):**
```bash
# Activate virtual environment
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Start server
python manage.py runserver
```

The server will start at: **http://localhost:8000**

### Step 2: Test the API

Open a new terminal and run:

```bash
.\venv\Scripts\activate
python test_api.py
```

This will:
- ✅ Login with test user
- ✅ Upload sample CSV
- ✅ List datasets
- ✅ Get dataset details
- ✅ Generate PDF report

### Step 3: Explore the API

#### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"testuser\",\"password\":\"testpass123\"}"
```

Response:
```json
{
  "token": "1159f76ae5c26fd5177ea22117a7f8ebbb298cb2",
  "user_id": 1,
  "username": "testuser"
}
```

#### Upload CSV
```bash
curl -X POST http://localhost:8000/api/datasets/upload/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "file=@sample_equipment_data.csv"
```

#### List Datasets
```bash
curl http://localhost:8000/api/datasets/ \
  -H "Authorization: Token YOUR_TOKEN"
```

#### Get Dataset Details
```bash
curl http://localhost:8000/api/datasets/1/ \
  -H "Authorization: Token YOUR_TOKEN"
```

#### Download PDF Report
```bash
curl http://localhost:8000/api/datasets/1/report/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -o report.pdf
```

## 📊 Admin Panel

1. Create superuser:
```bash
python manage.py createsuperuser
```

2. Access admin at: **http://localhost:8000/admin**

## 🔑 Test Credentials

- **Username**: testuser
- **Password**: testpass123
- **Token**: 1159f76ae5c26fd5177ea22117a7f8ebbb298cb2

## 📁 Sample CSV Format

Your CSV file should have these columns:
```
Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor-A1,Reactor,150.5,25.3,180.2
Heat Exchanger-B2,Heat Exchanger,200.0,15.8,120.5
...
```

See `sample_equipment_data.csv` for a complete example.

## 🎯 API Endpoints Summary

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | Register new user | No |
| POST | `/api/auth/login/` | Login and get token | No |
| POST | `/api/auth/logout/` | Logout | Yes |
| GET | `/api/datasets/` | List last 5 datasets | Yes |
| POST | `/api/datasets/upload/` | Upload CSV file | Yes |
| GET | `/api/datasets/<id>/` | Get dataset details | Yes |
| GET | `/api/datasets/<id>/summary/` | Get analytics | Yes |
| GET | `/api/datasets/<id>/report/` | Download PDF | Yes |

## 🐛 Troubleshooting

**Server won't start?**
- Make sure virtual environment is activated
- Check if port 8000 is available
- Run: `python manage.py migrate`

**Can't upload CSV?**
- Check file format (must be .csv)
- Verify required columns exist
- Check file size (should be reasonable)

**Authentication errors?**
- Make sure to include token in header: `Authorization: Token YOUR_TOKEN`
- Token is returned from login endpoint

## 📚 Next Steps

1. ✅ Backend is ready!
2. ⏳ Create React web frontend
3. ⏳ Create PyQt5 desktop app
4. ⏳ Deploy to production

See `PROJECT_STATUS.md` for detailed progress and next steps.

## 💡 Tips

- Use the test script (`test_api.py`) to verify everything works
- Check `PROJECT_STATUS.md` for complete project status
- Read `README.md` for full documentation
- Sample data is in `sample_equipment_data.csv`

## 🎉 You're Ready!

The backend is fully functional. You can now:
- Build the React web frontend
- Build the PyQt5 desktop app
- Both will connect to this same API

Happy coding! 🚀
