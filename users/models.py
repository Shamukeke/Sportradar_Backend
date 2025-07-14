from tabnanny import verbose
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('personal', 'Personal'),
        ('business', 'Business'),
    )

    email = models.EmailField(unique=True)
    type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    # Pour activities, location, level
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    preferences = models.JSONField(default=dict, blank=True)

    USERNAME_FIELD = 'email'
    # username reste requis sauf si on override plus
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return self.email
