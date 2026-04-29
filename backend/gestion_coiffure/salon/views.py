from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserSalon, Salon
from .serializers import (
    UserSalonSerializer,
    SalonSerializer,
)
from .permissions import IsSalonActive
from .permissions import is_salon_active


# =========================
# ViewSet pour les utilisateurs du salon
# =========================
class UserSalonViewSet(viewsets.ModelViewSet):
    serializer_class = UserSalonSerializer
    permission_classes = [permissions.IsAuthenticated, IsSalonActive]

    def get_queryset(self):
        """
        Récupère uniquement les utilisateurs du salon du user connecté
        """
        user_salon = UserSalon.objects.filter(user=self.request.user).first()
        if not user_salon:
            return UserSalon.objects.none()
        return UserSalon.objects.filter(salon=user_salon.salon)

    def perform_create(self, serializer):
        user_salon = UserSalon.objects.filter(user=self.request.user).first()
        if user_salon:
            serializer.save(salon=user_salon.salon)
        else:
            raise PermissionError("Impossible de créer un utilisateur sans salon")

# =========================
# Récupérer et mettre à jour le profil du salon
# =========================
class SalonProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = SalonSerializer
    permission_classes = [permissions.IsAuthenticated, IsSalonActive]

    def get_object(self):
        user_salon = UserSalon.objects.filter(user=self.request.user).first()
        if user_salon:
            return user_salon.salon
        return None


# =========================
# Récupérer et mettre à jour le logo du salon
# =========================
class SalonLogoView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsSalonActive]

    # Récupérer le logo
    def get(self, request):
        user_salon = UserSalon.objects.filter(user=request.user).first()
        if not user_salon:
            return Response({"logo": None, "nom": "Salon"})
        salon = user_salon.salon
        return Response({
            "logo": request.build_absolute_uri(salon.logo.url) if salon.logo else None,
            "nom": salon.nom
        })

    # Enregistrer le logo
    def post(self, request):
        user_salon = UserSalon.objects.filter(user=request.user).first()
        if not user_salon:
            return Response({"error": "Salon introuvable"}, status=status.HTTP_404_NOT_FOUND)

        salon = user_salon.salon
        logo = request.FILES.get("logo")

        if not logo:
            return Response({"error": "Aucun fichier envoyé"}, status=status.HTTP_400_BAD_REQUEST)

        salon.logo = logo
        salon.save()

        return Response({
            "message": "Logo enregistré avec succès",
            "logo": request.build_absolute_uri(salon.logo.url)
        }, status=status.HTTP_200_OK)


# =========================
# Statut du salon (accessible meme si inactif)
# =========================
class SalonStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_salon = UserSalon.objects.filter(user=request.user).first()
        if not user_salon:
            return Response({"error": "Salon introuvable"}, status=status.HTTP_404_NOT_FOUND)

        salon = user_salon.salon
        return Response(
            {
                "salon_id": salon.id,
                "salon_nom": salon.nom,
                "status": salon.status,
                "paiement_effectue": salon.paiement_effectue,
                "can_use_app": is_salon_active(request.user),
                "message": (
                    "Votre salon n'est pas encore validé par les administrateurs. "
                    "Merci de patienter ou d'appeler BarbrePro au 223 78746643."
                ),
                "contact": "223 78746643",
            },
            status=status.HTTP_200_OK,
        )
