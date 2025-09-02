from django.urls import path
from .views import login, logout, csrf, me, create_user, users, update_user, delete_user

urlpatterns = [

    # auth - (public endpoints)
    path("csrf/", csrf, name="csrf"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("me/", me, name="me"),

    # user management - (admin only)
    path("users/", users, name="users"),
    path("users/create/", create_user, name="create_user"),
    path("users/update/", update_user, name="update_user"),
    path("users/delete/", delete_user, name="delete_user")

]
