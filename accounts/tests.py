from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import User
from salon.models import Salon, UserSalon


class RegisterSalonApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('accounts:api:register_salon')

    def test_register_salon_creates_user_and_salon(self):
        payload = {
            'username': 'client_test1',
            'email': 'client_test1@example.com',
            'password': 'Password123',
            'password_confirm': 'Password123',
            'first_name': 'Client',
            'last_name': 'Test',
            'salon_nom': 'Salon Test',
            'salon_adresse': '123 Rue Principale',
            'salon_telephone': '+22370000000',
            'salon_email': 'salon@test.com',
            'salon_localisation': 'https://maps.google.com/',
            'max_postes': 3,
        }

        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        user = User.objects.get(username='client_test1')
        salon = Salon.objects.get(nom='Salon Test')
        usersalon = UserSalon.objects.get(user=user, salon=salon)

        self.assertEqual(user.email, 'client_test1@example.com')
        self.assertEqual(salon.adresse, '123 Rue Principale')
        self.assertEqual(usersalon.role, 'admin')

    def test_register_salon_passwords_must_match(self):
        payload = {
            'username': 'client_test2',
            'email': 'client_test2@example.com',
            'password': 'Password123',
            'password_confirm': 'Password124',
            'salon_nom': 'Salon Test 2',
        }

        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('password_confirm', response.data['errors'])
