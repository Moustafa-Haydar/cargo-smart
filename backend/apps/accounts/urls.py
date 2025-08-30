from django.urls import path
from . import views

urlpatterns = [

    path("csrf/", views.csrf, name="csrf"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("me/", views.me, name="me"),

    path("users/", views.create_user, name="create_user"),    

]
