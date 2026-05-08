from django.db.models import Q
from rest_framework import permissions, viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import Paiement
from .serializers import PaiementSerializer
from salon.models import UserSalon
from salon.permissions import IsSalonActive
from file_attente.models import FileAttente
from file_attente.serializers import FileAttenteSerializer


class PaiementViewSet(viewsets.ModelViewSet):
    serializer_class = PaiementSerializer
    permission_classes = [permissions.IsAuthenticated, IsSalonActive]

    def get_queryset(self):
        user_salon = UserSalon.objects.filter(user=self.request.user).first()
        if user_salon:
            salon = user_salon.salon
            return Paiement.objects.select_related(
                'file_attente',
                'file_attente__client',
                'file_attente__service'
            ).filter(
                Q(file_attente__salon=salon) |
                Q(file_attente__service__salon=salon)
            )
        return Paiement.objects.none()

    def perform_create(self, serializer):
        user_salon = UserSalon.objects.filter(user=self.request.user).first()
        if not user_salon:
            raise PermissionDenied("Vous n'êtes rattaché à aucun salon actif.")

        file_attente = serializer.validated_data.get('file_attente')
        if not file_attente:
            raise PermissionDenied("Le ticket de file d'attente est requis.")

        ticket_salon = file_attente.salon or getattr(file_attente.service, 'salon', None)
        if not ticket_salon:
            raise PermissionDenied("Impossible de déterminer le salon pour ce ticket.")

        if ticket_salon != user_salon.salon:
            raise PermissionDenied("Ce ticket ne fait pas partie de votre salon.")

        if not file_attente.salon:
            file_attente.salon = ticket_salon
            file_attente.save(update_fields=['salon'])

        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Retrieve the updated FileAttente object and serialize it
        file_attente_instance = serializer.validated_data['file_attente']
        file_attente_instance.refresh_from_db() # Ensure the instance is fresh from the database
        file_attente_serializer = FileAttenteSerializer(file_attente_instance, context={'request': request})
        
        headers = self.get_success_headers(serializer.data)
        return Response(file_attente_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
