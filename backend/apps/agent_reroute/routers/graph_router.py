from typing import Dict, List
from apps.shipments.models import Shipment
from apps.routes.models import Route, RouteSegment
from .base import RoutingProvider, RouteOption
import random
import uuid

class GraphRoutingProvider(RoutingProvider):
    """
    Simplified routing provider that works with the current model structure.
    This is a basic implementation that provides mock alternatives for testing.
    """
    
    def get_current_option(self, shipment_id) -> RouteOption:
        """Get the current route option for a shipment"""
        s = Shipment.objects.select_related("route").get(id=shipment_id)
        r: Route = s.route
        
        # Calculate ETA from route segments if available
        eta_minutes = 480  # Default 8 hours
        toll_cost = 25.0   # Default toll cost
        
        # Try to get ETA from route segments
        segments = r.segments.all().order_by('seq')
        if segments.exists():
            # Calculate total ETA from segments (simplified)
            eta_minutes = len(segments) * 60  # 1 hour per segment as approximation
        
        # Create a simple path representation
        path = [f"node_{i}" for i in range(len(segments) + 1)]
        
        return RouteOption({
            "route_id": str(r.id), 
            "eta_minutes": float(eta_minutes), 
            "toll_cost_usd": toll_cost, 
            "path": path
        })

    def get_alternatives(self, shipment_id, max_k: int) -> List[RouteOption]:
        """Get alternative route options for a shipment"""
        s = Shipment.objects.select_related("route").get(id=shipment_id)
        current = self.get_current_option(shipment_id)
        
        # Generate mock alternatives for testing
        alts: List[RouteOption] = []
        
        for i in range(max_k):
            # Create alternative routes with slightly different ETAs and costs
            alt_eta = current["eta_minutes"] + random.randint(-60, 120)  # ±1-2 hours
            alt_toll = current["toll_cost_usd"] + random.randint(-10, 20)  # ±$10-20
            alt_path = [f"alt_node_{j}" for j in range(len(current["path"]))]
            
            alts.append(RouteOption({
                "route_id": str(uuid.uuid4()),  # Generate proper UUID
                "eta_minutes": max(60, alt_eta),  # Minimum 1 hour
                "toll_cost_usd": max(0, alt_toll),  # Minimum $0
                "path": alt_path
            }))
        
        return alts
