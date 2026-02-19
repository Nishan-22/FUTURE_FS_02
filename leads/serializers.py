from rest_framework import serializers
from .models import Lead

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['id', 'name', 'email', 'source', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']
