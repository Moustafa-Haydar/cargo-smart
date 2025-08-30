from django.urls import path
from . import views

urlpatterns = [

    # to add all role related endpoints here
    path("roles/", views.roles, name="roles"),
    path("addRole/", views.create_role, name="create_role"),
    path("deleteRole/", views.delete_role, name="delete_role"),
    

]