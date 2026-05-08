from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prenom', 'telephone', 'salon')
    search_fields = ('nom', 'prenom', 'telephone')
    list_filter = ('salon',)
