from rest_framework import permissions
from salon.models import UserSalon
from salon.permissions import is_salon_active

class IsAdminDashboard(permissions.BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False
        if not is_salon_active(request.user):
            return False

        user_salon = UserSalon.objects.filter(user=request.user).first()

        if not user_salon:
            return False

        return user_salon.role == "admin"
