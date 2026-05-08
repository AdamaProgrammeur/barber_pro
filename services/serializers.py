from rest_framework import serializers
from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    salon = serializers.PrimaryKeyRelatedField(read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Service
        fields = ['id', 'salon', 'nom', 'prix', 'image', 'description']
        read_only_fields = ['salon']
