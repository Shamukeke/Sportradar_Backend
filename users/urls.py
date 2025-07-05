from django.urls import path
from .views import RegisterView, MeView, user_stats, BusinessRegisterView, UserListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # inscription publique = personal uniquement
    path('register/', RegisterView.as_view(), name='register'),

    # endpoint spécial pour créer un business — uniquement accessible aux admins
    path('register-business/',
         BusinessRegisterView.as_view(),
         name='register-business'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeView.as_view(), name='me'),
    path('me/stats/', user_stats, name='user-stats'),
    path('users/', UserListView.as_view(), name='user-list'),
]
