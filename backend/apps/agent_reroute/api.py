from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
from apps.shipments.models import Shipment
from apps.routes.models import Route
from .decision_maker import RouteDecisionAgent

@require_POST
@csrf_protect
@login_required
def evaluate_route(request, shipment_id):
    """
    Evaluate route for a shipment and return decision
    POST /agent_reroute/shipments/<uuid:shipment_id>/evaluate/
    """
    try:
        result = RouteDecisionAgent().decide(shipment_id)
        return JsonResponse({
            "action": result.action,
            "current": result.current,
            "proposal": result.best_alt,
            "rationale": result.rationale,
            "requires_approval": result.action == "propose_switch",
        })
    except Exception as e:
        return JsonResponse({"detail": "Internal server error", "error": str(e)}, status=500)

@require_POST
@csrf_protect
@login_required
def apply_proposal(request, shipment_id):
    """
    Apply a route proposal to a shipment
    POST /agent_reroute/shipments/<uuid:shipment_id>/apply/
    """
    try:
        shipment = get_object_or_404(Shipment, id=shipment_id)
        
        # Parse JSON data from request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"detail": "Invalid JSON"}, status=400)
        
        proposed_route_id = data.get("proposed_route_id")
        path = data.get("path")

        # Always create a new route for alternatives since they don't exist in DB
        import uuid
        if proposed_route_id:
            # Use the proposed_route_id as the new route ID
            new_route = Route.objects.create(
                id=proposed_route_id,
                name=f"Alternative Route {uuid.uuid4().hex[:8]}",
                geometry=f"Alternative route for shipment {shipment_id}"
            )
        elif path:
            # Create a new route with the given path
            new_route = Route.objects.create(
                id=uuid.uuid4(),
                name=f"Alternative Route {uuid.uuid4().hex[:8]}",
                geometry=str(path)  # Store path as string in geometry field
            )
        else:
            return JsonResponse({"detail": "Missing proposed_route_id or path"}, status=400)

        shipment.route = new_route
        shipment.save(update_fields=["route"])
        return JsonResponse({"status": "updated", "route_id": str(new_route.id)})
        
    except Exception as e:
        return JsonResponse({"detail": "Internal server error", "error": str(e)}, status=500)
