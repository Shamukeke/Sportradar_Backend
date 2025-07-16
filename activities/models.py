from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Activity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default='')
    category = models.CharField(max_length=50, default='autre')
    location = models.CharField(max_length=255, default='Lieu non précisé')
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    duration = models.CharField(max_length=50, default='1h')
    max_participants = models.PositiveIntegerField(default=20)
    price = models.CharField(max_length=50, default='Gratuit')
    level = models.CharField(max_length=50, default='Tous niveaux')
    sport_zen = models.BooleanField(default=False)
    rating = models.FloatField(default=0.0)
    instructor = models.CharField(
        max_length=100, blank=True, default='Instructeur inconnu')
    image = models.ImageField(
        upload_to='activity_images/', blank=True, null=True)
    is_public = models.BooleanField(default=True)
    attendees = models.ManyToManyField(
        User, related_name='registered_activities', blank=True
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='activities'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'time']   # tri natif par date puis heure
        verbose_name = "Activité"               # <-- ici, le singulier
        verbose_name_plural = "Activités"       # <-- ici, le pluriel

    @property
    def participants(self) -> int:
        return self.attendees.count()

    VENUE_CHOICES = [
        ('inside', 'Intérieur'),
        ('outside', 'Extérieur'),
    ]
    venue = models.CharField(
        max_length=10,
        choices=VENUE_CHOICES,
         default='inside',
        help_text="Lieu : 'inside' ou 'outside' (nullable temporaire)"
    )

    def __str__(self):
        return self.name
