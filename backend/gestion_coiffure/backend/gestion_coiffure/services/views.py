from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Service
from .serializers import ServiceSerializer
from salon.models import UserSalon
from salon.permissions import is_salon_active

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Admin d'un salon peut tout faire.
    Les autres utilisateurs authentifiés peuvent seulement lire.
    """

    def has_permission(self, request, view):
        if not is_salon_active(request.user):
            return False
        # Tous les utilisateurs authentifiés peuvent lire
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        # Pour écrire, vérifier que l'utilisateur est admin dans le salon du service
        if not request.user.is_authenticated:
            return False

        # Récupérer le salon lié au service
        salon = getattr(view, 'salon', None)
        if not salon:
            # Si pas défini dans la vue, autoriser uniquement si l'objet est fourni (POST/PUT géré via serializer)
            return True  # ou False selon ta logique

        # Vérifier dans UserSalon
        user_salon = UserSalon.objects.filter(
            user=request.user, salon=salon, role='admin'
        ).first()

        return bool(user_salon)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        """
        Si tu veux filtrer par salon pour chaque utilisateur, par exemple
        """
        user_salon = UserSalon.objects.filter(user=self.request.user).first()
        if user_salon:
            return Service.objects.filter(salon=user_salon.salon)
        return Service.objects.none()

    def perform_create(self, serializer):
        """
        Associer automatiquement le salon à un service créé par un admin
        """
        user_salon = UserSalon.objects.filter(user=self.request.user, role='admin').first()
        if user_salon:
            serializer.save(salon=user_salon.salon)
        else:
            raise permissions.PermissionDenied("Vous n'êtes pas admin dans un salon.")
