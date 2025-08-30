from django.urls import path
from . import views

urlpatterns = [

    # to add all role related endpoints here
    # add, update, delete, list roles
    path("addRole/", views.create_role, name="create_role"),
       

]