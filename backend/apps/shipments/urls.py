from django.urls import path
from .views import shipments

app_name = "shipments"

urlpatterns = [

    path("shipments/", shipments, name="shipments"),
    path("shipment/<uuid:shipment_id>/", shipments, name="detail"),

]
