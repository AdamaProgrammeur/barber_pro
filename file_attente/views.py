from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import FileAttente
from salon.models import UserSalon
from salon.permissions import IsSalonActive
from .serializers import FileAttenteSerializer
from paiements.models import Paiement
from paiements.serializers import PaiementSerializer

# -------------------------------
# Permissions dynamiques
# -------------------------------
class ReceptionnisteOrAdminForWork(permissions.BasePermission):
    """Autorise réceptionnistes ou admins du salon lié à la file"""
    def has_object_permission(self, request, view, obj):
        salon = getattr(obj.service, 'salon', None)
        if not salon:
            return False
        return UserSalon.objects.filter(
            user=request.user,
            salon=salon,
            role__in=['receptionniste', 'admin']
        ).exists()


class ReceptionnisteOrAdmin(permissions.BasePermission):
    """Autorise réceptionnistes ou admins du salon lié à la file"""
    def has_object_permission(self, request, view, obj):
        salon = getattr(obj.service, 'salon', None)
        if not salon:
            return False
        return UserSalon.objects.filter(
            user=request.user,
            salon=salon,
            role__in=['receptionniste', 'admin']
        ).exists()


# -------------------------------
# FileAttente ViewSet
# -------------------------------
class FileAttenteViewSet(viewsets.ModelViewSet):
    serializer_class = FileAttenteSerializer

    def get_permissions(self):
        if self.action in ['commencer', 'terminer']:
            permission_classes = [permissions.IsAuthenticated, IsSalonActive, ReceptionnisteOrAdminForWork]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, IsSalonActive, ReceptionnisteOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated, IsSalonActive]
        return [p() for p in permission_classes]

    def get_queryset(self):
        """Filtrer uniquement les files du salon de l'utilisateur connecté"""
        user_salon = UserSalon.objects.filter(user=self.request.user).first()
        if not user_salon:
            return FileAttente.objects.none()
        return FileAttente.objects.filter(service__salon=user_salon.salon).order_by('rang')

    def perform_create(self, serializer):
        """Vérifie que le service appartient au salon de l'utilisateur"""
        user_salon = UserSalon.objects.filter(user=self.request.user).first()
        if not user_salon:
            raise permissions.PermissionDenied("Impossible de créer une file sans salon")

        salon_utilisateur = user_salon.salon
        service = serializer.validated_data.get('service')
        if service.salon != salon_utilisateur:
            raise permissions.PermissionDenied("Le service doit appartenir au salon de l'utilisateur")

        serializer.save()

    # -------------------------------
    # Actions personnalisées
    # -------------------------------
    @action(detail=True, methods=['post'], url_path='commencer')
    def commencer(self, request, pk=None):
        """Marquer la file comme en cours"""
        file = self.get_object()
        file.statut = "EN_COURS"
        file.heure_debut = timezone.now()
        file.save()
        serializer = self.get_serializer(file)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='terminer')
    def terminer(self, request, pk=None):
        """Marquer la file comme terminée"""
        file = self.get_object()
        file.statut = "TERMINE"
        file.heure_fin = timezone.now()
        file.save()
        serializer = self.get_serializer(file)
        return Response(serializer.data, status=status.HTTP_200_OK)
