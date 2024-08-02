from .views import authenticate_user
from django.urls import path

urlpatterns = [
    
    path("login/", authenticate_user, name="authenticate_user"),
    
]