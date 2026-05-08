from decimal import Decimal
from django.db.models import Sum
from rest_framework import serializers
from .models import Paiement


class PaiementSerializer(serializers.ModelSerializer):
    client_nom = serializers.SerializerMethodField()
    client_prenom = serializers.SerializerMethodField()
    service_nom = serializers.SerializerMethodField()
    prix_service = serializers.SerializerMethodField()
    reste = serializers.SerializerMethodField()
    date_debut = serializers.SerializerMethodField()

    class Meta:
        model = Paiement
        fields = [
            'id',
            'file_attente',
            'user',
            'montant',
            'statut',
            'mode_paiement',
            'date_paiement',
            'client_nom',
            'client_prenom',
            'service_nom',
            'prix_service',
            'reste',
            'date_debut',
        ]
        read_only_fields = [
            'date_paiement',
            'client_nom',
            'client_prenom',
            'service_nom',
            'prix_service',
            'reste',
            'date_debut',
            'user',
        ]

    def get_client_nom(self, obj):
        return obj.file_attente.client.nom if obj.file_attente and obj.file_attente.client else ""

    def get_client_prenom(self, obj):
        return obj.file_attente.client.prenom if obj.file_attente and obj.file_attente.client else ""

    def get_service_nom(self, obj):
        return obj.file_attente.service.nom if obj.file_attente and obj.file_attente.service else ""

    def get_prix_service(self, obj):
        return obj.file_attente.service.prix if obj.file_attente and obj.file_attente.service else Decimal('0.00')

    def get_reste(self, obj):
        if not obj.file_attente or not obj.file_attente.service:
            return Decimal('0.00')

        # Utilise les paiements déjà préchargés si possible
        paiements = obj.file_attente.paiements.all()
        total_paye = sum((p.montant for p in paiements if p.statut in ['VALIDE', 'EN_ATTENTE']), Decimal('0.00'))
        return obj.file_attente.service.prix - total_paye

    def get_date_debut(self, obj):
        if not obj.file_attente:
            return None
        return obj.file_attente.heure_arrivee
