from pathlib import Path
import os

# =========================
# Paths
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# Secrets & Debug
# =========================
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-your-secret-key-here-change-in-production')

DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

# =========================
# Hosts & CSRF
# =========================
ALLOWED_HOSTS = [h.strip() for h in os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',') if h]

# Ajout automatique de l'hôte Render en production
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    # Autoriser l'URL Render pour les vérifications CSRF (Indispensable pour l'admin)
    CSRF_TRUSTED_ORIGINS = [f"https://{RENDER_EXTERNAL_HOSTNAME}"]
    # Indispensable pour que Django reconnaisse le HTTPS derrière le proxy de Render
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
else:
    CSRF_TRUSTED_ORIGINS = []

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
    'accounts',
    'rest_framework',

    'frontend',
    'clients',
    'services',
    'paiements',
    'file_attente',
    'dashbord',
    'salon',
    'depenses',
]

AUTH_USER_MODEL = 'accounts.User'
# =========================
# Middleware
# =========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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
# On lit DATABASE_URL pour Render (SQLite sur disque persistant)
# sinon on utilise le chemin local par défaut.
database_url = os.environ.get('DATABASE_URL')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}
if database_url and database_url.startswith('sqlite:///'):
    DATABASES['default']['NAME'] = database_url.replace('sqlite:///', '')
else:
    DATABASES['default']['NAME'] = BASE_DIR / 'db.sqlite3'

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
# Utilisation d'un stockage plus tolérant pour éviter les erreurs 500 sur fichiers manquants
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

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
