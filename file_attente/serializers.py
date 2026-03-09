from rest_framework import serializers
from .models import FileAttente
from paiements.models import Paiement
from decimal import Decimal

class FileAttenteSerializer(serializers.ModelSerializer):
    client_name = serializers.SerializerMethodField()
    client_prenom = serializers.SerializerMethodField()
    service_name = serializers.SerializerMethodField()
    service_prix = serializers.SerializerMethodField()
    paiement_info = serializers.SerializerMethodField()  # Infos paiement optimisées

    class Meta:
        model = FileAttente
        fields = '__all__'
        read_only_fields = ('statut', 'heure_arrivee', 'heure_fin', 'rang')

    # -------------------------------
    # Champs calculés
    # -------------------------------
    def get_client_name(self, obj):
        return obj.client.nom if obj.client else ""

    def get_client_prenom(self, obj):
        return obj.client.prenom if obj.client else ""

    def get_service_name(self, obj):
        return obj.service.nom if obj.service else ""

    def get_service_prix(self, obj):
        return obj.service.prix if obj.service else Decimal('0.00')
    def get_paiement_info(self, obj):
        # ✅ Récupère tous les paiements liés
        paiements = getattr(obj, 'paiements', None)
        if paiements is None:
            paiements = obj.paiement_set.all()  # fallback si pas de related_name

        paiement_valide = paiements.filter(statut="VALIDE").first()
        if not paiement_valide:
            # Si aucun paiement VALIDE, renvoyer le paiement en attente si existant
            paiement_valide = paiements.filter(statut="EN_ATTENTE").first()
        
        if not paiement_valide:
            return {
                "montant_paye": Decimal('0.00'),
                "reste": obj.service.prix if obj.service else Decimal('0.00'),
                "statut": "NON_PAYE",
                "mode_paiement": None,
            }

        montant_paye = paiement_valide.montant
        prix_service = obj.service.prix if obj.service else Decimal('0.00')
        reste = prix_service - montant_paye

        return {
            "paiement_id": paiement_valide.id,
            "montant_paye": montant_paye,
            "reste": reste,
            "statut": paiement_valide.statut,
            "mode_paiement": paiement_valide.mode_paiement,
        }

    # -------------------------------
    # Validation
    # -------------------------------
    def validate(self, data):
        if not data.get('client'):
            raise serializers.ValidationError({"client": "Le client est obligatoire."})
        if not data.get('service'):
            raise serializers.ValidationError({"service": "Le service est obligatoire."})
        return data

    # -------------------------------
    # Création
    # -------------------------------
    def create(self, validated_data):
        existe = FileAttente.objects.filter(
            client=validated_data['client'],
            statut__in=['EN_ATTENTE', 'EN_COURS']
        ).exists()
        if existe:
            raise serializers.ValidationError("Ce client est déjà dans la file d'attente.")

        # Calcul automatique du rang
        en_attente_count = FileAttente.objects.filter(statut='EN_ATTENTE').count()
        validated_data['rang'] = en_attente_count + 1
        validated_data['statut'] = 'EN_ATTENTE'

        return super().create(validated_data)

    # -------------------------------
    # Mise à jour
    # -------------------------------
    def update(self, instance, validated_data):
        new_client = validated_data.get('client', instance.client)
        if new_client != instance.client:
            existe = FileAttente.objects.filter(
                client=new_client,
                statut__in=['EN_ATTENTE', 'EN_COURS']
            ).exclude(id=instance.id).exists()
            if existe:
                raise serializers.ValidationError("Ce client est déjà dans la file d'attente.")

        instance.client = new_client
        instance.service = validated_data.get('service', instance.service)
        instance.save()
        return instance