# backend_sportradar/views.py

from django.http import HttpResponse

def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /api/",
        "Disallow: /static/",
        "Disallow: /media/",
        "Disallow: /dashboard",
        "Disallow: /profile",
        "Sitemap: https://ias-b3-1-lyon-g1-jjrh.onrender.com/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines).encode('utf-8'), content_type="text/plain")
