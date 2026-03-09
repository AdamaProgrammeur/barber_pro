from rest_framework import serializers
from decimal import Decimal, InvalidOperation
from .models import Paiement, MODE_PAIEMENT_CHOICES

# 1️⃣ Champ Decimal "friendly" pour éviter InvalidOperation
class FriendlyDecimalField(serializers.DecimalField):
    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except (TypeError, ValueError, InvalidOperation):
            raise serializers.ValidationError(
                "Le montant doit être un nombre valide (ex: 2500.00)"
            )

class PaiementSerializer(serializers.ModelSerializer):
    # Remplacer montant par le champ FriendlyDecimalField
    montant = FriendlyDecimalField(max_digits=10, decimal_places=2)

    # champs calculés pour la vue JS
    client_nom = serializers.SerializerMethodField()
    service_nom = serializers.SerializerMethodField()
    prix_service = serializers.SerializerMethodField()
    reste = serializers.SerializerMethodField()

    class Meta:
        model = Paiement
        fields = '__all__'  # les champs calculés sont automatiquement inclus
        read_only_fields = ('statut', 'date_paiement')

    def get_client_nom(self, obj):
        return f"{obj.file_attente.client.nom} {obj.file_attente.client.prenom}"

    def get_service_nom(self, obj):
        return obj.file_attente.service.nom

    def get_prix_service(self, obj):
        return obj.file_attente.service.prix

    def get_reste(self, obj):
        prix = obj.file_attente.service.prix
        return prix - obj.montant

    # 2️⃣ Validation du mode de paiement
    def validate_mode_paiement(self, value):
        if value not in dict(MODE_PAIEMENT_CHOICES).keys():
            raise serializers.ValidationError("Mode de paiement invalide.")
        return value

    # 3️⃣ Validation du montant > 0
    def validate_montant(self, value):
        if value <= 0:
            raise serializers.ValidationError("Le montant doit être supérieur à 0")
        return value

    # 4️⃣ Validation globale (optionnelle) pour vérifier que montant = service.prix
    def validate(self, data):
        file_attente = data.get('file_attente')
        montant = data.get('montant')
        if file_attente and montant is not None:
            if montant != file_attente.service.prix:
                raise serializers.ValidationError(
                    f"Le montant doit être égal au prix du service ({file_attente.service.prix})"
                )
        return data
