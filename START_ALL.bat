@echo off
echo ========================================
echo Chemical Equipment Visualizer
echo Starting Backend and Frontend
echo ========================================
echo.

echo Starting Django Backend...
start cmd /k "cd /d %~dp0 && venv\Scripts\activate && python manage.py runserver"

timeout /t 3 /nobreak > nul

echo Starting React Frontend...
start cmd /k "cd /d %~dp0web-frontend && npm start"

echo.
echo ========================================
echo Both servers are starting!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit this window...
pause > nul
