# companies/urls.py
from rest_framework.routers import DefaultRouter
from .views import PlaceViewSet

router = DefaultRouter()
# On enregistre le ViewSet « à la racine » du routeur
router.register(r'', PlaceViewSet, basename='place')

# On exporte uniquement router.urls
urlpatterns = router.urls
