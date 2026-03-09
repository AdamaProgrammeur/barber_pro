from decimal import Decimal
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from .models import Paiement
from file_attente.models import FileAttente
from salon.models import UserSalon
from .serializers import PaiementSerializer

# -------------------------------
# Permissions dynamiques
# -------------------------------
class ReceptionnisteOrAdminPermission(permissions.BasePermission):
    """Autorise réceptionnistes ou admin du salon."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        file = getattr(obj, 'file_attente', None)
        if not file:
            return False
        salon = file.salon or getattr(file.service, "salon", None)
        if not salon:
            return False

        # Vérifie si l'utilisateur a un rôle autorisé dans le salon
        return UserSalon.objects.filter(
            user=request.user,
            salon=salon,
            role__in=['receptionniste', 'admin']  # <-- inclure admin
        ).exists()


# -------------------------------
# Paiement ViewSet
# -------------------------------
class PaiementViewSet(viewsets.ModelViewSet):
    queryset = Paiement.objects.all()
    serializer_class = PaiementSerializer
    permission_classes = [ReceptionnisteOrAdminPermission]

    @staticmethod
    def _get_file_salon(file_obj):
        return file_obj.salon or getattr(file_obj.service, "salon", None)

    def get_queryset(self):
        qs = Paiement.objects.exclude(statut="VALIDE")
        user = self.request.user
        if UserSalon.objects.filter(user=user, role='admin').exists():
            return qs  # Admin d'au moins un salon voit tout
        salons_ids = UserSalon.objects.filter(user=user).values_list('salon__id', flat=True)
        return qs.filter(
            Q(file_attente__salon__id__in=salons_ids) |
            Q(file_attente__service__salon__id__in=salons_ids)
        ).distinct()

    @action(detail=False, methods=["get"], url_path="today")
    def today(self, request):
        today = timezone.localtime(timezone.now()).date()
        qs = self.get_queryset().filter(created_at__date=today)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def create(self, request):
        file_id = request.data.get("file_attente")
        file = get_object_or_404(FileAttente, id=file_id)
        salon = self._get_file_salon(file)
        if not salon:
            return Response({"error": "Salon introuvable pour cette file."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Vérifier permission pour ce salon
        if not UserSalon.objects.filter(
            user=request.user,
            salon=salon,
            role__in=['receptionniste', 'admin']  # <-- inclure admin
        ).exists():
            return Response({"error": "Permission refusée pour ce salon."},
                            status=status.HTTP_403_FORBIDDEN)

        montant_recu = Decimal(request.data.get("montant", 0))
        if montant_recu <= 0:
            return Response({"error": "Montant invalide."}, status=status.HTTP_400_BAD_REQUEST)

        paiement, created = Paiement.objects.get_or_create(
            file_attente=file,
            defaults={
                "montant": 0,
                "statut": "EN_ATTENTE",
                "mode_paiement": request.data.get("mode_paiement", "ORANGE_MONEY"),
            }
        )

        if not created and paiement.statut == "VALIDE":
            return Response({"error": "Le paiement est déjà validé."}, status=status.HTTP_400_BAD_REQUEST)

        nouveau_total = paiement.montant + montant_recu
        prix_service = file.service.prix

        if nouveau_total > prix_service:
            return Response({"error": f"Montant trop élevé. Prix du service = {prix_service}"},
                            status=status.HTTP_400_BAD_REQUEST)

        paiement.montant = nouveau_total
        paiement.statut = "VALIDE" if nouveau_total == prix_service else "EN_ATTENTE"
        paiement.mode_paiement = request.data.get("mode_paiement", paiement.mode_paiement)
        paiement.save()

        return Response({
            "file_attente_id": file.id,
            "paiement_id": paiement.id,
            "montant_paye": paiement.montant,
            "prix_service": prix_service,
            "reste": prix_service - paiement.montant,
            "statut": paiement.statut,
            "mode_paiement": paiement.mode_paiement
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["POST"], url_path="non_payes")
    def mark_non_paye(self, request):
        file_id = request.data.get("file_attente")
        montant = Decimal(request.data.get("montant", 0))
        file = get_object_or_404(FileAttente, id=file_id)
        salon = self._get_file_salon(file)
        if not salon:
            return Response({"error": "Salon introuvable pour cette file."},
                            status=status.HTTP_400_BAD_REQUEST)

        if not UserSalon.objects.filter(
            user=request.user,
            salon=salon,
            role__in=['receptionniste', 'admin']
        ).exists():
            return Response({"error": "Permission refusée pour ce salon."},
                            status=status.HTTP_403_FORBIDDEN)

        paiement, created = Paiement.objects.get_or_create(
            file_attente=file,
            defaults={
                "montant": montant,
                "statut": "NON_PAYE",
                "mode_paiement": request.data.get("mode_paiement", "ESPECE"),
            }
        )

        if not created:
            paiement.statut = "NON_PAYE"
            paiement.save()

        reste = file.service.prix - paiement.montant

        return Response({
            "file_attente_id": file.id,
            "paiement_id": paiement.id,
            "montant_paye": paiement.montant,
            "reste": reste,
            "statut": paiement.statut
        }, status=status.HTTP_200_OK)
