from django.urls import path
from . import views

urlpatterns = [

    path("/api/csrf/", views.csrf, name="csrf"),
    path("/api/login/", views.login, name="login"),
    path("/api/logout/", views.logout, name="logout"),
    path("/api/me/", views.me, name="me"),
    
]
