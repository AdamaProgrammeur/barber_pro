# urls.py
# file_attente/urls.py
from rest_framework.routers import DefaultRouter
from .views import FileAttenteViewSet

router = DefaultRouter()
router.register(r'file_attente', FileAttenteViewSet, basename='file_attente')

urlpatterns = router.urls
'''Avec cette configuration :

Action	URL	Méthode
Commencer	/file_attente/<pk>/commencer/	POST
Terminer	/file_attente/<pk>/terminer/	POST
CRUD	/file_attente/	GET, POST
Détails	/file_attente/<pk>/	GET, PUT, PATCH, DELETE

Le <pk> correspond à l’ID du client dans la file d’attente.
'''