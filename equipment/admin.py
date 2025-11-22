from django.contrib import admin
from .models import Dataset, Equipment


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
