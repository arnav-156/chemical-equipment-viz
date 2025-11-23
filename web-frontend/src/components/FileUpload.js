import React, { useState, useRef } from 'react';
import { datasetAPI } from '../services/api';
import ParticleExplosion from './ParticleExplosion';
import './FileUpload.css';

const FileUpload = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState('');
  const [dragActive, setDragActive] = useState(false);
  const [showExplosion, setShowExplosion] = useState(false);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileChange(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (selectedFile) => {
    setError('');

    if (!selectedFile.name.endsWith('.csv')) {
      setError('Hmm, that doesn\'t look like a CSV file. Try again? 🤔');
      return;
    }

    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) {
      setError('No file selected! Pick one first 📁');
      return;
    }

    setUploading(true);
    setError('');
    setUploadProgress(0);

    try {
      const data = await datasetAPI.upload(file, (progressEvent) => {
        const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        setUploadProgress(progress);
      });

      // Trigger particle explosion!
      setShowExplosion(true);
      
      setTimeout(() => {
        setFile(null);
        setUploadProgress(0);
        if (fileInputRef.current) {
          fileInputRef.current.value = '';
        }

        if (onUploadSuccess) {
          onUploadSuccess(data);
        }
      }, 500);
    } catch (err) {
      setError(err.response?.data?.error || 'Oops! Something went wrong. Give it another shot? 💪');
    } finally {
      setUploading(false);
    }
  };

  return (
    <>
      <ParticleExplosion 
        trigger={showExplosion}
        onComplete={() => setShowExplosion(false)}
      />
      <div className="file-upload-container">
        <h2>📊 Upload Equipment Data</h2>

      <div
        className={`drop-zone ${dragActive ? 'drag-active' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv"
          onChange={(e) => handleFileChange(e.target.files[0])}
          style={{ display: 'none' }}
        />

        <div className="drop-zone-content">
          <span className="upload-icon">📁</span>
          <p>Drag and drop your CSV here</p>
          <p className="or-text">or</p>
          <button type="button" className="btn-select">
            Browse Files
          </button>
          <p className="hint-text">Feed me some data! 🤖</p>
        </div>
      </div>

      {file && (
        <div className="file-info">
          <p>
            <strong>Selected file:</strong> {file.name} ({(file.size / 1024).toFixed(2)} KB)
          </p>
        </div>
      )}

      {error && <div className="error-message">{error}</div>}

      {uploading && (
        <div className="progress-container">
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${uploadProgress}%` }}></div>
          </div>
          <p>{uploadProgress}% uploaded</p>
        </div>
      )}

      <button
        className="btn-upload"
        onClick={handleUpload}
        disabled={!file || uploading}
      >
        {uploading ? 'Crunching numbers...' : '🚀 Upload and Analyze'}
      </button>

      <div className="csv-format-info">
        <p><strong>Required CSV format:</strong></p>
        <p>Equipment Name, Type, Flowrate, Pressure, Temperature</p>
      </div>
    </div>
    </>
  );
};

export default FileUpload;
