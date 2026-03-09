from django.contrib import admin
from .models import FileAttente

class AdminFile(admin.ModelAdmin):
    list_display = ('id', 'client', 'statut', 'service', 'rang')


admin.site.register(FileAttente, AdminFile)
