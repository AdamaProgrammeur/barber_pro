from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from datetime import date, timedelta
from django.db.models import Sum, Q
from file_attente.models import FileAttente
from paiements.models import Paiement
from depenses.models import Depense
from salon.models import UserSalon
from salon.permissions import is_salon_active


class IsAdminDashboard(permissions.BasePermission):
    def has_permission(self, request, view):
        if not is_salon_active(request.user):
            return False
        return UserSalon.objects.filter(user=request.user, role='admin').exists()


class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminDashboard]

    def get(self, request):
        today = date.today()

        user_salon = UserSalon.objects.filter(user=request.user, role='admin').first()
        if not user_salon:
            return Response({"error": "Salon introuvable"}, status=status.HTTP_404_NOT_FOUND)
        salon = user_salon.salon

        # ── File d'attente ──────────────────────────────────────
        file_qs = FileAttente.objects.filter(
            Q(service__salon=salon) | Q(salon=salon)
        ).distinct()

        clients_stats = {
            "total":      file_qs.count(),
            "en_attente": file_qs.filter(statut='EN_ATTENTE').count(),
            "en_cours":   file_qs.filter(statut='EN_COURS').count(),
            "termine":    file_qs.filter(statut='TERMINE').count(),
        }

        # ── Paiements ────────────────────────────────────────────
        paiement_qs = Paiement.objects.filter(
            Q(file_attente__service__salon=salon) | Q(file_attente__salon=salon)
        ).distinct()

        p_today = paiement_qs.filter(created_at__date=today, statut='VALIDE')
        p_all   = paiement_qs.filter(statut='VALIDE')

        paiements_stats = {
            "count_today":        p_today.count(),
            "total_amount_today": p_today.aggregate(t=Sum('montant'))['t'] or 0,
            "total_amount_all":   p_all.aggregate(t=Sum('montant'))['t'] or 0,
        }

        # ── Historique paiements 7 derniers jours ────────────────
        historique_paiements = []
        for i in range(6, -1, -1):
            jour = today - timedelta(days=i)
            total = paiement_qs.filter(
                created_at__date=jour, statut='VALIDE'
            ).aggregate(t=Sum('montant'))['t'] or 0
            historique_paiements.append({
                "date":  jour.strftime('%d/%m'),
                "total": float(total),
            })

        # ── Historique file (toutes les files du salon) ──────────
        historique_file = []
        for f in file_qs.select_related('client', 'service').prefetch_related('paiements').order_by('-heure_arrivee')[:50]:
            paiement = f.paiements.filter(statut='VALIDE').first() or f.paiements.first()
            montant_paye = paiement.montant if paiement else 0
            prix         = f.service.prix if f.service else 0
            reste        = float(prix) - float(montant_paye)
            historique_file.append({
                "client":       f"{f.client.nom} {f.client.prenom}" if f.client else "-",
                "service":      f.service.nom if f.service else "-",
                "prix":         float(prix),
                "montant_paye": float(montant_paye),
                "reste":        reste,
                "statut":       f.statut,
                "date":         f.heure_arrivee.strftime('%d/%m/%Y %H:%M') if f.heure_arrivee else "-",
            })

        # ── Dépenses ─────────────────────────────────────────────
        depense_qs = Depense.objects.filter(salon=salon)
        depenses_stats = {
            "total_today": float(depense_qs.filter(date=today).aggregate(t=Sum('montant'))['t'] or 0),
            "total_all":   float(depense_qs.aggregate(t=Sum('montant'))['t'] or 0),
            "count_today": depense_qs.filter(date=today).count(),
        }
        # 5 dernières dépenses
        dernieres_depenses = list(
            depense_qs.values('libelle', 'montant', 'categorie', 'date')[:5]
        )
        for d in dernieres_depenses:
            d['montant'] = float(d['montant'])
            d['date']    = d['date'].strftime('%d/%m/%Y')

        # ── Utilisateurs ─────────────────────────────────────────
        membres = UserSalon.objects.filter(salon=salon)
        users_stats = {
            "administrateurs": membres.filter(role='admin').count(),
            "receptionnistes": membres.filter(role='receptionniste').count(),
        }

        me = membres.filter(user=request.user).first()
        user_connecte = {
            "username": request.user.username,
            "email":    request.user.email,
            "role":     me.role if me else None,
        }

        return Response({
            "clients":              clients_stats,
            "paiements":            paiements_stats,
            "historique_paiements": historique_paiements,
            "historique_file":      historique_file,
            "depenses":             depenses_stats,
            "dernieres_depenses":   dernieres_depenses,
            "users":                users_stats,
            "user_connecte":        user_connecte,
        }, status=status.HTTP_200_OK)
