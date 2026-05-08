from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views

app_name = 'accounts'

api_urls = [
    path('profile/', views.ProfileAPIView.as_view(), name='profile'),
    path('register_salon/', views.RegisterSalonAPIView.as_view(), name='register_salon'),
    path('register-salon/', views.RegisterSalonAPIView.as_view(), name='register_salon_hyphen'),
    path('demo_login/', views.demo_login_view, name='demo_login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api/', include((api_urls, 'api'), namespace='api')),
]
