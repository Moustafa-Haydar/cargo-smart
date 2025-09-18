from django.urls import path
from .views import login, logout, csrf, me, create_user, users, update_user, delete_user
from .views.mobile_views import mobile_login, mobile_logout, mobile_profile

app_name = "accounts"

urlpatterns = [

    # auth - (public endpoints)
    path("csrf/", csrf, name="csrf"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("me/", me, name="me"),

    # user management - (admin only)
    path("users/", users, name="users"),
    path("user/<uuid:id>/", users, name="user"),
    path("users/create/", create_user, name="create_user"),
    path("users/update/", update_user, name="update_user"),
    path("users/delete/", delete_user, name="delete_user"),

    # --- Mobile API (token auth) ---
    path("mobile/login/", mobile_login, name="mobile_login"),
    path("mobile/logout/", mobile_logout, name="mobile_logout"),
    path("mobile/profile/", mobile_profile, name="mobile_profile"),

    # --- n8n (token auth) ---
    path("n8n/login/", mobile_login, name="mobile_login"),

]
