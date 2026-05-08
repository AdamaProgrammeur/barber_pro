from django.contrib import admin
from .models import Salon, UserSalon


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'telephone', 'status', 'date_creation')
    list_filter = ('status', 'date_creation')
    search_fields = ('nom', 'email', 'telephone')
    ordering = ('nom',)


@admin.register(UserSalon)
class UserSalonAdmin(admin.ModelAdmin):
    list_display = ('user', 'salon', 'role')
    list_filter = ('role', 'salon')
    search_fields = ('user__username', 'salon__nom')
    ordering = ('user',)