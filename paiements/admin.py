from django.contrib import admin
from .models import Paiement


@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_attente', 'montant', 'statut', 'mode_paiement', 'date_paiement')
    list_filter = ('statut', 'mode_paiement', 'date_paiement')
    search_fields = ('file_attente__client__nom', 'montant')
    ordering = ('-date_paiement',)