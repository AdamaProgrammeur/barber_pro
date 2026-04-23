from django.db import models
from salon.models import Salon

CATEGORIE_CHOICES = [
    ('LOYER', 'Loyer'),
    ('SALAIRE', 'Salaire'),
    ('MATERIEL', 'Matériel'),
    ('EAU_ELECTRICITE', 'Eau / Électricité'),
    ('PRODUIT', 'Produit coiffure'),
    ('AUTRE', 'Autre'),
]

class Depense(models.Model):
    salon      = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='depenses')
    libelle    = models.CharField(max_length=200)
    montant    = models.DecimalField(max_digits=10, decimal_places=2)
    categorie  = models.CharField(max_length=30, choices=CATEGORIE_CHOICES, default='AUTRE')
    date       = models.DateField()
    note       = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.libelle} — {self.montant} FCFA ({self.date})"
