# backend_sportradar/urls.py

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap
from activities.models import Activity
from activities.views import ActivityViewSet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models import QuerySet
from weather.views import weather_api
from backend_sportradar.views import robots_txt


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return [
            '/', '/dashboard', '/faq', '/privacy', '/legal',
            '/recommendations', '/badges', '/corporate-offers', '/profile'
        ]

    def location(self, item):
        return item

class ActivitySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Activity.objects.all() or [Activity(id=1)]  # type: ignore

    def location(self, obj):
        return f"/activities/{obj.id}/"

sitemaps = {
    'static': StaticViewSitemap(),
    'activities': ActivitySitemap(),
}

urlpatterns = [
    path('admin/', admin.site.urls),

      # API météo
    path('api/weather/', weather_api, name='api-weather'),
    # Route explicite pour les recommandations
    path(
        'api/activities/recommendations/',
        ActivityViewSet.as_view({'get': 'recommendations'}),
        name='activity-recommendations'
    ),
    # endpoints utilisateurs : /api/register/, /api/token/, /api/me/, etc.
    path('api/', include('users.urls')),
    # endpoints activités : /api/activities/, /api/activities/<pk>/, /api/activities/my-activities/, etc.
    path('api/activities/', include('activities.urls')),
    path('api/companies/', include('companies.urls')),
    path('api/subscriptions/',include('subscriptions.urls')),
    path('api/places/', include('companies.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', robots_txt),
    
    
]

    # Sert vos fichiers STATICFILES_DIRS
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

