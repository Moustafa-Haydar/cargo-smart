from django.urls import path
from . import views

urlpatterns = [

    # to add all role related endpoints here
    # add, update, delete, list roles
    path("roles/", views.roles, name="create_role"),
    path("addRole/", views.create_role, name="create_role"),
    

]