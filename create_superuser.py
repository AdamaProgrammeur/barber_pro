# create_superuser.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_coiffure.settings')
django.setup()
 
from django.contrib.auth import get_user_model
try:
    from salon.models import Salon, UserSalon
except ImportError:
    Salon, UserSalon = None, None

User = get_user_model()

# On utilise les variables définies dans le fichier render.yaml
username = os.environ.get("DEMO_USERNAME")
email = os.environ.get("DEMO_EMAIL")
password = os.environ.get("DEMO_PASSWORD")
salon_name = os.environ.get("DEMO_SALON_NAME", "Salon BarberPro")

if not username or not password:
    print("Superuser credentials not found in environment variables.")
    exit(0)

if not User.objects.filter(username=username).exists():
    user = User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created")

    # Création du salon initial pour que l'app soit prête immédiatement
    if Salon and UserSalon and not Salon.objects.exists():
        salon = Salon.objects.create(nom=salon_name)
        UserSalon.objects.create(user=user, salon=salon, role='admin')
        print(f"Salon '{salon_name}' créé et lié à l'administrateur.")
else:
    print("Superuser already exists")