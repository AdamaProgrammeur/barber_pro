from django.db import models
from salon.models import Salon


class Client(models.Model):
    
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name="clients", default=None)
    adresse = models.CharField(max_length=255, default="")
    telephone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom
