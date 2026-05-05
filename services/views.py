from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import PermissionDenied
from .models import Service
from .serializers import ServiceSerializer
from salon.models import UserSalon

class IsSalonAdminOrReadOnly(permissions.BasePermission):
    """
    Les utilisateurs authentifiés peuvent voir les services.
    Les admins du salon peuvent créer, modifier et supprimer.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_staff:
            return True

        return UserSalon.objects.filter(user=request.user, role='admin').exists()

class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = [IsSalonAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        if not self.request.user or not self.request.user.is_authenticated:
            return Service.objects.none()

        user_salon = UserSalon.objects.filter(user=self.request.user).first()
        if not user_salon:
            return Service.objects.none()

        return Service.objects.filter(salon=user_salon.salon)

    def perform_create(self, serializer):
        user_salon = UserSalon.objects.filter(user=self.request.user, role='admin').first()
        if not user_salon:
            raise PermissionDenied("Vous devez être admin du salon pour créer un service.")
        serializer.save(salon=user_salon.salon)
