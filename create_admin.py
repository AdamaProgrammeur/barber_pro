from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Cree un superutilisateur via variables d'environnement pour Render"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write(self.style.ERROR("❌ Variables manquantes : DJANGO_SUPERUSER_USERNAME ou DJANGO_SUPERUSER_PASSWORD"))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"⚠️ Admin '{username}' déjà existant"))
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        self.stdout.write(self.style.SUCCESS(f"✅ Admin '{username}' créé avec succès"))