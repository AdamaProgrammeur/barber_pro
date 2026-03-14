from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils import timezone
from django.db.models import Sum
from django.db.models import Q
from file_attente.models import FileAttente
from paiements.models import Paiement
from salon.models import UserSalon
from salon.permissions import is_salon_active

# ---------------------------
# Permission : admin salon
# ---------------------------
class IsAdminDashboard(permissions.BasePermission):
    """Autorise uniquement l'admin du salon à accéder au dashboard."""
    def has_permission(self, request, view):
        if not is_salon_active(request.user):
            return False
        return UserSalon.objects.filter(user=request.user, role='admin').exists()

# ---------------------------
# DashboardView
# ---------------------------
class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminDashboard]

    def get_salon(self, request):
        """
        Récupère le salon de l'utilisateur connecté.
        Si c'est un admin global, on prend le premier salon associé.
        """
        user_salon = UserSalon.objects.filter(user=request.user, role='admin').first()
        if user_salon:
            return user_salon.salon
        return None

    def get(self, request):
        today = timezone.localtime(timezone.now()).date()
        salon = self.get_salon(request)

        if not salon:
            return Response({"error": "Salon introuvable"}, status=status.HTTP_404_NOT_FOUND)

        # -----------------------
        # Stats file d'attente
        # -----------------------
        file_qs = FileAttente.objects.filter(
            Q(salon=salon) | Q(service__salon=salon)
        ).distinct()
        clients_stats = {
            "total": file_qs.count(),
            "en_attente": file_qs.filter(statut__iexact="EN_ATTENTE").count(),
            "en_cours": file_qs.filter(statut__iexact="EN_COURS").count(),
            "termine": file_qs.filter(statut__iexact="TERMINE").count(),
        }

        # -----------------------
        # Paiements aujourd'hui et total
        # -----------------------
        paiement_base_qs = Paiement.objects.filter(
            Q(file_attente__salon=salon) | Q(file_attente__service__salon=salon)
        ).distinct()
        paiements_today = paiement_base_qs.filter(
            created_at__date=today,
            statut__iexact="VALIDE"
        )
        paiements_total = paiement_base_qs.filter(statut__iexact="VALIDE")
        paiements_stats = {
            "count_today": paiements_today.count(),
            "total_amount_today": paiements_today.aggregate(total=Sum("montant"))["total"] or 0,
            "total_amount_all": paiements_total.aggregate(total=Sum("montant"))["total"] or 0
        }

        # -----------------------
        # Stats utilisateurs
        # -----------------------
        users_salon = UserSalon.objects.filter(salon=salon)
        users_stats = {
            "receptionnistes": users_salon.filter(role='receptionniste').count(),
            "administrateurs": users_salon.filter(role='admin').count(),
        }

        # -----------------------
        # Utilisateur connecté
        # -----------------------
        user_salon_relation = users_salon.filter(user=request.user).first()
        user_connecte = {
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "role_salon": user_salon_relation.role if user_salon_relation else None,
        }

        return Response({
            "clients": clients_stats,
            "paiements": paiements_stats,
            "users": users_stats,
            "user_connecte": user_connecte
        }, status=status.HTTP_200_OK)
