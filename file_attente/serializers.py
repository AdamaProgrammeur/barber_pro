from rest_framework import serializers
from .models import FileAttente
from paiements.models import Paiement
from decimal import Decimal
from django.db.models import Sum

class FileAttenteSerializer(serializers.ModelSerializer):
    client_nom = serializers.SerializerMethodField()
    client_prenom = serializers.SerializerMethodField()
    client_name = serializers.SerializerMethodField()
    service_nom = serializers.SerializerMethodField()
    service_name = serializers.SerializerMethodField()
    prix_service = serializers.SerializerMethodField()
    service_prix = serializers.SerializerMethodField()
    date_debut = serializers.SerializerMethodField()
    heure = serializers.SerializerMethodField()
    paiement_info = serializers.SerializerMethodField()  # Infos paiement optimisées

    class Meta:
        model = FileAttente
        fields = '__all__'
        read_only_fields = ('statut', 'heure_arrivee', 'heure_fin', 'rang')

    # -------------------------------
    # Champs calculés
    # -------------------------------
    def get_client_nom(self, obj):
        return obj.client.nom if obj.client else ""

    def get_client_prenom(self, obj):
        return obj.client.prenom if obj.client else ""

    def get_service_nom(self, obj):
        return obj.service.nom if obj.service else ""

    def get_service_name(self, obj):
        return obj.service.nom if obj.service else ""

    def get_prix_service(self, obj):
        return obj.service.prix if obj.service else Decimal('0.00')

    def get_service_prix(self, obj):
        return obj.service.prix if obj.service else Decimal('0.00')

    def get_client_name(self, obj):
        return obj.client.nom if obj.client else ""

    def get_heure(self, obj):
        return obj.heure_arrivee if obj.heure_arrivee else None

    def get_date_debut(self, obj):
        return obj.heure_arrivee if obj.heure_arrivee else None
    def get_paiement_info(self, obj):
        # ✅ Récupère tous les paiements liés à ce ticket
        # Utilise le cache du prefetch pour éviter des requêtes SQL N+1
        all_paiements = list(obj.paiements.all()) if hasattr(obj, 'paiements') else list(obj.paiement_set.all())
        
        # Calcul en mémoire (ultra rapide)
        total_paye = sum((p.montant for p in all_paiements if p.statut in ["VALIDE", "EN_ATTENTE"]), Decimal('0.00'))
        
        prix_service = obj.service.prix if obj.service else Decimal('0.00')
        reste = prix_service - total_paye

        # Détermination du statut global du ticket
        if total_paye >= prix_service:
            statut_global = "VALIDE"
        elif total_paye > 0:
            statut_global = "PARTIEL"
        else:
            # On vérifie dans la liste déjà chargée
            if any(p.statut == "EN_ATTENTE" for p in all_paiements):
                statut_global = "EN_ATTENTE"
            else:
                statut_global = "NON_PAYE"

        dernier_paiement = all_paiements[-1] if all_paiements else None

        return {
            "montant_paye": total_paye,
            "reste": max(Decimal('0.00'), reste),
            "statut": statut_global,
            "mode_paiement": dernier_paiement.mode_paiement if dernier_paiement else None,
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

        # ✅ Correction : Calculer le rang SPECIFIQUE au salon concerné
        salon = validated_data.get('salon')
        en_attente_count = FileAttente.objects.filter(salon=salon, statut='EN_ATTENTE').count()
        
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