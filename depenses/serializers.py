from rest_framework import serializers
from .models import Depense

class DepenseSerializer(serializers.ModelSerializer):
    salon = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model  = Depense
        fields = ['id', 'salon', 'libelle', 'montant', 'categorie', 'date', 'note', 'created_at']
        read_only_fields = ['id', 'salon', 'created_at']
