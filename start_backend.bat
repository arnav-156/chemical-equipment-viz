@echo off
echo Starting Chemical Equipment Visualizer Backend...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run Django development server
echo Starting Django server at http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
python manage.py runserver
