from django.shortcuts import render
from django.contrib.auth import logout
from django.conf import settings


def home_page(request):
    return render(
        request,
        "layout/accueil.html",
        {"demo_login_enabled": getattr(settings, "DEMO_LOGIN_ENABLED", False)},
    )


def login_page(request):
    return render(
        request,
        "accounts/login.html",
        {"demo_login_enabled": getattr(settings, "DEMO_LOGIN_ENABLED", False)},
    )

def logout_page(request):
    logout(request)
    return render(request, "accounts/login.html")

def gestion_users_page(request):
    return render(request, "gestion_users/gestion_users.html")

def profile_page(request):
    return render(request, "accounts/profile.html")


def register_salon_page(request):
    return render(request, "accounts/register_salon.html")


def dashbord_view(request):
    return render(request, "dashboard/dashboard.html", {
    
    })

def crud_clients_page(request):
    return render(request, "clients/crud_client.html")

def modifier_client(request, id):
    pass

def supprimer_client(request, id):
    pass

def crud_service_page(request):
    return render(request, "services/crud_service.html")
def list_service_page(request):
    return render(request, "services/list_service.html")

def crud_file_page(request):
    return render(request, "file/crud_file.html")


def gestion_file(request):
    return render(request, "file/gestion_file.html")
def crud_paiement_page(request):
    return render(request, "paiements/crud_paiement.html")


def setting(request):
    return render(request, "accounts/setting.html")


def en_attente_page(request):
    return render(request, "accounts/en_attente.html")


def depenses_page(request):
    return render(request, "depenses/crud_depense.html")
