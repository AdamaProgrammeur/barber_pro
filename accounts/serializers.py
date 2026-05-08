from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from salon.models import Salon, UserSalon

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
        }
        return data


class RegisterSalonSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    salon_nom = serializers.CharField(max_length=150)
    salon_adresse = serializers.CharField(required=False, allow_blank=True)
    salon_telephone = serializers.CharField(required=False, allow_blank=True)
    salon_email = serializers.EmailField(required=False, allow_blank=True)
    salon_localisation = serializers.URLField(required=False, allow_blank=True)
    max_postes = serializers.IntegerField(default=1)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Ce nom d’utilisateur est déjà utilisé.')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Cette adresse e-mail est déjà utilisée.')
        return value

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({'password_confirm': 'Les mots de passe ne correspondent pas.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=password,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )

        salon = Salon.objects.create(
            nom=validated_data['salon_nom'],
            adresse=validated_data.get('salon_adresse', ''),
            telephone=validated_data.get('salon_telephone', ''),
            email=validated_data.get('salon_email', ''),
            localisation=validated_data.get('salon_localisation', ''),
            max_postes=validated_data.get('max_postes', 1),
            status=Salon.STATUS_APPROVED,
            paiement_effectue=False,
        )
        UserSalon.objects.create(user=user, salon=salon, role='admin')
        return user, salon

    def save(self, **kwargs):
        return self.create(self.validated_data)
