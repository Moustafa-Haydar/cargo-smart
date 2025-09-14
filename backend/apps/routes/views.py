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
                "geometry": seg.geometry,
                "eta_start": seg.eta_start.isoformat() if seg.eta_start else None,
                "eta_end": seg.eta_end.isoformat() if seg.eta_end else None,
            }
            for seg in r.segments.all()
        ],
        # minimal info to avoid heavy joins - only include if relationships exist
        "shipments": [
            {
                "id": str(s.id),
                "ref_no": getattr(s, 'ref_no', None),
                "status": getattr(s, 'status', None),
                "carrier_name": getattr(s, 'carrier_name', None),
                "origin_id": getattr(s, 'origin_id', None),
                "destination_id": getattr(s, 'destination_id', None),
                "scheduled_at": s.scheduled_at.isoformat() if getattr(s, 'scheduled_at', None) else None,
                "vehicle": {
                    "id": str(s.vehicle.id),
                    "plate_number": s.vehicle.plate_number,
                    "model": s.vehicle.model,
                    "status": s.vehicle.status,
                } if getattr(s, 'vehicle', None) else None,
            }
            for s in getattr(r, 'shipments', []).all()
        ] if hasattr(r, 'shipments') else [],
        "vehicles": [
            {
                "id": str(v.id),
                "plate_number": getattr(v, 'plate_number', None),
                "model": getattr(v, 'model', None),
                "status": getattr(v, 'status', None),
            }
            for v in getattr(r, 'vehicles', []).all()
        ] if hasattr(r, 'vehicles') else [],
    }


@require_GET
def routes(request, route_id=None):
    """
    GET /routes/routes/          -> all routes
    GET /routes/route/<uuid:route_id>/ -> specific route by UUID
    """
    try:
        # Build base queryset with segments prefetch
        qs = Route.objects.prefetch_related(
            Prefetch("segments", queryset=RouteSegment.objects.order_by("seq"))
        )
        
        # Only add shipments and vehicles prefetch if the relationships exist
        # This prevents errors if the relationships haven't been defined yet
        try:
            qs = qs.prefetch_related(
                Prefetch("shipments", queryset=Shipment.objects.select_related("vehicle").only("id", "ref_no", "status", "carrier_name", "origin_id", "destination_id", "scheduled_at", "vehicle_id")),
                Prefetch("vehicles", queryset=Vehicle.objects.only("id", "plate_number", "model", "status")),
            )
        except Exception:
            # If relationships don't exist, continue without them
            pass

        if route_id is not None:
            try:
                route = qs.get(id=route_id)
                return JsonResponse({"routes": [_serialize_route(route)]})
            except Route.DoesNotExist:
                return JsonResponse({"detail": "Route not found"}, status=404)
            except ValueError:
                return JsonResponse({"detail": "Invalid route ID format"}, status=400)

        # Return all routes
        routes_list = list(qs.all())
        return JsonResponse({"routes": [_serialize_route(r) for r in routes_list]})
        
    except Exception as e:
        return JsonResponse({"detail": "Internal server error", "error": str(e)}, status=500)
