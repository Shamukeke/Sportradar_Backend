import os
from dotenv import load_dotenv
load_dotenv()
from datetime import timedelta
import datetime
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-l&k6fas!-t%2vtp)n@n2o237w&64jca&qah9e=)w#qw82w%8vc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

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

JAZZMIN_SETTINGS = {
    "site_title":           "SportRadar Admin",
   
    "welcome_sign":         "Bienvenue dans SportRadar",
    "site_logo":            "images/logo_sportradar_blanc.png",     # CHEMIN RELATIF À STATIC_URL
    "site_logo_classes":    "img-fluid rounded mx-auto d-block",
    "site_logo_background_color": "#fff",
    "show_sidebar":         True,
    "navigation_expanded":  True,
    "icons": {
      "auth":                           "fas fa-user-shield",
      "activities":                     "fas fa-dumbbell",
      "companies.subscriptionrequest":  "fas fa-file-signature",
      "subscriptions.subscriptionrequest": "fas fa-file-signature",
    },
    "topmenu_links": [
      {"name": "Tableau de bord", "url": "/admin/", "permissions": ["admin.view_logentry"]},
      {"model": "companies.subscriptionrequest", "label": "Abonnements"},
    ],
}

JAZZMIN_SETTINGS["custom_css"] = "css/jazzmin-overrides.css"


AUTH_USER_MODEL = 'users.CustomUser'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend_sportradar.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend_sportradar.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sportradar_db',       # nom de ta base
        'USER': 'Joa_user',            # ton utilisateur PostgreSQL
        'PASSWORD': 'jsk77eeTON',  # ton mot de passe
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/



# 1) URL & répertoire pour vos fichiers “statiques” (CSS, images de template…)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",    # <— votre dossier “static/” à la racine du projet
]
# pour la commande collectstatic (prod)
STATIC_ROOT = BASE_DIR / "staticfiles"

# 2) URL & répertoire pour vos “uploads” (media utilisateurs)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # frontend vite
    "http://127.0.0.1:5173",
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'no-reply@sportradar.com'
