# companies/views.py
from rest_framework import viewsets, permissions
from .models import SubscriptionRequest
from .serializers import SubscriptionRequestSerializer

class SubscriptionRequestViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionRequest.objects.all()
    serializer_class = SubscriptionRequestSerializer
    permission_classes = [permissions.AllowAny]  # ou IsAuthenticated si vous souhaitez restreindre
