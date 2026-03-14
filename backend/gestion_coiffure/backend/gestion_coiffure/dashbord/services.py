from django.utils import timezone
from clients.models import Client
from paiements.models import Paiement
from accounts.models import User
from django.db.models import Sum

from file_attente.models import FileAttente

def dashboard_stats():
    today = timezone.now().date()

    file_en_attente = FileAttente.objects.filter(statut="EN_ATTENTE")
    file_en_cours = FileAttente.objects.filter(statut="EN_COURS")
    file_termine = FileAttente.objects.filter(statut="TERMINE")

    clients_data = {
        "total": Client.objects.count(),
        "en_attente": file_en_attente.count(),
        "en_cours": file_en_cours.count(),
        "termine": file_termine.count(),
    }

    paiements_total_today = Paiement.objects.filter(
        date_paiement__date=today,
        statut="VALIDE"
    ).aggregate(total=Sum("montant"))["total"] or 0

    users_data = {
        "coiffeurs": User.objects.filter(role="COIFFEUR").count(),
        "receptionnistes": User.objects.filter(role="RECEPTIONNISTE").count(),
    }

    return {
        "clients": clients_data,
        "paiements": {"total_today": paiements_total_today},
        "users": users_data
    }
