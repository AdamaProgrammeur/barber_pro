# salon/permissions.py
from rest_framework import permissions

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
