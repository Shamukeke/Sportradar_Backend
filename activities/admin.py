from django.contrib import admin
from .models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'location',
                    'date', 'time', 'created_by')
    list_filter = ('category', 'level', 'sport_zen')
    search_fields = ('name', 'description', 'location', 'instructor')
    ordering = ('-created_at',)
    date_hierarchy = 'date'
    autocomplete_fields = ['created_by']
