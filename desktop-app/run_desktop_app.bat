@echo off
echo ========================================
echo Chemical Equipment Visualizer
echo Desktop Application
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
    
    echo Installing dependencies...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    echo.
) else (
    call venv\Scripts\activate.bat
)

echo Starting desktop application...
echo.
echo Make sure Django backend is running on http://localhost:8000
echo.

python main.py

pause
