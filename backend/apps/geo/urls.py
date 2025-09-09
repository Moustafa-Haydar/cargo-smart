from django.urls import path
from .views import locations

app_name = "geo"

urlpatterns = [
    path("locations/", locations, name="locations"),
]
