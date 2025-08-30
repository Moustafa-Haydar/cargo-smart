from django.urls import path
from . import views

urlpatterns = [

    path("addRole/", views.create_role, name="create_role"),
       

]