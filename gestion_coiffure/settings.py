from pathlib import Path
import os
from dotenv import load_dotenv

# =========================
# Paths
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / '.env')

# =========================
# Secrets & Debug
# =========================
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-your-secret-key-here-change-in-production')

DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

# =========================
# Hosts & CSRF
# =========================
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Ajout automatique de l'hôte Render en production
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)



# =========================
# Installed apps
# =========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'frontend',
    'accounts',
    'clients',
    'services',
    'paiements',
    'file_attente',
    'dashbord',
    'salon',
    'depenses',
]

# =========================
# Middleware
# =========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTH_USER_MODEL = 'accounts.User'
ROOT_URLCONF = 'gestion_coiffure.urls'

# =========================
# Templates
# =========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'gestion_coiffure.wsgi.application'

# =========================
# Database
# =========================
import dj_database_url

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# =========================
# Django REST Framework
# =========================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# =========================
# Static & Media
# =========================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# =========================
# Auth redirects
# =========================
LOGIN_REDIRECT_URL = 'accounts:redirect_user'
LOGOUT_REDIRECT_URL = 'login_page'

# =========================
# Misc
# =========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MAX_POSTE = 3

USE_TZ = False
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Bamako'
