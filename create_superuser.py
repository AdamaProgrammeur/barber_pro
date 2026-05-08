# create_superuser.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_coiffure.settings')
django.setup()
 
from django.contrib.auth import get_user_model

User = get_user_model()

# On utilise les variables définies dans le fichier render.yaml
username = os.environ.get("DEMO_USERNAME")
email = os.environ.get("DEMO_EMAIL")
password = os.environ.get("DEMO_PASSWORD")

if not username or not password:
    print("Superuser credentials not found in environment variables.")
    exit(0)

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created")
else:
    print("Superuser already exists")