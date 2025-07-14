from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionRequestViewSet

router = DefaultRouter()
router.register(r'', SubscriptionRequestViewSet, basename='subscription')

urlpatterns = [
    path('', include(router.urls)),
   
]