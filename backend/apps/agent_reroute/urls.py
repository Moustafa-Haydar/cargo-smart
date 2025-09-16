from django.urls import path
from .api import evaluate_route, apply_proposal

urlpatterns = [
    path("shipments/<uuid:shipment_id>/evaluate/", evaluate_route),
    path("shipments/<uuid:shipment_id>/apply/", apply_proposal),
]
