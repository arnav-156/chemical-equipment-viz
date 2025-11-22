import React, { useState, useEffect } from 'react';
import { Responsive, WidthProvider } from 'react-grid-layout';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';
import './CustomizableDashboard.css';

const ResponsiveGridLayout = WidthProvider(Responsive);

const CustomizableDashboard = ({ summary, equipmentData, onDownloadReport }) => {
  const [layouts, setLayouts] = useState(getFromLS('layouts') || getDefaultLayouts());
  const [widgets, setWidgets] = useState(getFromLS('widgets') || getDefaultWidgets());
  const [editMode, setEditMode] = useState(false);

  useEffect(() => {
    saveToLS('layouts', layouts);
    saveToLS('widgets', widgets);
  }, [layouts, widgets]);

  const onLayoutChange = (layout, allLayouts) => {
    setLayouts(allLayouts);
  };

  const toggleWidget = (widgetId) => {
    setWidgets(prev => ({
      ...prev,
      [widgetId]: { ...prev[widgetId], visible: !prev[widgetId].visible }
    }));
  };

  const resetLayout = () => {
    if (window.confirm('Reset dashboard to default layout?')) {
      setLayouts(getDefaultLayouts());
      setWidgets(getDefaultWidgets());
    }
  };

  const renderWidget = (widgetId) => {
    const widget = widgets[widgetId];
    if (!widget || !widget.visible) return null;

    switch (widgetId) {
      case 'totalCount':
        return renderStatCard('Total Equipment', summary?.total_count || 0, '📦', '#667eea');
      
      case 'avgFlowrate':
        return renderStatCard(
          'Avg Flowrate',
          summary?.avg_flowrate?.toFixed(2) || '0.00',
          '💧',
          '#4caf50',
          `${summary?.min_flowrate?.toFixed(1)} - ${summary?.max_flowrate?.toFixed(1)}`
        );
      
      case 'avgPressure':
        return renderStatCard(
          'Avg Pressure',
          summary?.avg_pressure?.toFixed(2) || '0.00',
          '⚡',
          '#ff9800',
          `${summary?.min_pressure?.toFixed(1)} - ${summary?.max_pressure?.toFixed(1)}`
        );
      
      case 'avgTemperature':
        return renderStatCard(
          'Avg Temperature',
          summary?.avg_temperature?.toFixed(2) || '0.00',
          '🌡️',
          '#f44336',
          `${summary?.min_temperature?.toFixed(1)} - ${summary?.max_temperature?.toFixed(1)}`
        );
      
      case 'typeDistribution':
        return renderTypeDistribution();
      
      case 'quickActions':
        return renderQuickActions();
      
      case 'recentActivity':
        return renderRecentActivity();
      
      case 'dataQuality':
        return renderDataQuality();
      
      default:
        return null;
    }
  };

  const renderStatCard = (title, value, icon, color, range) => (
    <div className="widget-content stat-card" style={{ borderTopColor: color }}>
      <div className="stat-icon" style={{ color }}>{icon}</div>
      <div className="stat-info">
        <h4>{title}</h4>
        <div className="stat-value">{value}</div>
        {range && <div className="stat-range">Range: {range}</div>}
      </div>
    </div>
  );

  const renderTypeDistribution = () => {
    const typeDist = summary?.type_distribution || {};
    const total = Object.values(typeDist).reduce((a, b) => a + b, 0);

    return (
      <div className="widget-content">
        <h4>Equipment Type Distribution</h4>
        <div className="type-list">
          {Object.entries(typeDist).map(([type, count]) => (
            <div key={type} className="type-item">
              <div className="type-info">
                <span className="type-name">{type}</span>
                <span className="type-count">{count} items</span>
              </div>
              <div className="type-bar">
                <div
                  className="type-bar-fill"
                  style={{ width: `${(count / total) * 100}%` }}
                ></div>
              </div>
              <span className="type-percent">{((count / total) * 100).toFixed(1)}%</span>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderQuickActions = () => (
    <div className="widget-content quick-actions">
      <h4>Quick Actions</h4>
      <div className="action-buttons">
        <button className="action-btn" onClick={onDownloadReport}>
          <span className="action-icon">📄</span>
          <span>Download Report</span>
        </button>
        <button className="action-btn" onClick={() => window.location.reload()}>
          <span className="action-icon">🔄</span>
          <span>Refresh Data</span>
        </button>
        <button className="action-btn" onClick={() => setEditMode(!editMode)}>
          <span className="action-icon">⚙️</span>
          <span>Customize</span>
        </button>
      </div>
    </div>
  );

  const renderRecentActivity = () => (
    <div className="widget-content">
      <h4>Recent Activity</h4>
      <div className="activity-list">
        <div className="activity-item">
          <span className="activity-icon">✅</span>
          <div className="activity-info">
            <div className="activity-title">Dataset uploaded</div>
            <div className="activity-time">Just now</div>
          </div>
        </div>
        <div className="activity-item">
          <span className="activity-icon">📊</span>
          <div className="activity-info">
            <div className="activity-title">Analytics generated</div>
            <div className="activity-time">1 minute ago</div>
          </div>
        </div>
        <div className="activity-item">
          <span className="activity-icon">📄</span>
          <div className="activity-info">
            <div className="activity-title">Report downloaded</div>
            <div className="activity-time">5 minutes ago</div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderDataQuality = () => {
    const quality = calculateDataQuality();
    return (
      <div className="widget-content">
        <h4>Data Quality Score</h4>
        <div className="quality-score">
          <div className="quality-circle" style={{ background: getQualityColor(quality) }}>
            <span className="quality-value">{quality}%</span>
          </div>
          <div className="quality-details">
            <div className="quality-item">
              <span className="quality-label">Completeness</span>
              <span className="quality-bar">
                <span style={{ width: '100%' }}></span>
              </span>
            </div>
            <div className="quality-item">
              <span className="quality-label">Consistency</span>
              <span className="quality-bar">
                <span style={{ width: '95%' }}></span>
              </span>
            </div>
            <div className="quality-item">
              <span className="quality-label">Accuracy</span>
              <span className="quality-bar">
                <span style={{ width: '98%' }}></span>
              </span>
            </div>
          </div>
        </div>
      </div>
    );
  };

  const calculateDataQuality = () => {
    if (!equipmentData || equipmentData.length === 0) return 0;
    // Simple quality calculation based on data completeness
    return 97; // Mock value
  };

  const getQualityColor = (quality) => {
    if (quality >= 90) return 'linear-gradient(135deg, #4caf50 0%, #45a049 100%)';
    if (quality >= 70) return 'linear-gradient(135deg, #ff9800 0%, #f57c00 100%)';
    return 'linear-gradient(135deg, #f44336 0%, #d32f2f 100%)';
  };

  return (
    <div className="customizable-dashboard">
      {/* Toolbar */}
      <div className="dashboard-toolbar">
        <div className="toolbar-left">
          <h3>📊 My Dashboard</h3>
          {editMode && <span className="edit-badge">Edit Mode</span>}
        </div>
        <div className="toolbar-right">
          <button
            className={`toolbar-btn ${editMode ? 'active' : ''}`}
            onClick={() => setEditMode(!editMode)}
          >
            {editMode ? '✓ Done' : '⚙️ Customize'}
          </button>
          {editMode && (
            <button className="toolbar-btn" onClick={resetLayout}>
              🔄 Reset
            </button>
          )}
        </div>
      </div>

      {/* Widget Selector (shown in edit mode) */}
      {editMode && (
        <div className="widget-selector">
          <h4>Available Widgets</h4>
          <div className="widget-toggles">
            {Object.entries(widgets).map(([id, widget]) => (
              <label key={id} className="widget-toggle">
                <input
                  type="checkbox"
                  checked={widget.visible}
                  onChange={() => toggleWidget(id)}
                />
                <span>{widget.title}</span>
              </label>
            ))}
          </div>
        </div>
      )}

      {/* Grid Layout */}
      <ResponsiveGridLayout
        className="dashboard-grid"
        layouts={layouts}
        breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
        cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
        rowHeight={100}
        isDraggable={editMode}
        isResizable={editMode}
        onLayoutChange={onLayoutChange}
        draggableHandle=".widget-header"
      >
        {Object.entries(widgets).map(([id, widget]) =>
          widget.visible ? (
            <div key={id} className="dashboard-widget">
              <div className="widget-header">
                <span className="widget-title">{widget.title}</span>
                {editMode && <span className="drag-handle">⋮⋮</span>}
              </div>
              {renderWidget(id)}
            </div>
          ) : null
        )}
      </ResponsiveGridLayout>
    </div>
  );
};

// Helper functions
function getDefaultLayouts() {
  return {
    lg: [
      { i: 'totalCount', x: 0, y: 0, w: 3, h: 1.5 },
      { i: 'avgFlowrate', x: 3, y: 0, w: 3, h: 1.5 },
      { i: 'avgPressure', x: 6, y: 0, w: 3, h: 1.5 },
      { i: 'avgTemperature', x: 9, y: 0, w: 3, h: 1.5 },
      { i: 'typeDistribution', x: 0, y: 1.5, w: 6, h: 3 },
      { i: 'quickActions', x: 6, y: 1.5, w: 3, h: 3 },
      { i: 'dataQuality', x: 9, y: 1.5, w: 3, h: 3 },
      { i: 'recentActivity', x: 0, y: 4.5, w: 6, h: 2.5 },
    ],
  };
}

function getDefaultWidgets() {
  return {
    totalCount: { title: 'Total Equipment', visible: true },
    avgFlowrate: { title: 'Average Flowrate', visible: true },
    avgPressure: { title: 'Average Pressure', visible: true },
    avgTemperature: { title: 'Average Temperature', visible: true },
    typeDistribution: { title: 'Type Distribution', visible: true },
    quickActions: { title: 'Quick Actions', visible: true },
    dataQuality: { title: 'Data Quality', visible: true },
    recentActivity: { title: 'Recent Activity', visible: true },
  };
}

function getFromLS(key) {
  let ls = {};
  if (global.localStorage) {
    try {
      ls = JSON.parse(global.localStorage.getItem('dashboard-config')) || {};
    } catch (e) {
      /* Ignore */
    }
  }
  return ls[key];
}

function saveToLS(key, value) {
  if (global.localStorage) {
    const config = JSON.parse(global.localStorage.getItem('dashboard-config') || '{}');
    config[key] = value;
    global.localStorage.setItem('dashboard-config', JSON.stringify(config));
  }
}

export default CustomizableDashboard;
