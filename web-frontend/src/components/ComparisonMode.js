import { useState, useEffect } from 'react';
import { datasetAPI } from '../services/api';
import './ComparisonMode.css';

const ComparisonMode = ({ datasets, onClose }) => {
  const [selectedDatasets, setSelectedDatasets] = useState([]);
  const [comparisonData, setComparisonData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [viewMode, setViewMode] = useState('side-by-side'); // 'side-by-side' or 'diff'

  useEffect(() => {
    if (selectedDatasets.length > 0) {
      loadComparisonData();
    }
  }, [selectedDatasets]);

  const loadComparisonData = async () => {
    setLoading(true);
    try {
      const dataPromises = selectedDatasets.map(id => 
        Promise.all([
          datasetAPI.get(id),
          datasetAPI.getSummary(id)
        ])
      );
      const results = await Promise.all(dataPromises);
      setComparisonData(results.map(([dataset, summary]) => ({
        dataset,
        summary
      })));
    } catch (error) {
      console.error('Failed to load comparison data:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleDataset = (id) => {
    if (selectedDatasets.includes(id)) {
      setSelectedDatasets(selectedDatasets.filter(dsId => dsId !== id));
    } else if (selectedDatasets.length < 5) {
      setSelectedDatasets([...selectedDatasets, id]);
    }
  };

  const calculateDiff = (value1, value2) => {
    if (!value1 || !value2) return 0;
    return ((value2 - value1) / value1 * 100).toFixed(1);
  };

  const getDiffColor = (diff) => {
    if (diff > 0) return '#6BCF7F'; // Green for increase
    if (diff < 0) return '#FF4757'; // Red for decrease
    return '#8B95C9'; // Neutral
  };

  return (
    <div className="comparison-mode-overlay">
      <div className="comparison-mode-container">
        <div className="comparison-header">
          <h2>⚖️ Dataset Comparison</h2>
          <button className="close-comparison" onClick={onClose}>✕</button>
        </div>

        <div className="comparison-content">
          {/* Dataset Selection */}
          <div className="dataset-selector">
            <h3>Select Datasets (2-5)</h3>
            <p className="selector-hint">Choose datasets to compare side-by-side</p>
            <div className="dataset-chips">
              {datasets.map(ds => (
                <button
                  key={ds.id}
                  className={`dataset-chip ${selectedDatasets.includes(ds.id) ? 'selected' : ''}`}
                  onClick={() => toggleDataset(ds.id)}
                  disabled={!selectedDatasets.includes(ds.id) && selectedDatasets.length >= 5}
                >
                  <span className="chip-icon">📊</span>
                  <span className="chip-name">{ds.file_name}</span>
                  <span className="chip-date">{new Date(ds.uploaded_at).toLocaleDateString()}</span>
                </button>
              ))}
            </div>
          </div>

          {/* View Mode Toggle */}
          {selectedDatasets.length >= 2 && (
            <div className="view-mode-toggle">
              <button
                className={`mode-btn ${viewMode === 'side-by-side' ? 'active' : ''}`}
                onClick={() => setViewMode('side-by-side')}
              >
                📊 Side-by-Side
              </button>
              <button
                className={`mode-btn ${viewMode === 'diff' ? 'active' : ''}`}
                onClick={() => setViewMode('diff')}
              >
                📈 Diff View
              </button>
            </div>
          )}

          {/* Comparison Display */}
          {loading && (
            <div className="comparison-loading">
              <div className="spinner"></div>
              <p>Loading comparison data...</p>
            </div>
          )}

          {!loading && comparisonData.length >= 2 && viewMode === 'side-by-side' && (
            <div className="side-by-side-view">
              {comparisonData.map((data, index) => (
                <div key={index} className="comparison-column">
                  <div className="column-header">
                    <h4>{data.dataset.file_name}</h4>
                    <span className="column-date">
                      {new Date(data.dataset.uploaded_at).toLocaleDateString()}
                    </span>
                  </div>

                  <div className="column-metrics">
                    <div className="metric-card">
                      <span className="metric-label">Equipment Count</span>
                      <span className="metric-value">{data.dataset.equipment_items.length}</span>
                    </div>

                    <div className="metric-card">
                      <span className="metric-label">Avg Temperature</span>
                      <span className="metric-value">
                        {data.summary.avg_temperature?.toFixed(1)}°C
                      </span>
                    </div>

                    <div className="metric-card">
                      <span className="metric-label">Avg Pressure</span>
                      <span className="metric-value">
                        {data.summary.avg_pressure?.toFixed(1)} bar
                      </span>
                    </div>

                    <div className="metric-card">
                      <span className="metric-label">Avg Flowrate</span>
                      <span className="metric-value">
                        {data.summary.avg_flowrate?.toFixed(1)} m³/h
                      </span>
                    </div>

                    <div className="metric-card">
                      <span className="metric-label">Avg Efficiency</span>
                      <span className="metric-value">
                        {data.summary.avg_efficiency?.toFixed(1)}%
                      </span>
                    </div>

                    <div className="metric-card">
                      <span className="metric-label">Health Score</span>
                      <span className="metric-value health-score">
                        {data.summary.health_score?.toFixed(1)}/100
                      </span>
                    </div>

                    <div className="metric-card">
                      <span className="metric-label">Anomalies</span>
                      <span className="metric-value anomaly-count">
                        {data.summary.anomaly_count || 0}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {!loading && comparisonData.length >= 2 && viewMode === 'diff' && (
            <div className="diff-view">
              <div className="diff-header">
                <h4>📈 Changes from {comparisonData[0].dataset.file_name} to {comparisonData[comparisonData.length - 1].dataset.file_name}</h4>
              </div>

              <div className="diff-metrics">
                {['avg_temperature', 'avg_pressure', 'avg_flowrate', 'avg_efficiency', 'health_score'].map(metric => {
                  const firstValue = comparisonData[0].summary[metric];
                  const lastValue = comparisonData[comparisonData.length - 1].summary[metric];
                  const diff = calculateDiff(firstValue, lastValue);
                  const diffColor = getDiffColor(diff);

                  return (
                    <div key={metric} className="diff-item">
                      <span className="diff-label">
                        {metric.replace('avg_', '').replace('_', ' ').toUpperCase()}
                      </span>
                      <div className="diff-values">
                        <span className="diff-old">{firstValue?.toFixed(1)}</span>
                        <span className="diff-arrow">→</span>
                        <span className="diff-new">{lastValue?.toFixed(1)}</span>
                      </div>
                      <span 
                        className="diff-percentage"
                        style={{ color: diffColor }}
                      >
                        {diff > 0 ? '+' : ''}{diff}%
                      </span>
                    </div>
                  );
                })}
              </div>

              <div className="diff-summary">
                <h5>Summary</h5>
                <div className="summary-grid">
                  <div className="summary-item positive">
                    <span className="summary-icon">📈</span>
                    <span className="summary-text">
                      {comparisonData.filter((d, i) => i > 0 && 
                        d.summary.health_score > comparisonData[i-1].summary.health_score
                      ).length} improvements
                    </span>
                  </div>
                  <div className="summary-item negative">
                    <span className="summary-icon">📉</span>
                    <span className="summary-text">
                      {comparisonData.filter((d, i) => i > 0 && 
                        d.summary.health_score < comparisonData[i-1].summary.health_score
                      ).length} declines
                    </span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {!loading && selectedDatasets.length < 2 && (
            <div className="comparison-empty">
              <span className="empty-icon">⚖️</span>
              <h3>Select at least 2 datasets to compare</h3>
              <p>Choose datasets from the list above to see side-by-side comparison</p>
            </div>
          )}
        </div>

        {comparisonData.length >= 2 && (
          <div className="comparison-footer">
            <button className="btn-export" onClick={() => alert('Export feature coming soon!')}>
              📄 Export Comparison Report
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ComparisonMode;
