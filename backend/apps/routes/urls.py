from django.urls import path
from .views import routes

app_name = "routes"

urlpatterns = [
    path("routes/", routes, name="list"),                     # /routes/
    path("route/<uuid:route_id>/", routes, name="detail"),   # /routes/<uuid>/
]
