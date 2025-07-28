# activities/serializers.py

from rest_framework import serializers
from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    participants = serializers.IntegerField(read_only=True)
    is_waiting = serializers.SerializerMethodField()
    image = serializers.ImageField(use_url=True) 

    class Meta:
        model = Activity
        fields = [
            'id', 'name', 'description', 'category', 'location', 'date', 'time', 'duration',
            'participants', 'max_participants', 'price', 'level', 'sport_zen', 'rating',
            'instructor', 'image', 'is_public', 'created_by', 'created_at', 'is_waiting'
        ]
        read_only_fields = ['created_by', 'created_at', 'participants']

    def get_is_waiting(self, obj):
        user = self.context['request'].user
        # en attente si plein ET que l'user y est inscrit
        return (
            user.is_authenticated
            and obj.participants >= obj.max_participants
            and obj.attendees.filter(pk=user.pk).exists()
        )
