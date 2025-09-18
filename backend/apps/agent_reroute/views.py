from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import ast
import json
from apps.shipments.models import Shipment
from apps.routes.models import Route
from .decision_maker import RouteDecisionAgent
from .models import RouteProposal
from .onesignal_service import OneSignalService

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
            "shipment_id": str(shipment_id),
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
        
        # Send OneSignal notification to the driver assigned to this shipment's vehicle
        try:
            onesignal = OneSignalService()
            
            # Debug: Check shipment vehicle and driver info
            print(f"🔍 Debug - Shipment ID: {shipment_id}")
            print(f"🔍 Debug - Shipment has vehicle: {shipment.vehicle is not None}")
            if shipment.vehicle:
                print(f"🔍 Debug - Vehicle ID: {shipment.vehicle.id}")
                print(f"🔍 Debug - Vehicle has driver: {shipment.vehicle.driver is not None}")
                if shipment.vehicle.driver:
                    print(f"🔍 Debug - Driver ID: {shipment.vehicle.driver.id}")
                    print(f"🔍 Debug - Driver external_id: {shipment.vehicle.driver.external_id}")
            
            # Get the driver's external_id from the shipment's vehicle
            external_user_ids = None
            driver_info = {
                "driver_id": None,
                "driver_name": None,
                "external_id": None
            }
            
            if shipment.vehicle and shipment.vehicle.driver:
                driver_info["driver_id"] = str(shipment.vehicle.driver.id)
                driver_info["driver_name"] = f"{shipment.vehicle.driver.first_name} {shipment.vehicle.driver.last_name}".strip()
                driver_info["external_id"] = shipment.vehicle.driver.external_id
                
                if shipment.vehicle.driver.external_id:
                    external_user_ids = [shipment.vehicle.driver.external_id]
            
            # Fallback: if no driver found, you can still pass external_user_ids from request
            if not external_user_ids:
                external_user_ids = data.get("external_user_ids")
            
            notification_result = onesignal.send_route_update_notification(
                shipment_id=shipment_id,
                route_id=new_route.id,
                external_user_ids=external_user_ids
            )
            
            if notification_result["success"]:
                return JsonResponse({
                    "status": "updated", 
                    "route_id": str(new_route.id),
                    "notification_sent": True,
                    "notification_id": notification_result["data"].get("id"),
                    "driver_notified": driver_info
                })
            else:
                # Still return success for the route update, but log notification failure
                return JsonResponse({
                    "status": "updated", 
                    "route_id": str(new_route.id),
                    "notification_sent": False,
                    "notification_error": notification_result["error"],
                    "driver_info": driver_info
                })
        except Exception as notification_error:
            # Don't fail the entire request if notification fails
            return JsonResponse({
                "status": "updated", 
                "route_id": str(new_route.id),
                "notification_sent": False,
                "notification_error": str(notification_error),
                "driver_info": driver_info
            })
        
    except Exception as e:
        return JsonResponse({"detail": "Internal server error", "error": str(e)}, status=500)

@require_GET
@login_required
def get_all_proposals(request):
    """
    Get all route proposals for all shipments from database
    GET /agent_reroute/proposals/
    """
    try:
        # Get all pending proposals for all shipments
        proposals = RouteProposal.objects.filter(
            status='pending'
        ).order_by('-created_at')
        
        if not proposals.exists():
            return JsonResponse({
                "proposals": [],
                "count": 0,
                "message": "No pending proposals found"
            })
        
        # Return all proposals as array
        proposals_data = []
        for proposal in proposals:
            proposal_data = {
                "id": str(proposal.id),
                "shipment_id": str(proposal.shipment_id),
                "action": proposal.action,
                "current": {
                    "route_id": str(proposal.current_route_id) if proposal.current_route_id else None,
                    "eta_minutes": proposal.current_eta_minutes,
                    "toll_cost_usd": float(proposal.current_toll_cost_usd) if proposal.current_toll_cost_usd else None,
                    "path": proposal.current_path,
                    "p_delay": float(proposal.current_p_delay) if proposal.current_p_delay else None,
                },
                "proposal": {
                    "route_id": str(proposal.proposed_route_id) if proposal.proposed_route_id else None,
                    "eta_minutes": proposal.proposed_eta_minutes,
                    "toll_cost_usd": float(proposal.proposed_toll_cost_usd) if proposal.proposed_toll_cost_usd else None,
                    "path": proposal.proposed_path,
                    "p_delay": float(proposal.proposed_p_delay) if proposal.proposed_p_delay else None,
                } if proposal.action == "propose_switch" else None,
                "rationale": proposal.rationale,
                "requires_approval": proposal.requires_approval,
                "created_at": proposal.created_at.isoformat(),
            }
            proposals_data.append(proposal_data)
        
        return JsonResponse({
            "proposals": proposals_data,
            "count": len(proposals_data)
        })
        
    except Exception as e:
        return JsonResponse({"detail": "Internal server error", "error": str(e)}, status=500)

@require_POST
def store_all_proposals(request):
    try:
        # 1) Parse and normalize payload into a list
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"detail": "Invalid JSON"}, status=400)

        if not payload:
            return JsonResponse({"detail": "No proposals provided"}, status=400)

        proposals = []
        if isinstance(payload, dict) and "proposals" in payload:
            proposals = payload.get("proposals") or []
        elif isinstance(payload, list):
            proposals = payload
        else:
            return JsonResponse({"detail": "Expected { 'proposals': [...] } or an array"}, status=400)

        # If proposals itself is a string, try parsing JSON, then Python-literal as fallback
        if isinstance(proposals, str):
            try:
                proposals = json.loads(proposals)
            except Exception:
                try:
                    proposals = ast.literal_eval(proposals)
                except Exception:
                    return JsonResponse({"detail": "'proposals' is a string and could not be parsed"}, status=400)

        # 2) Persist proposals (flat shape expected)
        created = []
        errors = []
        for idx, item in enumerate(proposals):
            # If the item is a JSON string, try to parse it
            if isinstance(item, str):
                try:
                    item = json.loads(item)
                except Exception:
                    try:
                        item = ast.literal_eval(item)
                    except Exception:
                        errors.append({"index": idx, "error": "Proposal item is a string and could not be parsed"})
                        continue

            if not isinstance(item, dict):
                errors.append({"index": idx, "error": "Proposal is not an object"})
                continue

            shipment_id = item.get("shipment_id")
            if not shipment_id:
                errors.append({"index": idx, "error": "Missing shipment_id"})
                continue

            try:
                rp = RouteProposal.objects.create(
                    shipment_id=shipment_id,
                    action="propose_switch",

                    # current is unknown for flat payloads
                    current_route_id=None,
                    current_eta_minutes=None,
                    current_toll_cost_usd=None,
                    current_path=None,
                    current_p_delay=None,

                    # proposed route from flat fields
                    proposed_route_id=item.get("route_id"),
                    proposed_eta_minutes=item.get("eta_minutes"),
                    proposed_toll_cost_usd=item.get("toll_cost_usd"),
                    proposed_path=item.get("path"),
                    proposed_p_delay=item.get("p_delay"),

                    rationale=item.get("rationale", "Imported from n8n"),
                    requires_approval=True,
                    status='pending'
                )

                created.append({
                    "id": str(rp.id),
                    "shipment_id": str(rp.shipment_id),
                    "created_at": rp.created_at.isoformat(),
                })
            except Exception as e:
                errors.append({
                    "index": idx,
                    "shipment_id": str(shipment_id),
                    "error": str(e)
                })

        return JsonResponse({
            "status": "success",
            "proposals_created": len(created),
            "proposals": created,
            "errors": errors,
        })
    except Exception as e:
        return JsonResponse({"detail": "Internal server error", "error": str(e)}, status=500)
