from rest_framework import viewsets, permissions
from .models import Client
from .serializers import ClientSerializer
from salon.models import UserSalon
from salon.permissions import IsSalonActive

class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated, IsSalonActive]

    def get_queryset(self):
        """
        Filtrer uniquement les clients du salon de l'utilisateur connecté.
        """
        user_salon = UserSalon.objects.filter(user=self.request.user).first()
        if user_salon:
            return Client.objects.filter(salon=user_salon.salon).order_by('id')
        return Client.objects.none()

    def perform_create(self, serializer):
        """
        Associer automatiquement le salon à un Client créé par un admin.
        """
        user_salon = UserSalon.objects.filter(user=self.request.user, role='admin').first()
        if not user_salon:
            raise permissions.PermissionDenied("Vous n'êtes pas admin dans un salon.")
        serializer.save(salon=user_salon.salon)

    def perform_update(self, serializer):
        """
        S'assurer que le salon du client reste celui du salon de l'admin.
        """
        user_salon = UserSalon.objects.filter(user=self.request.user, role='admin').first()
        if not user_salon:
            raise permissions.PermissionDenied("Vous n'êtes pas admin dans un salon.")
        serializer.save(salon=user_salon.salon)

    def perform_destroy(self, instance):
        """
        Vérifier que seul un admin du salon peut supprimer un client.
        """
        user_salon = UserSalon.objects.filter(user=self.request.user, role='admin').first()
        if not user_salon or instance.salon != user_salon.salon:
            raise permissions.PermissionDenied("Vous ne pouvez pas supprimer ce client.")
        instance.delete()
