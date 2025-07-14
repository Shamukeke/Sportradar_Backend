'''
from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import Plan, Company, Invitation
from .serializers import PlanSerializer, CompanySerializer, InvitationSerializer, AcceptInvitationSerializer
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [permissions.AllowAny]

class CompanySignupView(generics.CreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        company = serializer.save()
        # Optionally create admin
        User = settings.AUTH_USER_MODEL
        # Further implementation: payment hook

class InvitationViewSet(viewsets.ModelViewSet):
    serializer_class = InvitationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Invitation.objects.filter(company=self.request.user.company)

    def perform_create(self, serializer):
        invite = serializer.save(company=self.request.user.company)
        link = f"{settings.FRONTEND_URL}/accept-invite/{invite.token}"
        send_mail(
            subject="Invitation to join your company on SportRadar",
            message=f"Cliquez ici pour rejoindre: {link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[invite.email]
        )

class AcceptInvitationView(generics.CreateAPIView):
    serializer_class = AcceptInvitationSerializer
    permission_classes = [permissions.AllowAny]
    '''