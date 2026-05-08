from rest_framework import serializers
from .models import Salon, UserSalon
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSalonSerializer(serializers.ModelSerializer):
    # Champs à plat pour le frontend
    username = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = UserSalon
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'password']
        read_only_fields = ['salon']

    def to_representation(self, instance):
        """Aplatit les données de l'utilisateur pour le frontend"""
        ret = super().to_representation(instance)
        user = instance.user
        ret['username'] = user.username
        ret['first_name'] = user.first_name
        ret['last_name'] = user.last_name
        ret['email'] = user.email
        return ret

    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        password = validated_data.pop('password', None)
        role = validated_data.pop('role')
        salon = validated_data.pop('salon')

        # Créer ou récupérer l'utilisateur
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'first_name': first_name, 'last_name': last_name}
        )
        
        if created and password:
            user.set_password(password)
            user.save()

        # ✅ Correction : Utiliser update_or_create pour éviter les doublons accidentels
        user_salon, _ = UserSalon.objects.update_or_create(
            user=user, salon=salon, defaults={'role': role}
        )
        return user_salon

    def update(self, instance, validated_data):
        # Mise à jour des infos de l'utilisateur lié
        user = instance.user
        user.username = validated_data.get('username', user.username)
        user.email = validated_data.get('email', user.email)
        user.first_name = validated_data.get('first_name', user.first_name)
        user.last_name = validated_data.get('last_name', user.last_name)
        
        password = validated_data.get('password')
        if password:
            user.set_password(password)
        user.save()

        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance


class SalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salon
        fields = ['id', 'nom', 'logo', 'adresse', 'telephone', 'email', 'localisation', 'max_postes', 'status', 'paiement_effectue']
        read_only_fields = ['status', 'paiement_effectue']
