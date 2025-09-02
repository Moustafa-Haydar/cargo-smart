from django.urls import path
from .views import groups, create_group, update_group, delete_group, permissions, create_permission, group_permissions, update_permission, delete_permission

app_name = "rbac"

urlpatterns = [

    # Group management
    path("groups/", groups, name="groups"),
    path("group/<uuid:id>/", groups, name="group"),
    path("groups/create/", create_group, name="create_group"),
    path("groups/update/", update_group, name="update_group"),
    path("groups/delete/", delete_group, name="delete_group"),

    # Permission management
    path("permissions/", permissions, name="permissions"),
    path("permission/<uuid:id>/", permissions, name="permission"),
    path("permissions/create/", create_permission, name="create_permission"),
    path("permissions/update/", update_permission, name="update_permission"),
    path("permissions/delete/", delete_permission, name="delete_permission"),

    # Group Permissions management
    # List all permissions for specific group, and update the permissions
    path("groups/<uuid:group_id>/permissions/", group_permissions, name="group_permissions"),
    
    
]