from django.db import models

from django.db import models
from file_attente.models import FileAttente

MODE_PAIEMENT_CHOICES = (
    ('ESPECE', 'Espèce'),
    ('ORANGE_MONEY', 'Orange Money'),
    ('MOOV', 'Moov Africa'),
)

STATUT_CHOICES = [
    ("EN_ATTENTE", "En attente"),
    ("EN_COURS", "En cours"),
    ("TERMINE", "Terminé"),
    ("NON_PAYE", "Non payé"),  # 🔥 nouveau
]


class Paiement(models.Model):
    file_attente = models.ForeignKey(FileAttente, related_name='paiements', on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    mode_paiement = models.CharField(max_length=50, choices=MODE_PAIEMENT_CHOICES)  # ex: "Orange Money"
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES
    )
    #created_at = models.DateTimeField(auto_now_add=True,default=None)  # Date de création du paiement
    created_at= models.DateTimeField(auto_now_add=True)

'''
le prix de montant doit etre egale a montant service que le cliet a choisi
'''