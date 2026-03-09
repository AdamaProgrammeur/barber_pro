from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet

app_name = 'services'

# 🔹 DRF router
router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='services')

# ⚠️ Définir d'abord urlpatterns comme liste vide
urlpatterns = []

# 🔹 Ajouter les routes générées par le router
urlpatterns += router.urls