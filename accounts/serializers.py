from django.db import transaction
from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from salon.models import Salon, UserSalon

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if not password:
            raise serializers.ValidationError({"password": "Le mot de passe est obligatoire."})
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'username'

    def validate(self, attrs):
        data = super().validate(attrs)
        # role depuis UserSalon sera ajouté dans la vue login
        data['user'] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
        }
        return data


class ProfileSerializer(serializers.ModelSerializer):
    nom_complet = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'nom_complet', 'is_admin']

    def get_nom_complet(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def get_is_admin(self, obj):
        return obj.is_superuser


class RegisterSalonSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)

    salon_nom = serializers.CharField(max_length=150)
    salon_adresse = serializers.CharField(required=False, allow_blank=True)
    salon_telephone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    salon_email = serializers.EmailField(required=False, allow_blank=True)
    salon_localisation = serializers.URLField(required=False, allow_blank=True)
    max_postes = serializers.IntegerField(required=False, min_value=1, default=1)

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "Les mots de passe ne correspondent pas."}
            )

        if User.objects.filter(username=attrs["username"]).exists():
            raise serializers.ValidationError({"username": "Ce nom d'utilisateur existe déjà."})

        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError({"email": "Cet email est déjà utilisé."})

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop("password_confirm")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )

        salon = Salon.objects.create(
            nom=validated_data["salon_nom"],
            adresse=validated_data.get("salon_adresse", ""),
            telephone=validated_data.get("salon_telephone", ""),
            email=validated_data.get("salon_email", ""),
            localisation=validated_data.get("salon_localisation", ""),
            max_postes=validated_data.get("max_postes", 1),
        )

        UserSalon.objects.create(user=user, salon=salon, role="admin")
        return user, salon
