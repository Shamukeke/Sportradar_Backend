'''
# companies/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanViewSet, CompanySignupView, InvitationViewSet, AcceptInvitationView

router = DefaultRouter()
router.register(r'plans', PlanViewSet, basename='plan')
router.register(r'invitations', InvitationViewSet, basename='invitation')

urlpatterns = [
    # GET  /api/plans/                  → liste des plans
    # GET  /api/plans/{id}/             → détail d’un plan
    # GET  /api/invitations/            → liste des invitations de la company (auth required)
    # POST /api/invitations/            → créer/inviter un collaborateur (auth required)
    # ...
    path('', include(router.urls)),

    # POST /api/companies/signup/       → création de la company + admin (paiement géré dans la view)
    path('companies/signup/', CompanySignupView.as_view(), name='company-signup'),

    # POST /api/accept-invite/          → utilisation du token d’invitation
    path('accept-invite/', AcceptInvitationView.as_view(), name='accept-invite'),
]
'''