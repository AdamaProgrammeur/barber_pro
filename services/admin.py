from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'salon', 'date_creation')
    list_filter = ('salon', 'date_creation')
    search_fields = ('nom', 'description')
    ordering = ('nom',)