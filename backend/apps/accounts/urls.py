from django.urls import path
from . import views

urlpatterns = [

    path("csrf/", views.csrf, name="csrf"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("me/", views.me, name="me"),

    # user management - (admin only)
    # to add all user related endpoints here
    # add, update, delete, list users
    path("addUser/", views.create_user, name="create_user"),    


]
