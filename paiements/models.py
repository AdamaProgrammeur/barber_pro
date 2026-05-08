from django.db import models
from django.conf import settings
from file_attente.models import FileAttente


class Paiement(models.Model):
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('VALIDE', 'Valide'),
        ('REFUSE', 'Refusé'),
    ]
    MODE_CHOICES = [
        ('CASH', 'Espèce'),
        ('CARD', 'Carte'),
        ('MOBILE', 'Mobile'),
        ('ORANGE_MONEY', 'Orange Money'),
        ('MOOV', 'Moov Africa'),
        ('OTHER', 'Autre'),
    ]

    file_attente = models.ForeignKey(FileAttente, on_delete=models.CASCADE, related_name='paiements')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE')
    mode_paiement = models.CharField(max_length=20, choices=MODE_CHOICES, blank=True)
    date_paiement = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Paiement'
        verbose_name_plural = 'Paiements'
        ordering = ['-date_paiement']

    def __str__(self):
        return f"Paiement {self.id} - {self.montant} ({self.statut})"
