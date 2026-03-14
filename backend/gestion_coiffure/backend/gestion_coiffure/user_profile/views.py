# accounts/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth.models import User

class ProfileViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # GET /profile_api/ pour récupérer le profil
        user = request.user
        return Response({
            "email": user.email,
            "username": user.username,
            "is_admin": user.is_superuser,
             "max_postes": getattr(user.profile, "max_postes", None)
        })

    def partial_update(self, request, pk=None):
        # PATCH /profile_api/ pour mettre à jour le profil
        user = request.user
        data = request.data

        user.email = data.get("email", user.email)
        nom_complet = data.get("nom_complet", f"{user.first_name} {user.last_name}")
        user.first_name = nom_complet.split(" ")[0] if nom_complet else ""
        user.last_name = " ".join(nom_complet.split(" ")[1:]) if nom_complet else ""
        user.save()

        return Response({"detail": "Profil mis à jour avec succès"}, status=status.HTTP_200_OK)
