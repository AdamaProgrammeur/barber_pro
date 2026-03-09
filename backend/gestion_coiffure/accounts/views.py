from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.conf import settings
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer, MyTokenObtainPairSerializer, RegisterSalonSerializer
from salon.models import Salon, UserSalon
from clients.models import Client
from services.models import Service
from .permissions import IsAdmin

# JWT Token
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Login
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if user is not None:
        serializer = MyTokenObtainPairSerializer(data={"username": username, "password": password})
        serializer.is_valid(raise_exception=True)
        token_data = serializer.validated_data

        # Récupérer le rôle
        try:
            usersalon = UserSalon.objects.get(user=user)
            role = usersalon.role
        except UserSalon.DoesNotExist:
            role = None

        token_data['user']['role'] = role
        return Response(token_data)

    return Response({"error": "Invalid credentials"}, status=400)


# Logout
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    return Response({"message": "Logout réussi"})


# Profile API pour /api/profile/
class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            usersalon = UserSalon.objects.get(user=request.user)
            role = usersalon.role
        except UserSalon.DoesNotExist:
            role = None

        return Response({
            "username": request.user.username,
            "email": request.user.email,
            "role": role
        })

    def patch(self, request):
        email = request.data.get("email", "").strip()
        nom_complet = request.data.get("nom_complet", "").strip()

        if email:
            request.user.email = email

        if nom_complet:
            parts = nom_complet.split()
            request.user.first_name = parts[0]
            request.user.last_name = " ".join(parts[1:]) if len(parts) > 1 else ""

        request.user.save()
        return Response({
            "username": request.user.username,
            "email": request.user.email,
            "role": UserSalon.objects.filter(user=request.user).first().role if UserSalon.objects.filter(user=request.user).exists() else None
        })


# UserViewSet pour /api/users/
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # ou IsAdmin si restreindre aux admins


class RegisterSalonAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSalonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, salon = serializer.save()

        refresh = RefreshToken.for_user(user)
        try:
            role = UserSalon.objects.get(user=user, salon=salon).role
        except UserSalon.DoesNotExist:
            role = None

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": role,
                },
                "salon": {
                    "id": salon.id,
                    "nom": salon.nom,
                },
            },
            status=201,
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def demo_login_view(request):
    if not getattr(settings, "DEMO_LOGIN_ENABLED", False):
        return Response({"error": "Le mode démo est désactivé."}, status=403)

    demo_username = getattr(settings, "DEMO_USERNAME", "demo_salon")
    demo_password = getattr(settings, "DEMO_PASSWORD", "demo123456")
    demo_email = getattr(settings, "DEMO_EMAIL", "demo@salon.local")
    demo_salon_name = getattr(settings, "DEMO_SALON_NAME", "Salon Demo")

    with transaction.atomic():
        user, created = User.objects.get_or_create(
            username=demo_username,
            defaults={
                "email": demo_email,
                "first_name": "Compte",
                "last_name": "Demo",
            },
        )

        if created:
            user.set_password(demo_password)
            user.save(update_fields=["password"])
        elif not user.check_password(demo_password):
            user.set_password(demo_password)
            user.save(update_fields=["password"])

        salon = Salon.objects.filter(nom=demo_salon_name).order_by("id").first()
        if not salon:
            salon = Salon.objects.create(
                nom=demo_salon_name,
                adresse="Mode test uniquement",
                max_postes=3,
            )

        user_salon, _ = UserSalon.objects.get_or_create(
            user=user,
            salon=salon,
            defaults={"role": "admin"},
        )
        if user_salon.role != "admin":
            user_salon.role = "admin"
            user_salon.save(update_fields=["role"])

        Service.objects.get_or_create(
            salon=salon,
            nom="Coupe demo",
            defaults={"prix": "5000.00"},
        )
        Client.objects.get_or_create(
            salon=salon,
            nom="Client",
            prenom="Demo",
            defaults={"telephone": "70000000", "adresse": "Mode test"},
        )

    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": "admin",
            },
            "salon": {
                "id": salon.id,
                "nom": salon.nom,
            },
            "demo": True,
        }
    )
