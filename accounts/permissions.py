from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
# -------------------------------
# Permissions basées sur le rôle
# -------------------------------

class IsAdmin(permissions.BasePermission):
    """
    Accès uniquement pour l'Admin (propriétaire)
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'


