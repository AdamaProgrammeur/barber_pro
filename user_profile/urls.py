# accounts/urls.py
from django.urls import path
from .views import ProfileViewSet

profile_list = ProfileViewSet.as_view({
    "get": "list",
    "patch": "partial_update",
})

urlpatterns = [
    path("profile_api/", profile_list, name="profile_api"),
]
