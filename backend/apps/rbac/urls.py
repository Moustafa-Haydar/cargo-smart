from django.urls import path
from . import views

urlpatterns = [

    # Role management
    path("roles/", views.roles, name="roles"),
    path("addRole/", views.create_role, name="create_role"),
    path("deleteRole/", views.delete_role, name="delete_role"),
    path("updateRole/", views.update_role, name="update_role"),

    # Permission management
    path("permissions/", views.permissions, name="permissions"),
    path("addPermission/", views.add_permission, name="add_permission"),
    # List all permissions for specific role, and update the permissions
    path("roles/<int:role_id>/permissions/", views.role_permissions, name="role_permissions"),
    
    
]