from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from salon.models import Salon, UserSalon
from django.db import transaction

User = get_user_model()

class Command(BaseCommand):
    help = "Crée rapidement un compte Admin, un Salon et lie les deux."

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help="Email de l'admin", required=True)
        parser.add_argument('--password', type=str, help="Mot de passe", required=True)
        parser.add_argument('--salon', type=str, help="Nom du salon", required=True)

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        salon_name = options['salon']

        try:
            with transaction.atomic():
                # 1. Création de l'utilisateur avec le rôle ADMIN
                user, created = User.objects.get_or_create(
                    email=email,
                    defaults={
                        'username': email.split('@')[0],
                        'is_staff': True,
                        'is_active': True,
                        'is_superuser': True, # Recommandé pour un compte admin initial
                    }
                )

                if not created:
                    self.stdout.write(self.style.WARNING(f"L'utilisateur {email} existe déjà."))
                else:
                    user.set_password(password)
                    user.save()
                    self.stdout.write(self.style.SUCCESS(f"Utilisateur {email} créé avec le username: {user.username}"))

                # 2. Création du salon
                salon, s_created = Salon.objects.get_or_create(
                    nom=salon_name,
                    defaults={
                        'status': 'APPROVED',
                        'paiement_effectue': True
                    }
                )

                if s_created:
                    self.stdout.write(self.style.SUCCESS(f"Salon '{salon_name}' créé et activé."))

                # 3. Liaison User <-> Salon
                UserSalon.objects.get_or_create(
                    user=user, 
                    salon=salon, 
                    defaults={'role': 'admin'}
                )
                
                self.stdout.write(self.style.SUCCESS(f"Succès : {email} est maintenant admin de {salon_name}."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur lors de la création : {e}"))