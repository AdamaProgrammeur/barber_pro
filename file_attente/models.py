from django.db import models

# Create your models here.
from django.db import models
from salon.models import Salon
from clients.models import Client
from services.models import Service

STATUT_CHOICES = (
    ('EN_ATTENTE', 'En attente'),
    ('EN_COURS', 'En cours'),
    ('TERMINE', 'Terminé'),
)

class FileAttente(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, null=True, blank=True, related_name="file_attente")  # 🔹 nouveau
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE')
    rang = models.PositiveIntegerField(null=True, blank=True)
    heure_arrivee = models.DateTimeField(auto_now_add=True)
    heure_fin = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.client.nom} - {self.service.nom} ({self.statut})"
