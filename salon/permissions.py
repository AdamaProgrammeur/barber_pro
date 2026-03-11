# salon/permissions.py
from rest_framework import permissions
from .models import UserSalon, Salon


def is_salon_active(user):
    if not user or not user.is_authenticated:
        return False
    if getattr(user, "is_superuser", False):
        return True

    user_salon = UserSalon.objects.select_related("salon").filter(user=user).first()
    if not user_salon:
        return False

    salon = user_salon.salon
    if salon.status != Salon.STATUS_APPROVED:
        return False
    if not salon.paiement_effectue:
        return False
    return True


class IsSalonActive(permissions.BasePermission):
    message = (
        "Votre salon n'est pas encore validé par les administrateurs. "
        "Merci de patienter ou d'appeler BarbrePro au 223 78746643."
    )

    def has_permission(self, request, view):
        return is_salon_active(request.user)

# -------------------------------
# Permissions basées sur le rôle par salon
# -------------------------------

class IsAdminSalon(permissions.BasePermission):
    """
    Accès uniquement si l'utilisateur est admin dans le salon
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        salon = getattr(view, 'get_salon', lambda req: None)(request) or getattr(view, 'salon', None)
        if not salon:
            return False

        user_salon = request.user.usersalon_set.filter(salon=salon).first()
        return user_salon and user_salon.role == 'admin'


class IsCoiffeurSalon(permissions.BasePermission):
    """
    Compatibilité: accès "coiffeur" basculé vers réceptionniste
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        salon = getattr(view, 'get_salon', lambda req: None)(request) or getattr(view, 'salon', None)
        if not salon:
            return False

        user_salon = request.user.usersalon_set.filter(salon=salon).first()
        return user_salon and user_salon.role == 'receptionniste'


class IsReceptionnisteSalon(permissions.BasePermission):
    """
    Accès uniquement si l'utilisateur est réceptionniste dans le salon
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        salon = getattr(view, 'get_salon', lambda req: None)(request) or getattr(view, 'salon', None)
        if not salon:
            return False

        user_salon = request.user.usersalon_set.filter(salon=salon).first()
        return user_salon and user_salon.role == 'receptionniste'


# -------------------------------
# Permissions combinées lecture seule
# -------------------------------

class AdminOrReadOnlySalon(permissions.BasePermission):
    """
    Admin peut tout faire, les autres utilisateurs peuvent seulement lire
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        salon = getattr(view, 'get_salon', lambda req: None)(request) or getattr(view, 'salon', None)
        if not salon:
            return False

        user_salon = request.user.usersalon_set.filter(salon=salon).first()
        return user_salon and user_salon.role == 'admin'


class CoiffeurOrReadOnlySalon(permissions.BasePermission):
    """
    Compatibilité: règles "coiffeur" basculées vers réceptionniste
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        salon = getattr(view, 'get_salon', lambda req: None)(request) or getattr(view, 'salon', None)
        if not salon:
            return False

        user_salon = request.user.usersalon_set.filter(salon=salon).first()
        return user_salon and user_salon.role == 'receptionniste'


class ReceptionnisteOrReadOnlySalon(permissions.BasePermission):
    """
    Réceptionniste peut gérer clients et file d'attente, les autres peuvent seulement lire
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        salon = getattr(view, 'get_salon', lambda req: None)(request) or getattr(view, 'salon', None)
        if not salon:
            return False

        user_salon = request.user.usersalon_set.filter(salon=salon).first()
        return user_salon and user_salon.role == 'receptionniste'
