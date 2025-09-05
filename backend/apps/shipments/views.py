from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Prefetch
from .models import Shipment, ShipmentMilestone, ShipmentVehicle, ShipmentContainer
from apps.rbac.authz import require_read

MILESTONE_WEIGHTS = {
    "PREPOL": 25,
    "POL": 50,
    "POD": 75,
    "POSTPOD": 90,   # <100 so "Delivered" can be 100
}

def _simple_progress(shipment: Shipment) -> int:
    if shipment.delivered_at:
        return 100
    reached = 0
    for m in shipment.milestones.all():
        if m.actual:
            reached = max(reached, MILESTONE_WEIGHTS.get(m.kind, 0))
    return reached

def _serialize_shipment(s: Shipment) -> dict:
    return {
        "id": str(s.id),
        "ref_no": s.ref_no,
        "shipment_type": s.shipment_type,
        "status": s.status,
        "carrier_code": s.carrier_code,
        "carrier_name": s.carrier_name,

        "origin": {"id": s.origin_id, "name": s.origin.name},
        "destination": {"id": s.destination_id, "name": s.destination.name},
        "current_location": (
            {"id": s.current_location_id, "name": s.current_location.name}
            if s.current_location_id else None
        ),

        "scheduled_at": s.scheduled_at.isoformat(),
        "delivered_at": s.delivered_at.isoformat() if s.delivered_at else None,

        "route": ({"id": s.route_id, "name": s.route.name} if s.route_id else None),

        "milestones": [
            {
                "id": str(m.id),
                "kind": m.kind,
                "date": m.date.isoformat() if m.date else None,
                "actual": m.actual,
                "predictive_eta": m.predictive_eta.isoformat() if m.predictive_eta else None,
                "location": m.location.name,
            }
            for m in s.milestones.all()
        ],

        "vehicles": [
            {
                "id": str(sv.vehicle.id),
                "name": sv.vehicle.name,
                "voyage": sv.voyage,
                "role": sv.role,
            }
            for sv in s.shipment_vehicles.all()
        ],

        "containers": [
            {
                "id": str(sc.container.id),
                "number": sc.container.number,
                "status": sc.container.status,
            }
            for sc in s.shipment_containers.all()
        ],

        "progress_pct": _simple_progress(s),
    }

@require_GET
@require_read("shipments")
def shipments(request, shipment_id=None):
    """
    GET /shipments/shipments/                 -> all shipments
    GET /shipments/shipment/<uuid:shipment_id>/      -> specific shipment by UUID
    """
    qs = (
        Shipment.objects
        .select_related("origin", "destination", "current_location", "route")
        .prefetch_related(
            Prefetch(
                "milestones",
                queryset=ShipmentMilestone.objects.select_related("location").order_by("date")
            ),
            Prefetch("shipment_vehicles", queryset=ShipmentVehicle.objects.select_related("vehicle")),
            Prefetch("shipment_containers", queryset=ShipmentContainer.objects.select_related("container")),
        )
    )

    if shipment_id is not None:
        qs = qs.filter(id=shipment_id)
        if not qs.exists():
            return JsonResponse({"detail": "Shipment not found"}, status=404)

    return JsonResponse({"shipments": [_serialize_shipment(s) for s in qs]})
