from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Prefetch
from .models import Route, RouteSegment
from apps.shipments.models import Shipment
from apps.vehicles.models import Vehicle
from apps.rbac.authz import require_read, require_set


def _serialize_route(r: Route) -> dict:
    return {
        "id": str(r.id),
        "name": r.name,
        "geometry": r.geometry,
        "segments": [
            {
                "id": str(seg.id),
                "seq": seg.seq,
                "route_type": seg.route_type,
                "geometry": seg.geometry,
                "mode": seg.mode,
                "eta_start": seg.eta_start.isoformat() if seg.eta_start else None,
                "eta_end": seg.eta_end.isoformat() if seg.eta_end else None,
            }
            for seg in r.segments.all()
        ],
        # minimal info to avoid heavy joins
        "shipments": [
            {
                "id": str(s.id),
                "ref_no": s.ref_no,
                "status": s.status,
                "shipment_type": s.shipment_type,
                "origin_id": s.origin_id,
                "destination_id": s.destination_id,
            }
            for s in r.shipments.all()
        ],
        "vehicles": [
            {
                "id": str(v.id),
                "name": v.name,
                "type": v.type,
                "status": v.status,
            }
            for v in r.vehicles.all()
        ],
    }


@require_GET
@require_GET("routes")
def routes(request, route_id=None):
    """
    GET /routes/routes/          -> all routes
    GET /routes/route/<uuid:route_id>/ -> specific route by UUID
    """
    qs = (
        Route.objects
        .prefetch_related(
            Prefetch("segments", queryset=RouteSegment.objects.order_by("seq")),
            Prefetch("shipments", queryset=Shipment.objects.only("id", "ref_no", "status", "shipment_type", "origin_id", "destination_id")),
            Prefetch("vehicles", queryset=Vehicle.objects.only("id", "name", "type", "status")),
        )
    )

    if route_id is not None:
        qs = qs.filter(id=route_id)
        if not qs.exists():
            return JsonResponse({"detail": "Route not found"}, status=404)
        return JsonResponse({"routes": [_serialize_route(qs.first())]})

    return JsonResponse({"routes": [_serialize_route(r) for r in qs]})
