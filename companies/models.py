# companies/models.py
from django.db import models

class Company(models.Model):
    name       = models.CharField(max_length=200)
    location   = models.CharField(max_length=255)
    image      = models.ImageField(upload_to='company_images/', blank=True, null=True)
    rating     = models.FloatField(default=0.0)  # type: ignore
    sport_zen  = models.BooleanField(default=False)  # true si labellisé # type: ignore
    is_public  = models.BooleanField(default=True)   # public ou non # type: ignore

    def __str__(self):
        return self.name
