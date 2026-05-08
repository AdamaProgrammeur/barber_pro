from rest_framework import viewsets, permissions
from .models import Client
from .serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Limiter aux clients du salon de l'utilisateur si le salon est lié
            salons = user.usersalon_set.values_list('salon_id', flat=True)
            return Client.objects.filter(salon_id__in=salons)
        return Client.objects.none()

    def perform_create(self, serializer):
        # Auto-assign salon from user's first salon
        user = self.request.user
        salon = user.usersalon_set.first().salon if user.usersalon_set.exists() else None
        if salon:
            serializer.save(salon=salon)
        else:
            serializer.save()
