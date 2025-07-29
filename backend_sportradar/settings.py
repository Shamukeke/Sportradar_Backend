import os
from pathlib import Path
from decouple import config, Csv
from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured
import dj_database_url
from datetime import timedelta

# --- Chemins de base ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Chargement du bon .env selon DJANGO_ENV ---
env = os.getenv('DJANGO_ENV', 'production').lower()
dotenv_path = BASE_DIR / ('.env.development' if env == 'development' else '.env')
load_dotenv(dotenv_path)

# --- Helper pour récupérer les variables d'env ---
def get_env(var_name, default=None, cast=None):
    try:
        if cast is not None:
            return config(var_name, default=default, cast=cast)
        else:
            return config(var_name, default=default)
    except Exception as e:
        if 'required' in str(e).lower():
            raise ImproperlyConfigured(f"La variable {var_name} est requise mais non configurée")
        return default

# --- Sécurité générale ---
SECRET_KEY = get_env('SECRET_KEY')
DEBUG = get_env('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = get_env('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())


# HSTS & redirections HTTPS
SECURE_SSL_REDIRECT = get_env('SECURE_SSL_REDIRECT', default=True, cast=bool)
SECURE_HSTS_SECONDS = get_env('SECURE_HSTS_SECONDS', default=31536000, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = get_env('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True, cast=bool)
SECURE_HSTS_PRELOAD = get_env('SECURE_HSTS_PRELOAD', default=True, cast=bool)

# Cookies sécurisées
SESSION_COOKIE_SECURE = get_env('SESSION_COOKIE_SECURE', default=True, cast=bool)
CSRF_COOKIE_SECURE = get_env('CSRF_COOKIE_SECURE', default=True, cast=bool)

# Proxy pour HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# --- Applications installées ---
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

# Jazzmin config (inchangée)
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
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend_sportradar.urls'
WSGI_APPLICATION = 'backend_sportradar.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


CORS_ALLOWED_ORIGINS = get_env(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:5173,https://ias-b3-1-lyon-g1-jjrh.onrender.com',
    cast=Csv()
)
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = get_env(
    'CSRF_TRUSTED_ORIGINS',
    default='https://ias-b3-1-lyon-g1.onrender.com,https://ias-b3-1-lyon-g1-jjrh.onrender.com',
    cast=Csv()
)


# --- Base de données (Postgres/Render compatible + DEV sans dj_database_url) ---
# Dans settings.py
# settings.py

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': get_env('DB_NAME', 'sportradar_db'),
            'USER': get_env('DB_USER', 'postgres'),  # Utilisateur par défaut
            'PASSWORD': get_env('DB_PASSWORD', ''),
            'HOST': get_env('DB_HOST', 'localhost'),
            'PORT': get_env('DB_PORT', '5432'),  # Port explicite
            'OPTIONS': {'sslmode': 'disable'},
        }
    }
else:
    # Configuration pour la production (avec dj_database_url)
    DATABASES = {
        'default': dj_database_url.config(
            default=get_env('DATABASE_URL'),
            conn_max_age=get_env('DB_CONN_MAX_AGE', default=600, cast=int),
            ssl_require=True,
            engine='django.db.backends.postgresql',
    )
}
# --- Validation de mots de passe ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internationalisation ---
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

# --- Statiques & médias ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- Clé API tierces ---
OPENWEATHER_API_KEY = get_env('OPENWEATHER_API_KEY', default='')

# --- CORS (format CSV attendu par decouple) ---
# --- CORS ---


# --- Django REST & JWT ---
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

# --- Email SMTP ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = get_env('EMAIL_HOST', default='smtp.sendgrid.net')
EMAIL_PORT = get_env('EMAIL_PORT', default=587, cast=int)
EMAIL_HOST_USER = get_env('EMAIL_HOST_USER', default='apikey')
EMAIL_HOST_PASSWORD = get_env('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = get_env('EMAIL_USE_TLS', default=True, cast=bool)
DEFAULT_FROM_EMAIL = get_env('DEFAULT_FROM_EMAIL', default='no-reply@sportradar.com')

# --- MEDIA on S3 ---
INSTALLED_APPS += ['storages']
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = get_env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = get_env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = get_env('AWS_S3_REGION_NAME')

AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = False
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
