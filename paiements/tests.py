from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from salon.models import Salon, UserSalon
from file_attente.models import FileAttente
from .models import Paiement

User = get_user_model()


class PaiementAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.salon1 = Salon.objects.create(nom="Salon 1", status=Salon.STATUS_APPROVED, paiement_effectue=True)
        self.salon2 = Salon.objects.create(nom="Salon 2", status=Salon.STATUS_APPROVED, paiement_effectue=True)
        self.user1 = User.objects.create_user(username="user1", password="pass")
        self.user2 = User.objects.create_user(username="user2", password="pass")
        UserSalon.objects.create(user=self.user1, salon=self.salon1, role="admin")
        UserSalon.objects.create(user=self.user2, salon=self.salon2, role="admin")
        self.file1 = FileAttente.objects.create(salon=self.salon1, nom_client="Client1")
        self.file2 = FileAttente.objects.create(salon=self.salon2, nom_client="Client2")
        self.paiement1 = Paiement.objects.create(file_attente=self.file1, user=self.user1, montant=1000)
        self.paiement2 = Paiement.objects.create(file_attente=self.file2, user=self.user2, montant=2000)

    def test_paiement_list_filtered_by_salon(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('paiement-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['montant'], '1000.00')

    def test_paiement_list_requires_auth(self):
        response = self.client.get(reverse('paiement-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)