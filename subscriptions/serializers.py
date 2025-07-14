# companies/serializers.py
from rest_framework import serializers
from .models import SubscriptionRequest

class SubscriptionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionRequest
        fields = [
            'id', 'plan', 'company_name', 'admin_name',
            'email', 'phone', 'message', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
