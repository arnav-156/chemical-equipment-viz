# Chemical Equipment Visualizer - Web Frontend

React-based web frontend for the Chemical Equipment Parameter Visualizer.

## Features

- 🔐 User authentication (login/register)
- 📤 CSV file upload with drag-and-drop
- 📊 Interactive data visualization with Chart.js
- 📈 Real-time analytics and statistics
- 📄 PDF report generation and download
- 📱 Responsive design (mobile-friendly)
- 🎨 Modern UI with gradient themes

## Tech Stack

- **React 19** - UI framework
- **React Router** - Navigation
- **Axios** - HTTP client
- **Chart.js** - Data visualization
- **CSS3** - Styling

## Prerequisites

- Node.js 14+ and npm
- Django backend running on http://localhost:8000

## Installation

```bash
# Install dependencies
npm install

# Start development server
npm start
```

The app will open at http://localhost:3000

## Project Structure

```
src/
├── components/          # Reusable components
│   ├── FileUpload.js   # CSV upload component
│   ├── DatasetList.js  # Dataset list component
│   ├── SummaryCards.js # Statistics cards
│   ├── Charts.js       # Chart.js visualizations
│   └── DataTable.js    # Equipment data table
├── pages/              # Page components
│   ├── Login.js        # Login page
│   ├── Register.js     # Registration page
│   └── Dashboard.js    # Main dashboard
├── services/           # API services
│   └── api.js          # API client and endpoints
├── utils/              # Utility functions
│   ├── auth.js         # Authentication helpers
│   └── PrivateRoute.js # Protected route component
├── App.js              # Main app component
└── index.js            # Entry point
```

## Available Scripts

### `npm start`
Runs the app in development mode at http://localhost:3000

### `npm run build`
Builds the app for production to the `build` folder

### `npm test`
Launches the test runner

## Environment Variables

Create a `.env` file in the root directory:

```env
REACT_APP_API_URL=http://localhost:8000/api
PORT=3000
```

## Features in Detail

### Authentication
- Token-based authentication
- Automatic token refresh
- Protected routes
- Session persistence

### File Upload
- Drag-and-drop interface
- File validation (CSV only)
- Upload progress indicator
- Error handling

### Data Visualization
- Bar chart for equipment type distribution
- Line chart for parameter trends
- Pie chart for type percentages
- Responsive and interactive charts

### Dashboard
- Recent datasets (last 5)
- Summary statistics with min/max ranges
- Equipment details table
- PDF report download

## API Integration

The frontend communicates with the Django backend API:

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

## Building for Production

```bash
# Create production build
npm run build

# The build folder is ready to be deployed
```

## Deployment

### Vercel
```bash
npm install -g vercel
vercel
```

### Netlify
```bash
npm run build
# Upload build folder to Netlify
```

### GitHub Pages
```bash
npm install --save-dev gh-pages

# Add to package.json:
"homepage": "https://yourusername.github.io/chemical-equipment-viz",
"scripts": {
  "predeploy": "npm run build",
  "deploy": "gh-pages -d build"
}

# Deploy
npm run deploy
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License
