# backend_sportradar/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # endpoints utilisateurs : /api/register/, /api/token/, /api/me/, etc.
    path('api/', include('users.urls')),
    # endpoints activités : /api/activities/, /api/activities/<pk>/, /api/activities/my-activities/, etc.
    path('api/activities/', include('activities.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
