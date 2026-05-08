from django.db import models
from salon.models import Salon


class Client(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='clients')
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=150, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.nom} {self.prenom}".strip()
