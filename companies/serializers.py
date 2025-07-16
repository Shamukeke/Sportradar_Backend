# companies/serializers.py
from rest_framework import serializers
from .models import Company

class PlaceSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'location', 'image', 'rating']

    def get_image(self, obj):
        # pour renvoyer l’URL complète (notamment utile en React)
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
