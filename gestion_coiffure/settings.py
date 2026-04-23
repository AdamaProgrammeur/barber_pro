from pathlib import Path
import os
from dotenv import dotenv_values
from decouple import Csv

# =========================
# Paths
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

# Read .env file directly, ignoring system environment variables
_env = dotenv_values(BASE_DIR / ".env")

def config(key, default=None, cast=None):
    value = _env.get(key, default)
    if value is None:
        return default
    if cast is bool:
        return str(value).lower() in ("1", "true", "yes", "on")
    if cast is int:
        return int(value)
    if cast is Csv():
        return [v.strip() for v in str(value).split(",") if v.strip()]
    if cast is not None:
        return cast(value)
    return value

# =========================
# Secrets & Debug
# =========================
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)

# =========================
# Hosts & CSRF
# =========================
ALLOWED_HOSTS = [h.strip() for h in _env.get("ALLOWED_HOSTS", "unideating-sebrina-nonbindingly.ngrok-free.dev").split(",") if h.strip()]

CSRF_TRUSTED_ORIGINS = [
    "https://barber-pro-upue.onrender.com",
    # si tu utilises encore ngrok pour tests locaux
    "https://unideating-sebrina-nonbindingly.ngrok-free.dev",
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

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
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', cast=int),
    }
}

# =========================
# REST Framework
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

# =========================
# Mode demo
# =========================
DEMO_LOGIN_ENABLED = config("DEMO_LOGIN_ENABLED", default=str(DEBUG)).lower() in ("1", "true", "yes", "on")
DEMO_USERNAME = config("DEMO_USERNAME", default="demo_salon")
DEMO_PASSWORD = config("DEMO_PASSWORD", default="demo123456")
DEMO_EMAIL = config("DEMO_EMAIL", default="demo@salon.local")
DEMO_SALON_NAME = config("DEMO_SALON_NAME", default="Salon Demo")