from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Prefetch
from .models import Vehicle, VehicleIdentifier, VehiclePosition
from apps.rbac.authz import require_read, require_set


def _serialize_vehicle(v: Vehicle) -> dict:
    # positions are prefetched ordered by -recorded_at (newest first)
    pos_list = list(v.positions.all())[:10]
    last_pos = pos_list[0] if pos_list else None

    return {
        "id": str(v.id),
        "plate_number": v.plate_number,
        "model": v.model,
        "status": v.status,

        "current_location": (
            {"id": str(v.current_location.id), "name": v.current_location.name}
            if v.current_location else None
        ),

        "identifiers": [
            {"scheme": ident.scheme, "value": ident.value}
            for ident in v.identifiers.all()
        ],

        "last_position": (
            {
                "recorded_at": last_pos.recorded_at.isoformat(),
                "lat": last_pos.lat,
                "lng": last_pos.lng,
                "source": last_pos.source,
                "location": last_pos.location.name if last_pos.location else None,
            }
            if last_pos else None
        ),

        "positions": [
            {
                "id": str(p.id),
                "recorded_at": p.recorded_at.isoformat(),
                "lat": p.lat,
                "lng": p.lng,
                "source": p.source,
                "location": p.location.name if p.location else None,
            }
            for p in pos_list
        ],
    }


@require_GET
# @require_read("vehicles")  # Temporarily disabled for testing
def vehicles(request, vehicle_id=None):
    """
    GET /vehicles/vehicles/                 -> all vehicles
    GET /vehicles/vehicle/<uuid:vehicle_id>/  -> specific vehicle by UUID
    """
    try:
        qs = (
            Vehicle.objects
            .select_related("current_location")
            .prefetch_related(
                Prefetch("identifiers", queryset=VehicleIdentifier.objects.all()),
                Prefetch(
                    "positions",
                    queryset=VehiclePosition.objects.select_related("location")
                                                    .order_by("-recorded_at")
                ),
            )
        )

        if vehicle_id is not None:
            try:
                vehicle = qs.get(id=vehicle_id)
                return JsonResponse({"vehicles": [_serialize_vehicle(vehicle)]})
            except Vehicle.DoesNotExist:
                return JsonResponse({"detail": "Vehicle not found"}, status=404)
            except ValueError:
                return JsonResponse({"detail": "Invalid vehicle ID format"}, status=400)

        vehicles_list = list(qs.all())
        return JsonResponse({"vehicles": [_serialize_vehicle(v) for v in vehicles_list]})
    except Exception as e:
        return JsonResponse({"detail": "Internal server error", "error": str(e)}, status=500)

