# companies/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SubscriptionRequest(models.Model):
    PLAN_CHOICES = [
        ('basic', 'Abonnement de base'),
        ('intermediate', 'Abonnement intermédiaire'),
        ('enterprise', 'Abonnement sur mesure'),
    ]

    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    company_name = models.CharField(max_length=255)
    admin_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Demande d’abonnement"               # Singulier
        verbose_name_plural = "Demandes d’abonnement"       # Pluriel

    def __str__(self):
        return f"{self.company_name} – {self.get_plan_display()}"

