# Chemical Equipment Parameter Visualizer

A hybrid Web + Desktop application for visualizing and analyzing chemical equipment data.

## Tech Stack

- **Backend**: Django + Django REST Framework
- **Web Frontend**: React.js + Chart.js
- **Desktop Frontend**: PyQt5 + Matplotlib
- **Database**: SQLite
- **Data Processing**: Pandas

## Features

- CSV file upload for equipment data
- Data visualization with charts
- Summary statistics and analytics
- PDF report generation
- User authentication
- History management (last 5 datasets)
- Dual interface (Web + Desktop)

## Project Structure

```
chemical-equipment-viz/
├── backend/              # Django project settings
├── equipment/            # Django app for equipment management
├── web-frontend/         # React web application (to be created)
├── desktop-app/          # PyQt5 desktop application (to be created)
├── sample_equipment_data.csv
├── requirements.txt
└── manage.py
```

## Setup Instructions

### Backend Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create superuser:
```bash
python manage.py createsuperuser
```

5. Run development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

### API Endpoints

- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/datasets/` - List last 5 datasets
- `POST /api/datasets/upload/` - Upload CSV file
- `GET /api/datasets/<id>/` - Get specific dataset with equipment
- `GET /api/datasets/<id>/summary/` - Get analytics summary
- `GET /api/datasets/<id>/report/` - Generate PDF report

### Web Frontend Setup (Coming Next)

Instructions will be added after React frontend is created.

### Desktop App Setup (Coming Next)

Instructions will be added after PyQt5 desktop app is created.

## Sample Data

Use `sample_equipment_data.csv` for testing. The CSV should have the following columns:
- Equipment Name
- Type
- Flowrate
- Pressure
- Temperature

## Authentication

The API uses token-based authentication. Include the token in the Authorization header:
```
Authorization: Token <your-token-here>
```

## Development Status

- [x] Phase 1: Backend Setup & API
- [ ] Phase 2: React Web Frontend
- [ ] Phase 3: PyQt5 Desktop App
- [ ] Phase 4: Testing & Documentation
- [ ] Phase 5: Deployment

## License

MIT License
