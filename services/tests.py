from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from salon.models import Salon, UserSalon
from .models import Service

User = get_user_model()


class ServiceAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.salon1 = Salon.objects.create(nom="Salon 1", status=Salon.STATUS_APPROVED, paiement_effectue=True)
        self.salon2 = Salon.objects.create(nom="Salon 2", status=Salon.STATUS_APPROVED, paiement_effectue=True)
        self.user1 = User.objects.create_user(username="user1", password="pass")
        self.user2 = User.objects.create_user(username="user2", password="pass")
        UserSalon.objects.create(user=self.user1, salon=self.salon1, role="admin")
        UserSalon.objects.create(user=self.user2, salon=self.salon2, role="admin")
        self.service1 = Service.objects.create(salon=self.salon1, nom="Coupe", prix=1000)
        self.service2 = Service.objects.create(salon=self.salon2, nom="Coiffure", prix=2000)

    def test_service_list_filtered_by_salon(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('service-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nom'], 'Coupe')

    def test_service_list_requires_auth(self):
        response = self.client.get(reverse('service-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)