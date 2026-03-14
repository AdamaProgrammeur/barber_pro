from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    login_view,
    logout_view,
    MyTokenObtainPairView,
    ProfileAPIView,
    RegisterSalonAPIView,
    demo_login_view,
)
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'accounts'

# Router DRF pour /api/users/
router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

# Pages classiques
web_urlpatterns = [
    path('login/', login_view, name='login_page'),
    path('logout/', logout_view, name='logout_page'),
]

# Endpoints REST
api_urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('demo-login/', demo_login_view, name='demo_login'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('register-salon/', RegisterSalonAPIView.as_view(), name='register_salon'),
    path('', include(router.urls)),  # → /users/, /users/{pk}/
]

# URLs finales
urlpatterns = web_urlpatterns + [
    path('api/', include((api_urlpatterns, app_name), namespace='api')),
]
