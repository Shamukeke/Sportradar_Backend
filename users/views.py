# users/views.py
from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny, IsAdminUser
from .serializers import RegisterSerializer, UserSerializer, BusinessRegisterSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from activities.models import Activity
from django.db.models import Avg

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]    # ← indispensable


class BusinessRegisterView(generics.CreateAPIView):
    """
    Seuls les super-admins ou staff peuvent créer de vrais comptes business.
    """
    queryset = User.objects.all()
    serializer_class = BusinessRegisterSerializer
    permission_classes = [IsAdminUser]


class UserListView(generics.ListAPIView):
    """
    Retourne la liste de tous les users (ici on pourra filtrer côté front
    ou bien côté back pour ne renvoyer que les business).
    Accessible uniquement aux admins.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        request.user.preferences = request.data.get("preferences", {})
        request.user.save()
        return Response({"detail": "updated"})


@api_view(['GET'])
def user_stats(request):
    # restreint aux authentifiés grâce aux permissions globales
    activities = Activity.objects.filter(created_by=request.user)
    total = activities.count()
    last = activities.order_by('-created_at').first()
    avg_rating = activities.aggregate(avg=Avg('rating'))['avg'] or 0
    return Response({
        'total_activities': total,
        'average_rating': round(avg_rating, 2),
        'last_activity': last.name if last else None,
        'last_date': last.created_at if last else None
    })
