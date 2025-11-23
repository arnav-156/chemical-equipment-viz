import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { datasetAPI, authAPI } from '../services/api';
import { removeAuthToken, getUser } from '../utils/auth';
import PillNav from '../components/PillNav';
import FileUpload from '../components/FileUpload';
import DatasetList from '../components/DatasetList';
import SummaryCards from '../components/SummaryCards';
import Charts from '../components/Charts';
import DataTable from '../components/DataTable';
import CustomizableDashboard from '../components/CustomizableDashboard';
import EquipmentNetworkGraph from '../components/EquipmentNetworkGraph';
import ComparisonMode from '../components/ComparisonMode';
import './Dashboard.css';

const Dashboard = () => {
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [successMessage, setSuccessMessage] = useState('');
  const [viewMode, setViewMode] = useState('standard'); // 'standard' or 'customizable'
  const [showComparison, setShowComparison] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const user = getUser();

  useEffect(() => {
    loadDatasets();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const loadDatasets = async () => {
    try {
      const data = await datasetAPI.list();
      setDatasets(data);
      if (data.length > 0) {
        loadDatasetDetails(data[0].id);
      }
    } catch (error) {
      console.error('Failed to load datasets:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadDatasetDetails = async (id) => {
    try {
      const [datasetData, summaryData] = await Promise.all([
        datasetAPI.get(id),
        datasetAPI.getSummary(id),
      ]);
      setSelectedDataset(datasetData);
      setSummary(summaryData);
    } catch (error) {
      console.error('Failed to load dataset details:', error);
    }
  };

  const handleUploadSuccess = (data) => {
    setSuccessMessage('File uploaded successfully!');
    setTimeout(() => setSuccessMessage(''), 3000);
    loadDatasets();
    loadDatasetDetails(data.id);
  };

  const handleSelectDataset = (id) => {
    loadDatasetDetails(id);
  };

  const handleDownloadReport = async () => {
    if (!selectedDataset) return;

    try {
      await datasetAPI.downloadReport(
        selectedDataset.id,
        `${selectedDataset.file_name}_report.pdf`
      );
      setSuccessMessage('Report downloaded successfully!');
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (error) {
      console.error('Failed to download report:', error);
      alert('Failed to download report. Please try again.');
    }
  };

  const handleLogout = async () => {
    try {
      await authAPI.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      removeAuthToken();
      navigate('/login');
    }
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Waking up the machines...</p>
        </div>
      </div>
    );
  }

  const currentPath = location.pathname;

  const handleViewToggle = (e) => {
    e.preventDefault();
    setViewMode(viewMode === 'standard' ? 'customizable' : 'standard');
  };

  const navItems = [
    { label: 'Dashboard', href: '/dashboard' },
    { label: 'Features', href: '/features' },
    { 
      label: viewMode === 'standard' ? '🎨 Custom' : '📊 Standard', 
      href: '#', 
      onClick: handleViewToggle 
    },
    { label: 'Logout', href: '#', onClick: handleLogout }
  ];

  return (
    <div className="dashboard-container">
      {/* Pill Navigation */}
      <PillNav
        items={navItems}
        activeHref={currentPath}
        baseColor="#00FFA3"
        pillColor="#1E2749"
        hoveredPillTextColor="#0A0E27"
        pillTextColor="#00FFA3"
      />

      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <h1>🧪 Chemical Equipment Visualizer</h1>
          <div className="header-actions">
            <span className="user-info">Welcome, {user?.username}! 👋</span>
          </div>
        </div>
      </header>

      {/* Success Message */}
      {successMessage && (
        <div className="success-message">{successMessage}</div>
      )}

      {/* Main Content */}
      <div className="dashboard-content">
        {/* Upload Section */}
        <FileUpload onUploadSuccess={handleUploadSuccess} />

        {/* Dataset List */}
        <DatasetList
          datasets={datasets}
          onSelectDataset={handleSelectDataset}
          selectedDatasetId={selectedDataset?.id}
        />

        {/* Comparison Mode Button */}
        {datasets.length >= 2 && (
          <div className="comparison-trigger">
            <button 
              className="btn-comparison"
              onClick={() => setShowComparison(true)}
            >
              ⚖️ Compare Datasets
            </button>
            <p className="comparison-hint">Compare multiple datasets side-by-side</p>
          </div>
        )}

        {/* Dataset Details */}
        {selectedDataset && (
          <>
            {viewMode === 'customizable' ? (
              /* Customizable Dashboard View */
              <CustomizableDashboard
                summary={summary}
                equipmentData={selectedDataset.equipment_items}
                onDownloadReport={handleDownloadReport}
              />
            ) : (
              /* Standard View */
              <>
                {/* Download Report Button */}
                <div className="report-section">
                  <button onClick={handleDownloadReport} className="btn-download-report">
                    📄 Download PDF Report
                  </button>
                </div>

                {/* Summary Cards */}
                <SummaryCards summary={summary} />

                {/* Equipment Network Graph */}
                <EquipmentNetworkGraph equipmentData={selectedDataset.equipment_items} />

                {/* Charts */}
                <Charts
                  summary={summary}
                  equipmentData={selectedDataset.equipment_items}
                />

                {/* Data Table */}
                <DataTable equipmentData={selectedDataset.equipment_items} />
              </>
            )}
          </>
        )}

        {!selectedDataset && datasets.length === 0 && (
          <div className="empty-state">
            <h2>👋 Welcome to Chemical Equipment Visualizer!</h2>
            <p>Upload your first CSV file to get started with data analysis and visualization.</p>
          </div>
        )}
      </div>

      {/* Footer */}
      <footer className="dashboard-footer">
        <p>© 2025 Chemical Equipment Visualizer | Built with React & Django</p>
      </footer>

      {/* Comparison Mode Modal */}
      {showComparison && (
        <ComparisonMode 
          datasets={datasets}
          onClose={() => setShowComparison(false)}
        />
      )}
    </div>
  );
};

export default Dashboard;
