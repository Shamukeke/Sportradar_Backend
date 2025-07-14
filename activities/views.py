from django.db.models import F, Value, FloatField, ExpressionWrapper, Q
from django.db.models.functions import Radians, Sin, Cos, ACos
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models.functions import TruncMonth
from django.db.models import Count
from .models import Activity
from .serializers import ActivitySerializer


class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Activity.objects.filter(is_public=True)
        if self.request.user.is_authenticated and self.request.user.type == 'business':
            qs = Activity.objects.all()
        return qs.order_by('date', 'time')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[permissions.IsAuthenticated],
        url_path='register'
    )
    def register(self, request, pk=None):
        activity = self.get_object()
        user = request.user

        if request.method == 'POST':
            if activity.attendees.filter(pk=user.pk).exists():
                return Response({'detail': 'Vous êtes déjà inscrit·e.'},
                                status=status.HTTP_400_BAD_REQUEST)
            if activity.participants >= activity.max_participants:
                return Response({'detail': 'Complet.'},
                                status=status.HTTP_400_BAD_REQUEST)
            activity.attendees.add(user)

        else:  # DELETE → désinscription
            if not activity.attendees.filter(pk=user.pk).exists():
                return Response({'detail': "Vous n'êtes pas inscrit·e."},
                                status=status.HTTP_400_BAD_REQUEST)
            activity.attendees.remove(user)

        return Response({'participants': activity.participants})

    @action(
        detail=False,
        methods=['get'],
        url_path='my-activities',
        permission_classes=[permissions.IsAuthenticated]
    )
    def my_activities(self, request):
        qs = Activity.objects.filter(
            attendees=request.user).order_by('date', 'time')
        return Response(self.get_serializer(qs, many=True).data)

    @action(
        detail=False,
        methods=['get'],
        url_path='stats',
        permission_classes=[permissions.IsAuthenticated]
    )
    def get_stats(self, request):
        user = request.user
        total = Activity.objects.filter(created_by=user).count()
        monthly_qs = (
            Activity.objects.filter(created_by=user)
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )
        formatted = [
            {"month": m['month'].strftime('%Y-%m'), "count": m['count']}
            for m in monthly_qs
        ]
        top_cat = (
            Activity.objects.filter(created_by=user)
            .values('category')
            .annotate(total=Count('id'))
            .order_by('-total')[:3]
        )
        avg_p = Activity.objects.filter(created_by=user).aggregate(
            avg=Count('attendees')
        )['avg'] or 0

        return Response({
            'total_activities': total,
            'monthly_activity': formatted,
            'top_categories': list(top_cat),
            'average_participants': avg_p,
        })

    @action(detail=False, methods=['get'], url_path='recommendations')
    def recommendations(self, request):
        """
        GET /api/activities/recommendations/?lat=...&lon=...&condition=Clear
        """
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        condition = request.query_params.get('condition')
        if not all([lat, lon, condition]):
            return Response({'error':'lat, lon & condition requis'}, status=status.HTTP_400_BAD_REQUEST)

        # 1) On définit deux listes de catégories, selon si elles sont plutôt indoor ou outdoor
        OUTDOOR_CATS = ['course', 'randonnée', 'vélo', 'course-à-pied']
        INDOOR_CATS  = ['yoga', 'natation', 'fitness', 'boxe', 'musculation']

        # 2) Choix de la logique météo
        # si pluie/neige/orage  => privilégier indoor
        # sinon                => privilégier outdoor
        use_outdoor = condition not in ['Rain','Snow','Thunderstorm'] and float(lat) and float(lon)

        # 3) Filtrer la queryset par catégorie
        qs = self.get_queryset().filter(
            Q(category__in=OUTDOOR_CATS) if use_outdoor else Q(category__in=INDOOR_CATS)
        )

        # 4) Calcul de la distance Haversine (idem venue) pour trier par proximité
        lat_f = float(lat)
        lon_f = float(lon)
        user_lat = Radians(Value(lat_f))
        user_lon = Radians(Value(lon_f))

        qs = qs.annotate(
            act_lat=Radians(F('lat')),
            act_lon=Radians(F('lon'))
        ).annotate(
            distance=ExpressionWrapper(
                6371 * ACos(
                    Cos(user_lat) * Cos(F('act_lat')) * Cos(user_lon - F('act_lon'))
                    + Sin(user_lat) * Sin(F('act_lat'))
                ),
                output_field=FloatField()
            )
        )

        # 5) Ordonner par distance puis rating
        qs = qs.order_by('distance', '-rating')[:12]

        serializer = ActivitySerializer(qs, many=True)
        return Response(serializer.data)