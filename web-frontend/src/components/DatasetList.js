import React from 'react';
import './DatasetList.css';

const DatasetList = ({ datasets, onSelectDataset, selectedDatasetId }) => {
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  if (!datasets || datasets.length === 0) {
    return (
      <div className="dataset-list-container">
        <h2>📊 Recent Datasets</h2>
        <p className="no-data">No datasets uploaded yet. Upload a CSV file to get started!</p>
      </div>
    );
  }

  return (
    <div className="dataset-list-container">
      <h2>📊 Recent Datasets (Last 5)</h2>

      <div className="dataset-list">
        {datasets.map((dataset) => (
          <div
            key={dataset.id}
            className={`dataset-item ${selectedDatasetId === dataset.id ? 'selected' : ''}`}
            onClick={() => onSelectDataset(dataset.id)}
          >
            <div className="dataset-icon">📄</div>
            <div className="dataset-info">
              <h3>{dataset.file_name}</h3>
              <p className="dataset-date">{formatDate(dataset.upload_date)}</p>
              <p className="dataset-count">
                <strong>{dataset.equipment_count}</strong> equipment items
              </p>
            </div>
            <div className="dataset-arrow">→</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DatasetList;
