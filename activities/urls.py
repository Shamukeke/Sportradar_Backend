# activities/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet

router = DefaultRouter()
router.register(r'', ActivityViewSet, basename='activity')

urlpatterns = [
    # toutes les routes REST classiques : list, retrieve, create, etc.
    path('', include(router.urls)),

    # route explicite pour recommendations
    path(
        'recommendations/',
        ActivityViewSet.as_view({'get': 'recommendations'}),
        name='activity-recommendations'
    ),
]
