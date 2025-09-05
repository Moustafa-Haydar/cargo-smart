from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Prefetch
from .models import (
    Shipment,
    ShipmentMilestone,
    ShipmentVehicle,
    ShipmentContainer,
)

@require_GET
def shipments_list_simple(request):
    """
    GET /api/shipments/
    Returns ALL shipments with minimal nested info:
    - route (id, name)
    - milestones (kind, date, actual, predictive_eta, location name)
    - vehicles (id, name, voyage, role)
    - containers (id, number, status)
    """
    qs = (
        Shipment.objects
        .select_related("origin", "destination", "current_location", "route")
        .prefetch_related(
            Prefetch(
                "milestones",
                queryset=ShipmentMilestone.objects.select_related("location").order_by("date"),
            ),
            Prefetch(
                "shipment_vehicles",
                queryset=ShipmentVehicle.objects.select_related("vehicle"),
            ),
            Prefetch(
                "shipment_containers",
                queryset=ShipmentContainer.objects.select_related("container"),
            ),
        )
    )

    results = []
    for s in qs:
        results.append({
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

            "route": (
                {"id": s.route_id, "name": s.route.name} if s.route_id else None
            ),

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

            # Vehicles linked to this shipment
            "vehicles": [
                {
                    "id": str(sv.vehicle.id),
                    "name": sv.vehicle.name,
                    "voyage": sv.voyage,
                    "role": sv.role,
                }
                for sv in s.shipment_vehicles.all()
            ],

            # Containers linked to this shipment
            "containers": [
                {
                    "id": str(sc.container.id),
                    "number": sc.container.number,
                    "status": sc.container.status,
                }
                for sc in s.shipment_containers.all()
            ],
        })

    return JsonResponse({"results": results})
