from rest_framework import serializers
from .models import Client
import re

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
    
    def validate_nom(self, value):
        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError("Le nom doit contenir uniquement des lettres.")
        return value

    
    def validate_telephone(self, value):
        # Enlever espaces et tirets
        numero = re.sub(r'[\s\-]', '', value)

        # Vérifier que ce ne sont que des chiffres (après +223 optionnel)
        if numero.startswith('+223'):
            numero_sans_code = numero[4:]
        else:
            numero_sans_code = numero

        if not numero_sans_code.isdigit():
            raise serializers.ValidationError("Le numéro doit contenir uniquement des chiffres après le code pays.")

        if len(numero_sans_code) != 8:
            raise serializers.ValidationError("Le numéro doit contenir exactement 8 chiffres après le code pays.")

        if numero_sans_code[0] not in '56789':
            raise serializers.ValidationError("Le numéro doit commencer par 5, 6, 7, 8 ou 9.")

        return numero