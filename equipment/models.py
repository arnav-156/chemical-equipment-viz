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
