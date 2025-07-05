# activities/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet

router = DefaultRouter()
router.register(r'', ActivityViewSet,
                basename='activity')  # garde "activities" ici

urlpatterns = [
    path('', include(router.urls)),  # ça donne /activities/
]
