# companies/views.py
from rest_framework import viewsets, permissions
from .models import Company
from .serializers import PlaceSerializer

class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/places/        → liste de tous les lieux publics
    GET /api/places/?badge=sportzen → lieux sport_zen=True
    """
    queryset = Company.objects.filter(is_public=True)
    serializer_class = PlaceSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        badge = self.request.query_params.get('badge')
        if badge == 'sportzen':
            qs = qs.filter(sport_zen=True)
        return qs
