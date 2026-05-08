from rest_framework import serializers, viewsets
from .models import Service
from .serializers import ServiceSerializer
from salon.models import UserSalon
from salon.permissions import IsSalonActive


class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = [IsSalonActive]

    def get_queryset(self):
        user_salon = UserSalon.objects.filter(user=self.request.user).first()
        if user_salon:
            return Service.objects.filter(salon=user_salon.salon)
        return Service.objects.none()

    def perform_create(self, serializer):
        user_salon = UserSalon.objects.filter(user=self.request.user).first()
        if not user_salon:
            raise serializers.ValidationError({'salon': 'Salon non trouvé pour cet utilisateur.'})
        serializer.save(salon=user_salon.salon)

    def perform_update(self, serializer):
        user_salon = UserSalon.objects.filter(user=self.request.user).first()
        if not user_salon:
            raise serializers.ValidationError({'salon': 'Salon non trouvé pour cet utilisateur.'})
        serializer.save(salon=user_salon.salon)
