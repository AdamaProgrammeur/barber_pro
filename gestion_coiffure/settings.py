from pathlib import Path
import os
from decouple import Csv
import dj_database_url

# =========================
# Paths
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# ENV CONFIG (PRODUCTION SAFE)
# =========================
def config(key, default=None, cast=None):
    value = os.environ.get(key, default)

    if value is None:
        return default

    if cast is bool:
        return str(value).lower() in ("1", "true", "yes", "on")

    if cast is int:
        return int(value)

    if isinstance(cast, Csv):
        return [v.strip() for v in str(value).split(",") if v.strip()]

    if cast is not None:
        return cast(value)

    return value


# =========================
# Secrets & Debug
# =========================
DEBUG = config("DEBUG", default=True, cast=bool)

SECRET_KEY = config("SECRET_KEY", default="")

if not SECRET_KEY and not DEBUG:
    raise Exception("❌ SECRET_KEY manquant sur Render")
elif not SECRET_KEY:
    # Clé de secours pour le développement local uniquement
    SECRET_KEY = "django-insecure-dev-key-change-me-in-production"

# =========================
# Hosts & CSRF
# =========================
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="127.0.0.1",
    
    cast=Csv(),
)

# Ajout automatique de l'hôte Render en production
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Autoriser l'URL Render pour les vérifications CSRF (Indispensable pour l'admin)
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS = [f"https://{RENDER_EXTERNAL_HOSTNAME}"]


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
    'whitenoise.middleware.WhiteNoiseMiddleware',
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

db_url = config("DATABASE_URL", default=f"sqlite:///{BASE_DIR}/db.sqlite3")

DATABASES = {
    'default': dj_database_url.config(
        default=db_url,
        conn_max_age=600,
        ssl_require=not DEBUG
    )
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
# Utilisation d'un stockage plus tolérant pour éviter les erreurs 500 sur fichiers manquants
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

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
# Demo mode
# =========================
DEMO_LOGIN_ENABLED = config(
    "DEMO_LOGIN_ENABLED",
    default=str(DEBUG),
    cast=bool
)

DEMO_USERNAME = config("DEMO_USERNAME", default="demo_salon")
DEMO_PASSWORD = config("DEMO_PASSWORD", default="demo123456")
DEMO_EMAIL = config("DEMO_EMAIL", default="demo@salon.local")
DEMO_SALON_NAME = config("DEMO_SALON_NAME", default="Salon Demo")
