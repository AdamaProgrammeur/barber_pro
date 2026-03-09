from django.db import models
from django.conf import settings

class Salon(models.Model):
    nom = models.CharField(max_length=150)
    logo = models.ImageField(upload_to="logos/", blank=True, null=True)
    adresse = models.TextField(blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    localisation = models.URLField(blank=True)
    max_postes = models.PositiveIntegerField(default=1)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom


class UserSalon(models.Model):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("receptionniste", "Réceptionniste"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name="membres")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ("user", "salon")

    def __str__(self):
        return f"{self.user.username} - {self.salon.nom} ({self.role})"
