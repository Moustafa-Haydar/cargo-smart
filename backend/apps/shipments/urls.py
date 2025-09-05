from django.urls import path
from .views import shipments_list_simple

app_name = "shipments"

urlpatterns = [

    path("shipments/", shipments_list_simple, name="shipments-list-simple"),

]
