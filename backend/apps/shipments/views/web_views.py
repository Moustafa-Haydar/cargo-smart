from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.db.models import Prefetch
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from apps.routes.models import Route
from apps.rbac.authz import require_read, require_set
from ..models import Shipment, ShipmentMilestone
import json


def _serialize_shipment(s: Shipment) -> dict:
    return {
        "id": str(s.id),
        "ref_no": s.ref_no,
        "shipment_type": s.shipment_type,
        "status": s.status,
        "carrier_code": s.carrier_code,
        "carrier_name": s.carrier_name,
        "api_updated_at": s.api_updated_at.isoformat() if s.api_updated_at else None,

        "origin": {
            "id": str(s.origin.id),
            "name": s.origin.name
        } if s.origin else None,

        "destination": {
            "id": str(s.destination.id),
            "name": s.destination.name
        } if s.destination else None,

        "current_location": {
            "id": str(s.current_location.id),
            "name": s.current_location.name
        } if s.current_location else None,

        "route": {
            "id": str(s.route.id),
            "name": s.route.name
        } if s.route else None,

        "driver": {
            "id": str(s.driver.id),
            "name": f"{s.driver.first_name} {s.driver.last_name}"
        } if s.driver else None,

        "scheduled_at": s.scheduled_at.isoformat() if s.scheduled_at else None,
        "delivered_at": s.delivered_at.isoformat() if s.delivered_at else None,

        "milestones": [{
            "id": str(m.id),
            "kind": m.kind,
            "location": {
                "id": str(m.location.id),
                "name": m.location.name
            },
            "date": m.date.isoformat(),
            "actual": m.actual,
            "predictive_eta": m.predictive_eta.isoformat() if m.predictive_eta else None
        } for m in s.milestones.all()],

        "vehicles": [{
            "id": str(sv.id),
            "vehicle": {
                "id": str(sv.vehicle.id),
                "name": sv.vehicle.name
            },
            "voyage": sv.voyage,
            "role": sv.role
        } for sv in s.shipment_vehicles.all()],

        "containers": [{
            "id": str(sc.id),
            "container": {
                "id": str(sc.container.id),
                "number": sc.container.number
            },
            "is_active": sc.is_active,
            "loaded_at": sc.loaded_at.isoformat() if sc.loaded_at else None,
            "discharged_at": sc.discharged_at.isoformat() if sc.discharged_at else None
        } for sc in s.shipment_containers.all()]
    }


@require_GET
@require_read("shipments")
def shipments(request, shipment_id=None):
    """
    GET /shipments/                    -> all shipments
    GET /shipment/<uuid:shipment_id>/  -> specific shipment by UUID
    """
    qs = (
        Shipment.objects
        .select_related(
            "origin",
            "destination",
            "current_location",
            "route",
            "driver"
        )
        .prefetch_related(
            Prefetch(
                "milestones",
                queryset=ShipmentMilestone.objects.select_related("location")
            ),
            Prefetch(
                "shipment_vehicles",
                queryset=ShipmentVehicle.objects.select_related("vehicle")
            ),
            Prefetch(
                "shipment_containers",
                queryset=ShipmentContainer.objects.select_related("container")
            )
        )
    )

    if shipment_id is not None:
        qs = qs.filter(id=shipment_id)
        if not qs.exists():
            return JsonResponse({"detail": "Shipment not found"}, status=404)
        return JsonResponse({"shipments": [_serialize_shipment(qs.first())]})

    return JsonResponse({"shipments": [_serialize_shipment(s) for s in qs]})



# @permission_classes([IsAuthenticated])
@require_POST
def change_shipment_route(request, shipment_id):
    """
    Change the route of a shipment
    """

    try:
        # Get the shipment
        shipment = get_object_or_404(Shipment, id=shipment_id)
        
        # Get route_id from request data
        data = json.loads(request.body.decode() or "{}")
        route_id = (data.get("route_id") or "").strip()
        if not route_id:
            return JsonResponse(
                {'error': 'route_id is required'}, 
                status=400
            )

        # Get and validate the new route
        try:
            new_route = Route.objects.get(id=route_id)
        except Route.DoesNotExist:
            return JsonResponse(
                {'error': 'Route not found'}, 
                status=404
            )

        # Update the shipment's route
        shipment.route = new_route
        shipment.save()

        return JsonResponse({
            'message': 'Route updated successfully',
            'shipment_id': str(shipment.id),
            'new_route_id': str(new_route.id)
        })

    except Exception as e:
        return JsonResponse(
            {'error': str(e)}, status=500)
