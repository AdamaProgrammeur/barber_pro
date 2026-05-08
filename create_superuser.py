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

username = os.environ.get("DEMO_USERNAME")
email = os.environ.get("DEMO_EMAIL")
password = os.environ.get("DEMO_PASSWORD")
salon_name = os.environ.get("DEMO_SALON_NAME", "Salon BarberPro")

if not username or not password:
    print("Superuser credentials not found in environment variables.")
    exit(0)

user, created = User.objects.get_or_create(username=username, defaults={"email": email})
user.set_password(password)
user.is_staff = True
user.is_superuser = True
user.save()
print("Superuser created" if created else "Superuser updated")

if Salon and UserSalon and not Salon.objects.exists():
    salon = Salon.objects.create(nom=salon_name)
    UserSalon.objects.get_or_create(user=user, salon=salon, defaults={"role": "admin"})
    print(f"Salon '{salon_name}' créé.")

