from rest_framework import viewsets, permissions
from salon.models import UserSalon
from salon.permissions import IsSalonActive
from .models import Depense
from .serializers import DepenseSerializer


class DepenseViewSet(viewsets.ModelViewSet):
    serializer_class   = DepenseSerializer
    permission_classes = [permissions.IsAuthenticated, IsSalonActive]

    def get_queryset(self):
        user_salon = UserSalon.objects.filter(user=self.request.user).first()
        if not user_salon:
            return Depense.objects.none()
        return Depense.objects.filter(salon=user_salon.salon)

    def perform_create(self, serializer):
        user_salon = UserSalon.objects.filter(user=self.request.user).first()
        serializer.save(salon=user_salon.salon)
