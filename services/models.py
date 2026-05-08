from django.db import models
from salon.models import Salon


class Service(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='services')
    nom = models.CharField(max_length=150)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    description = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'services'
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['nom']

    def __str__(self):
        return self.nom
