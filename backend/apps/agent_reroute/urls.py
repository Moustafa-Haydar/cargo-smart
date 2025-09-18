from django.urls import path
from .views import evaluate_route, apply_proposal, get_all_proposals, store_all_proposals

urlpatterns = [
    path("shipments/<uuid:shipment_id>/evaluate/", evaluate_route),
    path("shipments/<uuid:shipment_id>/apply/", apply_proposal),
    path("proposals/", get_all_proposals),  # GET all proposals
    path("proposals/store/", store_all_proposals),  # POST all proposals from n8n
]
