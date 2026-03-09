from django.db import models
from salon.models import Salon

class Service(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name="services", default=None)
    nom = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='services_img/', blank=True, null=True)

    verbose_name = "Prix du service"
    error_messages = {
        'nom': {
            'blank': "Le nom du service ne peut pas être vide.",
        },
        'prix': {
            'invalid': "Le prix doit être un nombre valide.",
        },
    }

    def __str__(self):
        return self.nom

