from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserSalon, Salon

User = get_user_model()

class UserSalonSerializer(serializers.ModelSerializer):
    username   = serializers.CharField(source='user.username', required=False)
    email      = serializers.EmailField(source='user.email', required=False)
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name  = serializers.CharField(source='user.last_name', required=False)
    password   = serializers.CharField(write_only=True, required=False)

    class Meta:
        model  = UserSalon
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'salon', 'password']
        extra_kwargs = {'salon': {'read_only': True}}

    def validate(self, attrs):
        user_data = attrs.get('user', {})
        username  = user_data.get('username')

        if username:
            # En modification, exclure l'utilisateur courant
            qs = User.objects.filter(username=username)
            if self.instance:
                qs = qs.exclude(pk=self.instance.user.pk)
            if qs.exists():
                raise serializers.ValidationError({"username": "Ce nom d'utilisateur existe déjà."})

        email = user_data.get('email')
        if email:
            qs = User.objects.filter(email=email)
            if self.instance:
                qs = qs.exclude(pk=self.instance.user.pk)
            if qs.exists():
                raise serializers.ValidationError({"email": "Cet email est déjà utilisé."})

        return attrs

    def create(self, validated_data):
        user_data = validated_data.pop('user', {})
        password  = validated_data.pop('password', None)
        if not password:
            raise serializers.ValidationError({"password": "Le mot de passe est obligatoire."})

        user = User.objects.create(
            username   = user_data.get('username'),
            email      = user_data.get('email', ''),
            first_name = user_data.get('first_name', ''),
            last_name  = user_data.get('last_name', ''),
        )
        user.set_password(password)
        user.save()

        return UserSalon.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        password  = validated_data.pop('password', None)

        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        if password:
            user.set_password(password)
        user.save()

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