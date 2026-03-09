from rest_framework import serializers
from .models import UserSalon
from .models import Salon
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSalonSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=False)
    email = serializers.EmailField(source='user.email', read_only=False)
    first_name = serializers.CharField(source='user.first_name', read_only=False)
    last_name = serializers.CharField(source='user.last_name', read_only=False)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = UserSalon
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'salon', 'password']
        extra_kwargs = {
            'salon': {'read_only': True},  # on l'attribue automatiquement
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user', {})
        password = validated_data.pop('password', None)

        # Création du User
        user = User.objects.create(
            username=user_data.get('username'),
            email=user_data.get('email'),
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name')
        )
        if password:
            user.set_password(password)
            user.save()

        # Création du UserSalon
        user_salon = UserSalon.objects.create(user=user, **validated_data)
        return user_salon

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        password = validated_data.pop('password', None)

        # Update User
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        if password:
            user.set_password(password)
        user.save()

        # Update UserSalon
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

class SalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salon
        fields = ['id', 'nom', 'logo', 'adresse', 'telephone', 'email', 'localisation', 'max_postes', 'date_creation']
