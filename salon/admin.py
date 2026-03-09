# admin.py
from django.contrib import admin
from .models import Salon, UserSalon

# Inline pour afficher les utilisateurs liés à un salon
class UserSalonInline(admin.TabularInline):
    model = UserSalon
    extra = 1  # nombre de lignes vides pour ajouter de nouveaux utilisateurs
    autocomplete_fields = ["user"]  # pratique si tu as beaucoup d'utilisateurs

# Admin du salon
@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ["nom", "telephone", "email", "max_postes"]
    inlines = [UserSalonInline]  # on ajoute l'inline pour gérer les utilisateurs
