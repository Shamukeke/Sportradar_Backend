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
