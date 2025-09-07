from django.urls import path
from .views.web_views import shipments, change_shipment_route
from .views.mobile_views import (
    driver_shipments, 
    driver_shipment_detail, 
    mark_shipment_delivered, 
    update_shipment_status
)

app_name = "shipments"

urlpatterns = [
    # Web API endpoints
    path("shipments/", shipments, name="shipments"),
    path("shipment/<uuid:shipment_id>/", shipments, name="detail"),
    path("shipment/<uuid:shipment_id>/change-route/", change_shipment_route, name="change_route"),
    
    # Mobile API endpoints (token auth required)
    path("mobile/driver/shipments/", driver_shipments, name="driver_shipments"),
    path("mobile/driver/shipment/<uuid:shipment_id>/", driver_shipment_detail, name="driver_shipment_detail"),
    path("mobile/driver/shipment/<uuid:shipment_id>/delivered/", mark_shipment_delivered, name="mark_delivered"),
    path("mobile/driver/shipment/<uuid:shipment_id>/status/", update_shipment_status, name="update_status"),
]