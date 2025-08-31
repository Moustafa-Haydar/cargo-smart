from django.urls import path
from .views import groups, create_group, update_group, delete_group, permissions, add_permission, group_permissions

urlpatterns = [

    # Group management
    path("groups/", groups, name="groups"),
    path("groups/create/", create_group, name="create_group"),
    path("groups/update/", update_group, name="update_group"),
    path("groups/delete/", delete_group, name="delete_group"),

    # Permission management
    path("permissions/", permissions, name="permissions"),
    path("addPermission/", add_permission, name="add_permission"),
    # List all permissions for specific group, and update the permissions
    path("groups/<int:group_id>/permissions/", group_permissions, name="group_permissions"),
    
    
]