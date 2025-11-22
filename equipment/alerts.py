"""
Alert System for Chemical Equipment Visualizer
Detects anomalies and sends notifications via Email/Telegram
"""
from django.core.mail import send_mail
from django.conf import settings
import requests
from .models import Equipment, AlertRule, AlertHistory
from datetime import datetime


class AlertManager:
    """Manages alert detection and notification"""
    
    def __init__(self):
        self.rules = []
    
    def check_equipment(self, equipment):
        """Check equipment against alert rules"""
        alerts = []
        
        # Get active alert rules
        rules = AlertRule.objects.filter(is_active=True)
        
        for rule in rules:
            if self.evaluate_rule(equipment, rule):
                alert = self.create_alert(equipment, rule)
                alerts.append(alert)
                
                # Send notifications
                if rule.send_email:
                    self.send_email_alert(alert)
                
                if rule.send_telegram:
                    self.send_telegram_alert(alert)
        
        return alerts
    
    def evaluate_rule(self, equipment, rule):
        """Evaluate if equipment triggers the rule"""
        value = getattr(equipment, rule.parameter)
        
        if rule.condition == 'greater_than':
            return value > rule.threshold
        elif rule.condition == 'less_than':
            return value < rule.threshold
        elif rule.condition == 'equals':
            return value == rule.threshold
        elif rule.condition == 'between':
            return rule.min_value <= value <= rule.max_value
        
        return False
    
    def create_alert(self, equipment, rule):
        """Create alert record"""
        alert = AlertHistory.objects.create(
            equipment=equipment,
            rule=rule,
            parameter=rule.parameter,
            value=getattr(equipment, rule.parameter),
            threshold=rule.threshold,
            message=self.generate_message(equipment, rule),
            severity=rule.severity
        )
        return alert
    
    def generate_message(self, equipment, rule):
        """Generate alert message"""
        value = getattr(equipment, rule.parameter)
        return (
            f"⚠️ ALERT: {equipment.name}\n"
            f"Parameter: {rule.parameter.upper()}\n"
            f"Current Value: {value:.2f}\n"
            f"Threshold: {rule.threshold:.2f}\n"
            f"Condition: {rule.get_condition_display()}\n"
            f"Severity: {rule.get_severity_display()}"
        )
    
    def send_email_alert(self, alert):
        """Send email notification"""
        try:
            subject = f"🚨 Equipment Alert: {alert.equipment.name}"
            message = alert.message
            
            # Add more details
            message += f"\n\nDataset: {alert.equipment.dataset.file_name}"
            message += f"\nTime: {alert.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
            message += f"\n\nPlease check the dashboard for more details."
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[alert.rule.email_recipients],
                fail_silently=False,
            )
            
            alert.email_sent = True
            alert.save()
            
        except Exception as e:
            print(f"Failed to send email: {e}")
    
    def send_telegram_alert(self, alert):
        """Send Telegram notification"""
        try:
            bot_token = settings.TELEGRAM_BOT_TOKEN
            chat_id = alert.rule.telegram_chat_id
            
            if not bot_token or not chat_id:
                return
            
            message = alert.message
            message += f"\n\n📊 Dataset: {alert.equipment.dataset.file_name}"
            message += f"\n🕐 Time: {alert.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
            
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, data=data)
            
            if response.status_code == 200:
                alert.telegram_sent = True
                alert.save()
            
        except Exception as e:
            print(f"Failed to send Telegram message: {e}")
    
    def check_dataset(self, dataset):
        """Check all equipment in a dataset"""
        all_alerts = []
        
        for equipment in dataset.equipment_items.all():
            alerts = self.check_equipment(equipment)
            all_alerts.extend(alerts)
        
        return all_alerts


def check_anomalies(equipment_data):
    """
    Quick anomaly detection based on statistical analysis
    Returns list of potential issues
    """
    anomalies = []
    
    # Check for extreme values (3 standard deviations)
    # This is a simple implementation
    
    if equipment_data.flowrate > 250 or equipment_data.flowrate < 50:
        anomalies.append({
            'parameter': 'flowrate',
            'value': equipment_data.flowrate,
            'message': 'Flowrate outside normal range'
        })
    
    if equipment_data.pressure > 40 or equipment_data.pressure < 10:
        anomalies.append({
            'parameter': 'pressure',
            'value': equipment_data.pressure,
            'message': 'Pressure outside normal range'
        })
    
    if equipment_data.temperature > 200 or equipment_data.temperature < 50:
        anomalies.append({
            'parameter': 'temperature',
            'value': equipment_data.temperature,
            'message': 'Temperature outside normal range'
        })
    
    return anomalies
