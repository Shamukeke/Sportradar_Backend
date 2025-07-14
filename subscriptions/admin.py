from django.contrib import admin
from .models import SubscriptionRequest

@admin.register(SubscriptionRequest)
class SubscriptionRequestAdmin(admin.ModelAdmin):
    list_display = ('company_name','plan','email','created_at')