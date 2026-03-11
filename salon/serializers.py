from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserSalon, Salon

User = get_user_model()

class UserSalonSerializer(serializers.ModelSerializer):
    # Champs imbriqués pour l'utilisateur
    username = serializers.CharField(source='user.username', write_only=False)
    email = serializers.EmailField(source='user.email', write_only=False)
    first_name = serializers.CharField(source='user.first_name', write_only=False)
    last_name = serializers.CharField(source='user.last_name', write_only=False)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserSalon
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'salon', 'password']
        extra_kwargs = {
            'salon': {'read_only': True},  # le salon sera attribué automatiquement
        }

    def validate(self, attrs):
        user_data = attrs.get('user', {})
        username = user_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "Ce nom d'utilisateur existe déjà."})
        return attrs

    def create(self, validated_data):
        user_data = validated_data.pop('user', {})
        password = validated_data.pop('password')

        # Création de l'utilisateur
        user = User.objects.create(
            username=user_data.get('username'),
            email=user_data.get('email', ''),
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', '')
        )
        user.set_password(password)
        user.save()

        # Création du UserSalon
        user_salon = UserSalon.objects.create(user=user, **validated_data)

        # Marquer le salon en attente d'approbation
        if hasattr(user_salon, 'salon') and user_salon.salon:
            user_salon.salon.status = 'en_attente'  # ou is_approved=False selon ton modèle
            user_salon.salon.save()

        return user_salon

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        password = validated_data.pop('password', None)

        # Mise à jour du User
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        if password:
            user.set_password(password)
        user.save()

        # Mise à jour du UserSalon
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class SalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salon
        fields = [
            'id',
            'nom',
            'logo',
            'adresse',
            'telephone',
            'email',
            'localisation',
            'max_postes',
            'date_creation',
            'status',
            'paiement_effectue',
        ]
        read_only_fields = ['status', 'paiement_effectue']