from django.urls import path
from .views import (
    home_page,
    crud_clients_page,
    dashbord_view,
    gestion_users_page,
    modifier_client,
    supprimer_client,
    crud_paiement_page,
    crud_service_page,
    list_service_page,
    logout_page,
    login_page,
    profile_page,
    crud_file_page,
    gestion_file,
    setting,
    register_salon_page,
    en_attente_page,
    depenses_page,
)

urlpatterns = [
    path('', home_page, name='home_page'),

    path("gestion-users/", gestion_users_page, name="gestion_users"),
    path('accounts/login/', login_page, name='login_page'),
    path('accounts/register-salon/', register_salon_page, name='register_salon_page'),
    path('logout/', logout_page, name='logout_page'),
    path('profile/', profile_page, name='profile_page'),

    path('dashboard/', dashbord_view, name='dashboard_view'),

    path('crud_client_page/', crud_clients_page, name='crud_client_page'),

    path('crud_service_page/', crud_service_page, name='crud_service_page'),
    path('list_service_page/', list_service_page, name='list_service'),
    

    path('crud_file_page/', crud_file_page, name='crud_file_page'),
    path('gestion_file/', gestion_file, name='gestion_file'),
    path('gestion_users/', gestion_users_page, name='gestion_users'),

    path('crud_paiement_page/', crud_paiement_page, name='crud_paiement_page'),

    path('setting/', setting, name='setting'),
    path('en-attente/', en_attente_page, name='en_attente_page'),
    path('depenses/', depenses_page, name='depenses_page'),
]
