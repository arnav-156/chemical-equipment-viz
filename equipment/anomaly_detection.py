"""
Advanced Anomaly Detection System using Machine Learning
Detects equipment parameters that deviate from normal ranges
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from scipy import stats
from datetime import datetime, timedelta


class AnomalyDetector:
    """ML-based anomaly detection for equipment data"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = IsolationForest(
            contamination=0.1,  # Expect 10% anomalies
            random_state=42,
            n_estimators=100
        )
    
    def detect_anomalies(self, equipment_data):
        """
        Detect anomalies in equipment data using multiple methods
        Returns dict with anomaly scores and flags
        """
        if len(equipment_data) < 3:
            # Need at least 3 data points for meaningful detection
            return self._simple_detection(equipment_data)
        
        # Prepare data
        df = pd.DataFrame([{
            'flowrate': item.flowrate,
            'pressure': item.pressure,
            'temperature': item.temperature
        } for item in equipment_data])
        
        # Method 1: Isolation Forest (ML-based)
        isolation_scores = self._isolation_forest_detection(df)
        
        # Method 2: Z-Score (Statistical)
        z_scores = self._zscore_detection(df)
        
        # Method 3: IQR (Interquartile Range)
        iqr_flags = self._iqr_detection(df)
        
        # Combine results
        results = []
        for i, item in enumerate(equipment_data):
            anomaly_info = {
                'equipment_id': item.id,
                'equipment_name': item.name,
                'is_anomaly': isolation_scores[i] == -1 or z_scores[i] or iqr_flags[i],
                'isolation_score': float(isolation_scores[i]),
                'z_score_flag': bool(z_scores[i]),
                'iqr_flag': bool(iqr_flags[i]),
                'health_score': self._calculate_health_score(
                    isolation_scores[i], z_scores[i], iqr_flags[i]
                ),
                'anomaly_details': self._get_anomaly_details(item, df.iloc[i]),
                'severity': self._calculate_severity(
                    isolation_scores[i], z_scores[i], iqr_flags[i]
                )
            }
            results.append(anomaly_info)
        
        return results
    
    def _isolation_forest_detection(self, df):
        """Use Isolation Forest for anomaly detection"""
        try:
            # Normalize data
            X = self.scaler.fit_transform(df)
            
            # Fit and predict
            predictions = self.model.fit_predict(X)
            # Returns: 1 for normal, -1 for anomaly
            
            return predictions
        except Exception as e:
            print(f"Isolation Forest error: {e}")
            return np.ones(len(df))  # All normal if error
    
    def _zscore_detection(self, df):
        """Use Z-score for anomaly detection"""
        try:
            z_scores = np.abs(stats.zscore(df))
            # Flag if any parameter has |z-score| > 3
            anomalies = (z_scores > 3).any(axis=1)
            return anomalies.values
        except Exception as e:
            print(f"Z-score error: {e}")
            return np.zeros(len(df), dtype=bool)
    
    def _iqr_detection(self, df):
        """Use IQR method for anomaly detection"""
        try:
            Q1 = df.quantile(0.25)
            Q3 = df.quantile(0.75)
            IQR = Q3 - Q1
            
            # Define outliers as values outside 1.5*IQR
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Check if any value is outside bounds
            anomalies = ((df < lower_bound) | (df > upper_bound)).any(axis=1)
            return anomalies.values
        except Exception as e:
            print(f"IQR error: {e}")
            return np.zeros(len(df), dtype=bool)
    
    def _simple_detection(self, equipment_data):
        """Simple rule-based detection for small datasets"""
        results = []
        for item in equipment_data:
            # Simple thresholds
            is_anomaly = (
                item.flowrate > 250 or item.flowrate < 50 or
                item.pressure > 40 or item.pressure < 10 or
                item.temperature > 200 or item.temperature < 50
            )
            
            results.append({
                'equipment_id': item.id,
                'equipment_name': item.name,
                'is_anomaly': is_anomaly,
                'isolation_score': -1 if is_anomaly else 1,
                'z_score_flag': is_anomaly,
                'iqr_flag': is_anomaly,
                'health_score': 50 if is_anomaly else 95,
                'anomaly_details': self._get_simple_anomaly_details(item),
                'severity': 'high' if is_anomaly else 'normal'
            })
        
        return results
    
    def _calculate_health_score(self, isolation_score, z_score_flag, iqr_flag):
        """
        Calculate health score (0-100)
        100 = Perfect health, 0 = Critical
        """
        score = 100
        
        # Isolation Forest penalty
        if isolation_score == -1:
            score -= 40
        
        # Z-score penalty
        if z_score_flag:
            score -= 30
        
        # IQR penalty
        if iqr_flag:
            score -= 20
        
        return max(0, min(100, score))
    
    def _calculate_severity(self, isolation_score, z_score_flag, iqr_flag):
        """Calculate severity level"""
        anomaly_count = sum([
            isolation_score == -1,
            z_score_flag,
            iqr_flag
        ])
        
        if anomaly_count >= 3:
            return 'critical'
        elif anomaly_count == 2:
            return 'high'
        elif anomaly_count == 1:
            return 'medium'
        else:
            return 'normal'
    
    def _get_anomaly_details(self, item, row):
        """Get detailed anomaly information"""
        details = []
        
        # Check each parameter
        if row['flowrate'] > 220 or row['flowrate'] < 100:
            details.append({
                'parameter': 'flowrate',
                'value': float(item.flowrate),
                'status': 'abnormal',
                'message': f"Flowrate {item.flowrate:.2f} is outside normal range"
            })
        
        if row['pressure'] > 35 or row['pressure'] < 15:
            details.append({
                'parameter': 'pressure',
                'value': float(item.pressure),
                'status': 'abnormal',
                'message': f"Pressure {item.pressure:.2f} is outside normal range"
            })
        
        if row['temperature'] > 180 or row['temperature'] < 70:
            details.append({
                'parameter': 'temperature',
                'value': float(item.temperature),
                'status': 'abnormal',
                'message': f"Temperature {item.temperature:.2f} is outside normal range"
            })
        
        return details
    
    def _get_simple_anomaly_details(self, item):
        """Get anomaly details for simple detection"""
        details = []
        
        if item.flowrate > 250 or item.flowrate < 50:
            details.append({
                'parameter': 'flowrate',
                'value': float(item.flowrate),
                'status': 'critical',
                'message': f"Flowrate {item.flowrate:.2f} is critically abnormal"
            })
        
        if item.pressure > 40 or item.pressure < 10:
            details.append({
                'parameter': 'pressure',
                'value': float(item.pressure),
                'status': 'critical',
                'message': f"Pressure {item.pressure:.2f} is critically abnormal"
            })
        
        if item.temperature > 200 or item.temperature < 50:
            details.append({
                'parameter': 'temperature',
                'value': float(item.temperature),
                'status': 'critical',
                'message': f"Temperature {item.temperature:.2f} is critically abnormal"
            })
        
        return details
    
    def analyze_trends(self, datasets):
        """
        Analyze trends across multiple datasets
        Returns trend analysis for parameters
        """
        if len(datasets) < 2:
            return None
        
        # Get last 3 datasets
        recent_datasets = datasets[:3]
        
        trends = {
            'flowrate': self._calculate_trend([
                ds.get_summary().get('avg_flowrate', 0) 
                for ds in recent_datasets
            ]),
            'pressure': self._calculate_trend([
                ds.get_summary().get('avg_pressure', 0) 
                for ds in recent_datasets
            ]),
            'temperature': self._calculate_trend([
                ds.get_summary().get('avg_temperature', 0) 
                for ds in recent_datasets
            ])
        }
        
        return trends
    
    def _calculate_trend(self, values):
        """Calculate trend (increasing/decreasing/stable)"""
        if len(values) < 2:
            return {'direction': 'stable', 'change_percent': 0}
        
        # Calculate percentage change from oldest to newest
        oldest = values[-1]
        newest = values[0]
        
        if oldest == 0:
            return {'direction': 'stable', 'change_percent': 0}
        
        change_percent = ((newest - oldest) / oldest) * 100
        
        if abs(change_percent) < 5:
            direction = 'stable'
        elif change_percent > 0:
            direction = 'increasing'
        else:
            direction = 'decreasing'
        
        return {
            'direction': direction,
            'change_percent': round(change_percent, 2),
            'oldest_value': round(oldest, 2),
            'newest_value': round(newest, 2),
            'message': self._get_trend_message(direction, change_percent)
        }
    
    def _get_trend_message(self, direction, change_percent):
        """Generate human-readable trend message"""
        abs_change = abs(change_percent)
        
        if direction == 'stable':
            return f"Stable (±{abs_change:.1f}%)"
        elif direction == 'increasing':
            return f"Increasing {abs_change:.1f}% over last 3 uploads"
        else:
            return f"Decreasing {abs_change:.1f}% over last 3 uploads"


def get_dataset_health_summary(dataset):
    """
    Get overall health summary for a dataset
    """
    detector = AnomalyDetector()
    equipment_items = list(dataset.equipment_items.all())
    
    if not equipment_items:
        return {
            'overall_health': 100,
            'total_equipment': 0,
            'anomalies_detected': 0,
            'critical_count': 0,
            'health_status': 'excellent'
        }
    
    anomalies = detector.detect_anomalies(equipment_items)
    
    # Calculate statistics
    total = len(anomalies)
    anomaly_count = sum(1 for a in anomalies if a['is_anomaly'])
    critical_count = sum(1 for a in anomalies if a['severity'] == 'critical')
    avg_health = sum(a['health_score'] for a in anomalies) / total
    
    # Determine overall status
    if avg_health >= 90:
        status = 'excellent'
    elif avg_health >= 75:
        status = 'good'
    elif avg_health >= 60:
        status = 'fair'
    elif avg_health >= 40:
        status = 'poor'
    else:
        status = 'critical'
    
    return {
        'overall_health': round(avg_health, 2),
        'total_equipment': total,
        'anomalies_detected': anomaly_count,
        'critical_count': critical_count,
        'health_status': status,
        'anomaly_rate': round((anomaly_count / total) * 100, 2) if total > 0 else 0
    }
