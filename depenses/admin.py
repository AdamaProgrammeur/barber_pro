from django.contrib import admin
from .models import Depense


@admin.register(Depense)
class DepenseAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'montant', 'categorie', 'date', 'salon')
    list_filter = ('categorie', 'date', 'salon')
    search_fields = ('libelle', 'note')
    ordering = ('-date',)