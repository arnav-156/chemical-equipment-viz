from rest_framework import serializers
from .models import Dataset, Equipment
from django.contrib.auth.models import User


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'name', 'type', 'flowrate', 'pressure', 'temperature']


class DatasetSerializer(serializers.ModelSerializer):
    equipment_items = EquipmentSerializer(many=True, read_only=True)
    summary = serializers.SerializerMethodField()
    
    class Meta:
        model = Dataset
        fields = ['id', 'upload_date', 'file_name', 'summary', 'equipment_items']
    
    def get_summary(self, obj):
        return obj.get_summary()


class DatasetListSerializer(serializers.ModelSerializer):
    equipment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Dataset
        fields = ['id', 'upload_date', 'file_name', 'equipment_count']
    
    def get_equipment_count(self, obj):
        return obj.equipment_items.count()
