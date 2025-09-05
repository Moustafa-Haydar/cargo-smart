from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Prefetch

from .models import Vehicle, VehicleIdentifier, VehiclePosition, PortCall


def _serialize_vehicle(v: Vehicle) -> dict:
    # positions are prefetched ordered by -recorded_at (newest first)
    pos_list = list(v.positions.all())[:10]
    last_pos = pos_list[0] if pos_list else None

    # port calls are prefetched ordered by -scheduled_at / -actual_at (newest first)
    calls = list(v.port_calls.all())[:10]

    return {
        "id": str(v.id),
        "name": v.name,
        "type": v.type,
        "status": v.status,

        "imo": v.imo,
        "mmsi": v.mmsi,
        "call_sign": v.call_sign,
        "flag": v.flag,

        "current_location": (
            {"id": v.current_location_id, "name": v.current_location.name}
            if v.current_location_id else None
        ),
        "route": ({"id": v.route_id, "name": v.route.name} if v.route_id else None),

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
                "location": last_pos.location.name if last_pos.location_id else None,
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
                "location": p.location.name if p.location_id else None,
            }
            for p in pos_list
        ],

        "port_calls": [
            {
                "id": str(pc.id),
                "voyage": pc.voyage,
                "event": pc.event,                 # ARRIVAL/DEPARTURE/BERTH...
                "label": pc.label,
                "scheduled_at": pc.scheduled_at.isoformat() if pc.scheduled_at else None,
                "actual_at": pc.actual_at.isoformat() if pc.actual_at else None,
                "status": pc.status,
                "source_ref": pc.source_ref,
                "port_location": {
                    "id": pc.port_location_id,
                    "name": pc.port_location.name,
                },
                "facility": (
                    {"id": pc.facility_id, "name": pc.facility.name}
                    if pc.facility_id else None
                ),
            }
            for pc in calls
        ],
    }


@require_GET
def vehicles(request, vehicle_id=None):
    """
    GET /vehicles/                 -> all vehicles
    GET /vehicles/<uuid:vehicle_id>/  -> specific vehicle by UUID
    """
    qs = (
        Vehicle.objects
        .select_related("current_location", "route")
        .prefetch_related(
            Prefetch("identifiers", queryset=VehicleIdentifier.objects.all()),
            Prefetch(
                "positions",
                queryset=VehiclePosition.objects.select_related("location")
                                                .order_by("-recorded_at")
            ),
            Prefetch(
                "port_calls",
                queryset=PortCall.objects.select_related("port_location", "facility")
                                         .order_by("-scheduled_at", "-actual_at")
            ),
        )
    )

    if vehicle_id is not None:
        qs = qs.filter(id=vehicle_id)
        if not qs.exists():
            return JsonResponse({"detail": "Vehicle not found"}, status=404)
        return JsonResponse({"vehicles": [_serialize_vehicle(qs.first())]})

    return JsonResponse({"vehicles": [_serialize_vehicle(v) for v in qs]})

