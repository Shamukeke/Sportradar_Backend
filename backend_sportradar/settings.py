from pathlib import Path
import os
from decouple import config, Csv
from django.core.exceptions import ImproperlyConfigured
import dj_database_url
from datetime import timedelta

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

def get_env(var_name, default=None, cast=str):
    """
    Récupère une variable d'environnement avec type casting.
    Args:
        var_name: Nom de la variable
        default: Valeur par défaut si non trouvée
        cast: Type de conversion (str, int, bool, etc.)
    """
    try:
        return config(var_name, default=default, cast=cast)
    except Exception as e:
        if 'required' in str(e).lower():
            raise ImproperlyConfigured(f"La variable {var_name} est requise mais non configurée")
        return default

# SECURITY
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# Applications
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'users',
    'activities',
    'companies',
    'subscriptions',
    'weather',
]

# Jazzmin admin UI customizations
JAZZMIN_SETTINGS = {
    'site_title': 'SportRadar Admin',
    'welcome_sign': 'Bienvenue dans SportRadar',
    'site_logo': 'images/logo_sportradar_blanc.png',
    'site_logo_classes': 'img-fluid rounded mx-auto d-block',
    'site_logo_background_color': '#fff',
    'show_sidebar': True,
    'navigation_expanded': True,
    'icons': {
        'auth': 'fas fa-user-shield',
        'activities': 'fas fa-dumbbell',
        'companies.subscriptionrequest': 'fas fa-file-signature',
        'subscriptions.subscriptionrequest': 'fas fa-file-signature',
    },
    'topmenu_links': [
        {'name': 'Tableau de bord', 'url': '/admin/', 'permissions': ['admin.view_logentry']},
        {'model': 'companies.subscriptionrequest', 'label': 'Abonnements'},
    ],
}

AUTH_USER_MODEL = 'users.CustomUser'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # sert les statics
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend_sportradar.urls'
WSGI_APPLICATION = 'backend_sportradar.wsgi.application'

# Database
DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        ssl_require=True
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Third‑party keys
OPENWEATHER_API_KEY = get_env('OPENWEATHER_API_KEY', default='')

# CORS
CORS_ALLOWED_ORIGINS = get_env('CORS_ALLOWED_ORIGINS', default='', cast=Csv())

# REST Framework / JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = get_env('EMAIL_HOST', default='smtp.sendgrid.net')
EMAIL_PORT = get_env('EMAIL_PORT', default=587, cast=int)
EMAIL_HOST_USER = get_env('EMAIL_HOST_USER', default='apikey')
EMAIL_HOST_PASSWORD = get_env('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = get_env('DEFAULT_FROM_EMAIL', default='no-reply@sportradar.com')