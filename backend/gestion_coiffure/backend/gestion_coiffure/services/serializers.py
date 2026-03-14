from rest_framework import serializers
from .models import Service



class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

    def validate_prix(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Le prix doit être supérieur à 0"
            )
        return value
