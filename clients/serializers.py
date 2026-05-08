from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'salon', 'nom', 'prenom', 'telephone', 'adresse']
        read_only_fields = ['salon']  # Salon is auto-assigned
