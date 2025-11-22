from django.db import models
from django.contrib.auth.models import User
import json


class Dataset(models.Model):
    """Model to store uploaded CSV datasets"""
    upload_date = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)
    summary_json = models.TextField(blank=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ['-upload_date']
    
    def __str__(self):
        return f"{self.file_name} - {self.upload_date.strftime('%Y-%m-%d %H:%M')}"
    
    def get_summary(self):
        """Return summary as dictionary"""
        if self.summary_json:
            return json.loads(self.summary_json)
        return {}
    
    def set_summary(self, summary_dict):
        """Set summary from dictionary"""
        self.summary_json = json.dumps(summary_dict)


class Equipment(models.Model):
    """Model to store individual equipment records"""
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='equipment_items')
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.type})"


class AlertRule(models.Model):
    """Model to store alert rules"""
    PARAMETER_CHOICES = [
        ('flowrate', 'Flowrate'),
        ('pressure', 'Pressure'),
        ('temperature', 'Temperature'),
    ]
    
    CONDITION_CHOICES = [
        ('greater_than', 'Greater Than'),
        ('less_than', 'Less Than'),
        ('equals', 'Equals'),
        ('between', 'Between'),
    ]
    
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    name = models.CharField(max_length=255)
    parameter = models.CharField(max_length=50, choices=PARAMETER_CHOICES)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    threshold = models.FloatField()
    min_value = models.FloatField(null=True, blank=True)
    max_value = models.FloatField(null=True, blank=True)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='medium')
    
    # Notification settings
    send_email = models.BooleanField(default=False)
    email_recipients = models.TextField(blank=True, help_text='Comma-separated email addresses')
    send_telegram = models.BooleanField(default=False)
    telegram_chat_id = models.CharField(max_length=100, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.parameter} {self.condition} {self.threshold}"


class AlertHistory(models.Model):
    """Model to store alert history"""
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='alerts')
    rule = models.ForeignKey(AlertRule, on_delete=models.SET_NULL, null=True, related_name='triggered_alerts')
    parameter = models.CharField(max_length=50)
    value = models.FloatField()
    threshold = models.FloatField()
    message = models.TextField()
    severity = models.CharField(max_length=20)
    
    email_sent = models.BooleanField(default=False)
    telegram_sent = models.BooleanField(default=False)
    acknowledged = models.BooleanField(default=False)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Alert histories'
    
    def __str__(self):
        return f"Alert: {self.equipment.name} - {self.parameter} = {self.value}"
