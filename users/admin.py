from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'type',
                    'is_active', 'is_staff', 'is_superuser')
    list_filter = ('type', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Informations personnelles'), {
         'fields': ('username', 'type', 'preferences')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        (_('Dates importantes'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'type', 'password1', 'password2'),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions')
    readonly_fields = ('last_login', 'date_joined')
