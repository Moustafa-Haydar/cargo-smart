from django.urls import path
from .views import vehicles

app_name = "vehicles"

urlpatterns = [
    path("vehicles/", vehicles, name="list"),
    path("vehicle/<uuid:vehicle_id>/", vehicles, name="detail")
]
