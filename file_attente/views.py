from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Sum, Count, Q
from decimal import Decimal
from .models import FileAttente
from salon.models import UserSalon
from salon.permissions import IsSalonActive
from .serializers import FileAttenteSerializer
from paiements.models import Paiement
from depenses.models import Depense # Assuming you have a Depense model
from paiements.serializers import PaiementSerializer

# -------------------------------
# Permissions dynamiques
# -------------------------------
class ReceptionnisteOrAdminForWork(permissions.BasePermission):
    """Autorise réceptionnistes ou admins du salon lié à la file"""
    def has_permission(self, request, view):
        # Vérifie globalement si l'utilisateur a un rôle autorisé dans au moins un salon
        return UserSalon.objects.filter(
            user=request.user, 
            role__in=['receptionniste', 'admin']
        ).exists()

    def has_object_permission(self, request, view, obj):
        # Vérifie si l'utilisateur a le rôle spécifiquement pour le salon de cet objet
        salon = obj.salon or getattr(obj.service, 'salon', None)
        if not salon:
            return False
        return UserSalon.objects.filter(
            user=request.user,
            salon=salon,
            role__in=['receptionniste', 'admin']
        ).exists()


class ReceptionnisteOrAdmin(permissions.BasePermission):
    """Autorise réceptionnistes ou admins du salon lié à la file"""
    def has_permission(self, request, view):
        # Pour la création (POST), on vérifie si l'utilisateur est admin ou réceptionniste
        # Le filtrage par salon se fait ensuite dans perform_create
        return UserSalon.objects.filter(
            user=request.user,
            role__in=['receptionniste', 'admin']
        ).exists()


# -------------------------------
# FileAttente ViewSet
# -------------------------------
class FileAttenteViewSet(viewsets.ModelViewSet):
    serializer_class = FileAttenteSerializer

    def get_permissions(self):
        if self.action in ['commencer', 'terminer']:
            permission_classes = [permissions.IsAuthenticated, IsSalonActive, ReceptionnisteOrAdminForWork]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, IsSalonActive, ReceptionnisteOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated, IsSalonActive]
        return [p() for p in permission_classes]

    def get_queryset(self):
        """Filtrer uniquement les files du salon de l'utilisateur connecté"""
        user_salon = UserSalon.objects.filter(user=self.request.user).first()
        if not user_salon:
            return FileAttente.objects.none()
        # select_related et prefetch_related suppriment les lenteurs (N+1)
        return FileAttente.objects.filter(
            salon=user_salon.salon
        ).select_related(
            'client', 'service'
        ).prefetch_related(
            'paiements'
        ).order_by('rang')

    def perform_create(self, serializer):
        """Vérifie que le service appartient au salon de l'utilisateur"""
        user_salon = UserSalon.objects.filter(user=self.request.user).first()
        if not user_salon:
            raise permissions.PermissionDenied("Impossible de créer une file sans salon")

        salon_utilisateur = user_salon.salon
        service = serializer.validated_data.get('service')
        if service.salon != salon_utilisateur:
            raise permissions.PermissionDenied("Le service doit appartenir au salon de l'utilisateur")

        serializer.save(salon=salon_utilisateur)

    # -------------------------------
    # Actions personnalisées
    # -------------------------------
    @action(detail=True, methods=['post'], url_path='commencer')
    def commencer(self, request, pk=None):
        """Marquer la file comme en cours"""
        file = self.get_object()
        file.statut = "EN_COURS"
        if not file.heure_arrivee:
            file.heure_arrivee = timezone.now()
        file.save()
        serializer = self.get_serializer(file)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Données pour le Dashboard : CA du jour et flux clients"""
        user_salon = UserSalon.objects.filter(user=request.user).first()
        if not user_salon:
            return Response({"error": "Salon non trouvé"}, status=404)

        salon = user_salon.salon
        today = timezone.now().date()

        # Stats clients en une seule agrégation
        counts = FileAttente.objects.filter(salon=salon, heure_arrivee__date=today).aggregate(
            total=Count('id'),
            en_attente=Count('id', filter=Q(statut='EN_ATTENTE')),
            en_cours=Count('id', filter=Q(statut='EN_COURS')),
            termines=Count('id', filter=Q(statut='TERMINE'))
        )

        # Stats paiements du jour (CA et volume)
        # On inclut 'EN_ATTENTE' pour que le dashboard soit cohérent avec la saisie immédiate
        paiement_stats_today = Paiement.objects.filter(
            file_attente__salon=salon,
            date_paiement__date=today,
            statut__in=['VALIDE', 'EN_ATTENTE']
        ).aggregate(
            total=Sum('montant'),
            count=Count('id')
        )
        revenue_today = paiement_stats_today['total'] or Decimal('0.00')
        count_today = paiement_stats_today['count'] or 0

        # Total CA tous les temps
        total_ca = Paiement.objects.filter(
            file_attente__salon=salon,
            statut__in=['VALIDE', 'EN_ATTENTE']
        ).aggregate(total=Sum('montant'))['total'] or Decimal('0.00')

        # Stats dépenses (du jour et total cumulé)
        depenses_today = Depense.objects.filter(
            salon=salon,
            date=today
        ).aggregate(total=Sum('montant'))['total'] or Decimal('0.00')

        depenses_total = Depense.objects.filter(
            salon=salon
        ).aggregate(total=Sum('montant'))['total'] or Decimal('0.00')

        # --- Historique des paiements (7 derniers jours) ---
        historique_paiements = []
        for i in range(7):
            d = today - timezone.timedelta(days=i)
            total = Paiement.objects.filter(
                file_attente__salon=salon,
                date_paiement__date=d,
                statut__in=['VALIDE', 'EN_ATTENTE']
            ).aggregate(t=Sum('montant'))['t'] or Decimal('0.00')
            historique_paiements.append({
                "date": d.strftime('%d/%m/%Y'),
                "total": float(total)
            })

        # --- Dernières dépenses (5 dernières) ---
        dernieres_depenses_qs = Depense.objects.filter(salon=salon).order_by('-date', '-id')[:5]
        dernieres_depenses = []
        for dep in dernieres_depenses_qs:
            dernieres_depenses.append({
                "libelle": dep.libelle,
                "categorie": dep.categorie,
                "montant": float(dep.montant),
                "date": dep.date.strftime('%d/%m/%Y') if dep.date else ""
            })

        # --- Historique de la file (10 derniers clients) ---
        histo_file_qs = FileAttente.objects.filter(salon=salon).order_by('-id')[:10]
        histo_file_data = FileAttenteSerializer(histo_file_qs, many=True).data
        historique_file = []
        for item in histo_file_data:
            historique_file.append({
                "client": f"{item.get('client_nom', '')} {item.get('client_prenom', '')}".strip(),
                "service": item.get('service_nom', ''),
                "prix": float(item.get('prix_service', 0)),
                "montant_paye": float(item['paiement_info']['montant_paye']),
                "reste": float(item['paiement_info']['reste']),
                "statut": item.get('statut', ''),
                "date": item['heure'].strftime('%d/%m/%Y') if item.get('heure') else ""
            })

        # Calcul des créances (Reste à payer total pour aujourd'hui)
        total_services_today = FileAttente.objects.filter(
            salon=salon,
            heure_arrivee__date=today
        ).aggregate(total=Sum('service__prix'))['total'] or Decimal('0.00')

        return Response({
            "clients": counts,
            "paiements": {
                "total_amount_today": revenue_today,
                "total_amount_all": total_ca,
                "count_today": count_today,
                "reste_a_payer_today": max(Decimal('0.00'), total_services_today - revenue_today)
            },
            "depenses": {
                "total_today": depenses_today,
                "total_all": depenses_total
            },
            "revenue_today": revenue_today,
            "benefice_net_today": revenue_today - depenses_today,
            "date": today,
            "historique_paiements": historique_paiements,
            "dernieres_depenses": dernieres_depenses,
            "historique_file": historique_file
        })

    @action(detail=True, methods=['post'], url_path='terminer')
    def terminer(self, request, pk=None):
        """Marquer la file comme terminée"""
        file = self.get_object()
        file.statut = "TERMINE"
        file.heure_fin = timezone.now()
        file.save()
        serializer = self.get_serializer(file)
        return Response(serializer.data, status=status.HTTP_200_OK)
