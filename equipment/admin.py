from django.contrib import admin
from .models import Dataset, Equipment, AlertRule, AlertHistory


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'upload_date', 'uploaded_by', 'equipment_count']
    list_filter = ['upload_date']
    search_fields = ['file_name']
    readonly_fields = ['upload_date']
    
    def equipment_count(self, obj):
        return obj.equipment_items.count()
    equipment_count.short_description = 'Equipment Count'


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'flowrate', 'pressure', 'temperature', 'dataset']
    list_filter = ['type', 'dataset']
    search_fields = ['name', 'type']
    list_per_page = 50



@admin.register(AlertRule)
class AlertRuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'parameter', 'condition', 'threshold', 'severity', 'is_active', 'send_email', 'send_telegram']
    list_filter = ['parameter', 'severity', 'is_active', 'send_email', 'send_telegram']
    search_fields = ['name']
    list_editable = ['is_active']


@admin.register(AlertHistory)
class AlertHistoryAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'parameter', 'value', 'threshold', 'severity', 'acknowledged', 'email_sent', 'telegram_sent', 'created_at']
    list_filter = ['severity', 'acknowledged', 'email_sent', 'telegram_sent', 'created_at']
    search_fields = ['equipment__name', 'message']
    readonly_fields = ['created_at']
    list_per_page = 50
