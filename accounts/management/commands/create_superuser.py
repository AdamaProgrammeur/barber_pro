from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from salon.models import UserSalon, Salon
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Crée un superuser par défaut si aucun n\'existe'

    def handle(self, *args, **options):
        # Vérifier si un superuser existe déjà
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.SUCCESS('Un superuser existe déjà.')
            )
            return

        # Créer le superuser
        username = os.environ.get('DEMO_USERNAME', 'admin')
        email = os.environ.get('DEMO_EMAIL', 'admin@salon.local')
        password = os.environ.get('DEMO_PASSWORD', 'admin123456')
        salon_name = os.environ.get('DEMO_SALON_NAME', 'Salon Demo')

        try:
            # Créer l'utilisateur
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name='Admin',
                last_name='Salon'
            )

            # Créer le salon par défaut
            salon, created = Salon.objects.get_or_create(
                nom=salon_name,
                defaults={
                    'adresse': 'Adresse par défaut',
                    'telephone': '+22300000000',
                    'email': email,
                    'status_paiement': True
                }
            )

            # Créer la relation UserSalon avec rôle admin
            UserSalon.objects.get_or_create(
                user=user,
                salon=salon,
                defaults={'role': 'admin'}
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Superuser créé avec succès:\n'
                    f'  Username: {username}\n'
                    f'  Email: {email}\n'
                    f'  Salon: {salon_name}\n'
                    f'  Mot de passe: {password}'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erreur lors de la création du superuser: {e}')
            )