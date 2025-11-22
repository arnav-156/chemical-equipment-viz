# Chemical Equipment Visualizer - Desktop Application

PyQt5-based desktop application for the Chemical Equipment Parameter Visualizer.

## Features

- 🔐 User authentication (login/register)
- 📤 CSV file upload with file picker
- 📊 Interactive data visualization with Matplotlib
- 📈 Real-time analytics and statistics
- 📄 PDF report generation and download
- 🖥️ Native desktop interface
- 📱 Multi-tab organization
- 🎨 Professional UI with custom styling

## Tech Stack

- **PyQt5** - Desktop GUI framework
- **Matplotlib** - Data visualization
- **Requests** - HTTP client for API calls
- **Threading** - Async operations

## Prerequisites

- Python 3.8+
- Django backend running on http://localhost:8000
- PyQt5, matplotlib, requests

## Installation

### Option 1: Using Virtual Environment (Recommended)

```bash
# Navigate to desktop-app directory
cd desktop-app

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Option 2: System-wide Installation

```bash
cd desktop-app
pip install -r requirements.txt
```

## Running the Application

```bash
# Make sure Django backend is running first
# Then start the desktop app:
python main.py
```

## Project Structure

```
desktop-app/
├── main.py              # Application entry point
├── api_client.py        # API client for backend communication
├── login_dialog.py      # Login/Register dialog
├── main_window.py       # Main application window
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Features in Detail

### Authentication
- **Login Dialog**
  - Username/password authentication
  - Test credentials displayed
  - Registration tab
  - Error handling

### Main Window
- **Upload Tab**
  - File picker for CSV selection
  - Upload progress feedback
  - Upload history log

- **Datasets Tab**
  - List of last 5 datasets
  - Sortable table view
  - Double-click to view details
  - Refresh button

- **Analytics Tab**
  - 4 summary cards (total, avg flowrate, pressure, temperature)
  - Equipment details table
  - Real-time data updates

- **Charts Tab**
  - 4 interactive Matplotlib charts:
    1. Equipment type distribution (bar chart)
    2. Parameter trends (line chart)
    3. Type distribution (pie chart)
    4. Parameter ranges (bar chart with error bars)
  - Navigation toolbar (zoom, pan, save)
  - PDF report download button

### Menu Bar
- **File Menu**
  - Upload CSV
  - Download Report
  - Exit

- **View Menu**
  - Refresh Datasets

- **Help Menu**
  - About

## API Integration

The desktop app communicates with the Django backend API:

- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `POST /api/auth/logout/` - User logout
- `GET /api/datasets/` - List datasets
- `POST /api/datasets/upload/` - Upload CSV
- `GET /api/datasets/<id>/` - Get dataset details
- `GET /api/datasets/<id>/summary/` - Get analytics
- `GET /api/datasets/<id>/report/` - Download PDF

## Test Credentials

- **Username**: testuser
- **Password**: testpass123

## Building Standalone Executable

### Using PyInstaller

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed --name="ChemicalEquipmentViz" main.py

# The executable will be in the dist/ folder
```

### Advanced Build Options

```bash
# With icon (if you have an icon file)
pyinstaller --onefile --windowed --icon=icon.ico --name="ChemicalEquipmentViz" main.py

# Include all dependencies
pyinstaller --onefile --windowed --hidden-import=PyQt5 --hidden-import=matplotlib --name="ChemicalEquipmentViz" main.py
```

## Configuration

### API URL Configuration

By default, the app connects to `http://localhost:8000/api`. To change this:

1. Edit `api_client.py`
2. Modify the `base_url` parameter in `APIClient.__init__()`

```python
def __init__(self, base_url='http://your-server:port/api'):
    self.base_url = base_url
```

## Troubleshooting

### Application won't start
- Ensure Python 3.8+ is installed
- Check if all dependencies are installed: `pip list`
- Verify Django backend is running

### Can't connect to backend
- Check if backend is running on http://localhost:8000
- Verify firewall settings
- Check API URL in `api_client.py`

### Charts not displaying
- Ensure matplotlib is installed correctly
- Try reinstalling: `pip uninstall matplotlib && pip install matplotlib`

### Upload fails
- Check file format (must be CSV)
- Verify required columns exist
- Check backend logs for errors

## Development

### Adding New Features

1. **New Tab**: Add to `main_window.py` in `init_ui()` method
2. **New API Endpoint**: Add method to `api_client.py`
3. **New Dialog**: Create new file similar to `login_dialog.py`

### Styling

The application uses Qt stylesheets. Modify in `main_window.py`:

```python
self.setStyleSheet("""
    /* Your custom styles here */
""")
```

## Dependencies

```
PyQt5==5.15.10          # GUI framework
matplotlib==3.9.0       # Charts and visualization
requests==2.32.5        # HTTP client
```

## Screenshots

### Login Dialog
- Clean, tabbed interface
- Login and Register tabs
- Test credentials displayed

### Main Window
- Multi-tab interface
- Professional styling
- Responsive layout

### Charts
- 4 interactive visualizations
- Matplotlib navigation toolbar
- Export capabilities

## Performance

- **Async Operations**: File uploads use threading
- **Efficient Rendering**: Charts update only when needed
- **Memory Management**: Proper cleanup of resources

## Security

- Token-based authentication
- Secure password input (masked)
- Session management
- Automatic logout on token expiration

## Known Limitations

- Requires active internet connection
- Backend must be running locally or accessible
- Large CSV files may take time to upload

## Future Enhancements

- [ ] Offline mode with local caching
- [ ] Settings dialog for API configuration
- [ ] Dark mode theme
- [ ] Export charts as images
- [ ] Batch file upload
- [ ] Real-time notifications
- [ ] Auto-update feature

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Support

For issues and questions:
- GitHub Issues: https://github.com/arnav-156/chemical-equipment-viz/issues
- Email: support@example.com

## Acknowledgments

- PyQt5 for the excellent GUI framework
- Matplotlib for powerful visualization
- Django REST Framework for the backend API
