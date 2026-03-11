from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserSalonViewSet,
    SalonLogoView,
    SalonProfileView,
    SalonStatusView,
)

router = DefaultRouter()
router.register(r'usersalon', UserSalonViewSet, basename='usersalon')

urlpatterns = [
    path('api/', include(router.urls)),

    # Endpoints du salon
    path('api/settings/logo/', SalonLogoView.as_view(), name='salon-logo'),
    path('api/settings/profile/', SalonProfileView.as_view(), name='salon-profile'),
    path('api/settings/status/', SalonStatusView.as_view(), name='salon-status'),
]
