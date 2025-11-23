import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import ScrollStack, { ScrollStackItem } from '../components/ScrollStack';
import AuroraSimple from '../components/AuroraSimple';
import PillNav from '../components/PillNav';
import './Features.css';

const Features = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const currentPath = location.pathname;

  const navItems = [
    { label: 'Login', href: '/login' },
    { label: 'Features', href: '/features' },
    { label: 'Dashboard', href: '/dashboard' }
  ];

  return (
    <div className="features-page">
      <div className="aurora-background-features">
        <AuroraSimple colorStops={["#00FFA3", "#FF6B9D", "#FFD93D"]} />
      </div>

      {/* Pill Navigation */}
      <PillNav
        items={navItems}
        activeHref={currentPath}
        baseColor="#00FFA3"
        pillColor="#1E2749"
        hoveredPillTextColor="#0A0E27"
        pillTextColor="#00FFA3"
      />

      <div className="features-header">
        <h1>🧪 Chemical Equipment Visualizer</h1>
        <p>Powerful Features for Equipment Analysis</p>
      </div>

      <ScrollStack
        itemDistance={150}
        itemScale={0.05}
        itemStackDistance={40}
        stackPosition="25%"
        scaleEndPosition="15%"
        baseScale={0.9}
        rotationAmount={0}
        blurAmount={0}
      >
        <ScrollStackItem>
          <div className="feature-card feature-card-1">
            <div className="feature-icon">📊</div>
            <h2>Real-Time Data Visualization</h2>
            <p>
              Upload CSV files and instantly visualize your chemical equipment data
              with interactive charts and graphs. Support for temperature, pressure,
              flow rate, and efficiency metrics.
            </p>
            <ul>
              <li>Interactive line and bar charts</li>
              <li>Real-time data updates</li>
              <li>Multiple dataset comparison</li>
              <li>Export to PDF with embedded charts</li>
            </ul>
          </div>
        </ScrollStackItem>

        <ScrollStackItem>
          <div className="feature-card feature-card-2">
            <div className="feature-icon">🤖</div>
            <h2>ML-Powered Anomaly Detection</h2>
            <p>
              Advanced machine learning algorithms automatically detect anomalies
              in your equipment data using Isolation Forest technology. Get instant
              alerts when something looks unusual.
            </p>
            <ul>
              <li>Automatic anomaly detection</li>
              <li>Health score calculation (0-100)</li>
              <li>Isolation Forest algorithm</li>
              <li>Real-time anomaly alerts</li>
            </ul>
          </div>
        </ScrollStackItem>

        <ScrollStackItem>
          <div className="feature-card feature-card-3">
            <div className="feature-icon">🎨</div>
            <h2>Customizable Dashboard</h2>
            <p>
              Personalize your workspace with drag-and-drop widgets. Resize, reorder,
              and toggle visibility of dashboard components to match your workflow.
              Your layout is automatically saved.
            </p>
            <ul>
              <li>Drag-and-drop interface</li>
              <li>Resizable widgets</li>
              <li>Toggle widget visibility</li>
              <li>Auto-save layout preferences</li>
            </ul>
          </div>
        </ScrollStackItem>

        <ScrollStackItem>
          <div className="feature-card feature-card-4">
            <div className="feature-icon">🔔</div>
            <h2>Smart Alert System</h2>
            <p>
              Configure custom alerts for critical equipment parameters. Get notified
              when values exceed thresholds or when anomalies are detected. Multiple
              alert channels supported.
            </p>
            <ul>
              <li>Threshold-based alerts</li>
              <li>Anomaly notifications</li>
              <li>Email and in-app alerts</li>
              <li>Alert history tracking</li>
            </ul>
          </div>
        </ScrollStackItem>

        <ScrollStackItem>
          <div className="feature-card feature-card-5">
            <div className="feature-icon">📱</div>
            <h2>Multi-Platform Access</h2>
            <p>
              Access your data anywhere with our responsive web interface and native
              desktop application. Seamless synchronization across all your devices.
            </p>
            <ul>
              <li>Web application (React)</li>
              <li>Desktop app (PyQt6)</li>
              <li>Responsive design</li>
              <li>Cross-platform compatibility</li>
            </ul>
          </div>
        </ScrollStackItem>

        <ScrollStackItem>
          <div className="feature-card feature-card-6">
            <div className="feature-icon">🚀</div>
            <h2>Ready to Get Started?</h2>
            <p>
              Experience the power of advanced equipment monitoring and analysis.
              Upload your first dataset and see the insights in seconds.
            </p>
            <button 
              className="cta-button"
              onClick={() => navigate('/dashboard')}
            >
              Go to Dashboard →
            </button>
          </div>
        </ScrollStackItem>
      </ScrollStack>
    </div>
  );
};

export default Features;
