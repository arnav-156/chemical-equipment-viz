import { useState, useEffect } from 'react';
import './OnlineStatus.css';

const OnlineStatus = () => {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [showStatus, setShowStatus] = useState(false);
  const [syncStatus, setSyncStatus] = useState(null);

  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true);
      setShowStatus(true);
      setSyncStatus('Reconnected! Syncing data...');
      setTimeout(() => setShowStatus(false), 3000);
    };

    const handleOffline = () => {
      setIsOnline(false);
      setShowStatus(true);
      setSyncStatus('Offline mode - Data will sync when reconnected');
    };

    const handleServiceWorkerMessage = (event) => {
      const { data } = event;
      
      if (data.type === 'ONLINE_STATUS') {
        setIsOnline(data.isOnline);
        if (!data.isOnline) {
          setShowStatus(true);
          setSyncStatus('Working offline - Changes saved locally');
        }
      }
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.addEventListener('message', handleServiceWorkerMessage);
    }

    if (!navigator.onLine) {
      setShowStatus(true);
      setSyncStatus('Offline mode - Data will sync when reconnected');
    }

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
      if ('serviceWorker' in navigator) {
        navigator.serviceWorker.removeEventListener('message', handleServiceWorkerMessage);
      }
    };
  }, []);

  if (!showStatus && isOnline) return null;

  return (
    <div className={`online-status ${isOnline ? 'online' : 'offline'}`}>
      <div className="status-content">
        <span className="status-icon">
          {isOnline ? '🌐' : '📵'}
        </span>
        <div className="status-text">
          <span className="status-title">
            {isOnline ? 'Online' : 'Offline Mode'}
          </span>
          {syncStatus && (
            <span className="status-message">{syncStatus}</span>
          )}
        </div>
        {showStatus && (
          <button 
            className="status-close"
            onClick={() => setShowStatus(false)}
          >
            ✕
          </button>
        )}
      </div>
      
      {!isOnline && (
        <div className="offline-features">
          <h4>Available Offline:</h4>
          <ul>
            <li>✅ View cached data</li>
            <li>✅ Create new entries</li>
            <li>✅ Generate reports</li>
            <li>✅ Use all visualizations</li>
          </ul>
          <p className="sync-note">
            💾 Changes saved locally and will sync when online
          </p>
        </div>
      )}
    </div>
  );
};

export default OnlineStatus;
