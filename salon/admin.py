from django.contrib import admin
from .models import Salon, UserSalon

class UserSalonInline(admin.TabularInline):
    model = UserSalon
    extra = 1  # nombre de lignes vides pour ajouter de nouveaux utilisateurs
    # autocomplete_fields est désactivé pour éviter l'erreur 500 
    # tant que UserAdmin n'a pas de search_fields

# Admin du salon
@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ["nom", "telephone", "email", "max_postes", "status", "paiement_effectue"]
    list_filter = ["status", "paiement_effectue"]
    actions = ["approve_salons", "reject_salons", "mark_paid", "mark_unpaid"]
    inlines = [UserSalonInline]

    @admin.action(description="Approuver les salons sélectionnés")
    def approve_salons(self, request, queryset):
        queryset.update(status=Salon.STATUS_APPROVED)

    @admin.action(description="Refuser les salons sélectionnés")
    def reject_salons(self, request, queryset):
        queryset.update(status=Salon.STATUS_REJECTED)

    @admin.action(description="Marquer paiement effectué")
    def mark_paid(self, request, queryset):
        queryset.update(paiement_effectue=True)

    @admin.action(description="Marquer paiement non effectué")
    def mark_unpaid(self, request, queryset):
        queryset.update(paiement_effectue=False)
