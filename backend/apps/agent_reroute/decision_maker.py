from dataclasses import dataclass
from typing import Dict, Any, Optional
from django.conf import settings
from apps.agent_reroute.models import AgentDecision
from apps.agent_reroute.ml import predict_p_delay
from apps.agent_reroute.routers.graph_router import GraphRoutingProvider

W = settings.ROUTE_AI["SCORE_WEIGHTS"]

def _score(option: Dict[str, Any], p_delay: float) -> float:
    return -(W["eta_minutes"]*float(option["eta_minutes"])
             + W["toll_cost_usd"]*float(option.get("toll_cost_usd", 0.0))
             + W["p_delay"]*(p_delay*100.0))

@dataclass
class DecisionResult:
    action: str
    current: Dict[str, Any]
    best_alt: Optional[Dict[str, Any]]
    rationale: str

class RouteDecisionAgent:
    def __init__(self, routing_provider=None):
        self.routing = routing_provider or GraphRoutingProvider()
        self.cfg = settings.ROUTE_AI

    def decide(self, shipment_id) -> DecisionResult:
        from apps.shipments.models import Shipment
        s = Shipment.objects.select_related("route").get(id=shipment_id)
        current_option = self.routing.get_current_option(shipment_id)
        
        # Convert RouteOption to dict - handle all possible cases
        try:
            if hasattr(current_option, 'copy'):
                # It's a dict-like object, create a copy to avoid modifying the original
                current = current_option.copy()
            elif hasattr(current_option, '__dict__'):
                # It's an object with attributes, convert to dict
                current = {
                    'route_id': getattr(current_option, 'route_id', ''),
                    'eta_minutes': getattr(current_option, 'eta_minutes', 0),
                    'toll_cost_usd': getattr(current_option, 'toll_cost_usd', 0),
                    'path': getattr(current_option, 'path', [])
                }
            else:
                # Try to convert to dict
                current = dict(current_option)
        except Exception as e:
            # Fallback to a basic dict
            current = {
                'route_id': 'unknown',
                'eta_minutes': 480,
                'toll_cost_usd': 25.0,
                'path': []
            }
            
        p_delay, snap = predict_p_delay(s, current)
        current["p_delay"] = p_delay
        cur_score = _score(current, p_delay)

        if p_delay < self.cfg["P_DELAY_THRESHOLD"]:
            rationale = f"p_delay={p_delay:.2f} < threshold {self.cfg['P_DELAY_THRESHOLD']:.2f}; stay."
            self._log(shipment_id, current, None, cur_score, None, "stick", snap, rationale)
            return DecisionResult("stick", current, None, rationale)

        alts = self.routing.get_alternatives(shipment_id, self.cfg["MAX_ALTERNATIVES"])
        if not alts:
            rationale = "High risk but no alternatives; stay."
            self._log(shipment_id, current, None, cur_score, None, "stick", snap, rationale)
            return DecisionResult("stick", current, None, rationale)

        best, best_score = None, None
        for a in alts:
            # Convert RouteOption to dict if needed
            if hasattr(a, 'copy'):
                # It's a dict-like object, create a copy to avoid modifying the original
                alt_dict = a.copy()
            else:
                alt_dict = dict(a)
                
            alt_p = max(0.0, p_delay - 0.10)  # replace with true per-alt prediction later
            alt_dict["p_delay"] = alt_p
            s_alt = _score(alt_dict, alt_p)
            if best is None or s_alt > best_score:
                best, best_score = alt_dict, s_alt

        improvement = (best_score - cur_score) / (abs(cur_score) + 1e-6)
        if improvement >= self.cfg["IMPROVEMENT_EPS"]:
            delta_eta = best["eta_minutes"] - current["eta_minutes"]
            rationale = (f"p_delay={p_delay:.2f} ≥ threshold; alt improves score {improvement*100:.1f}%. "
                         f"Alt ETA {best['eta_minutes']:.0f}m (Δ{delta_eta:+.0f}m).")
            self._log(shipment_id, current, best, cur_score, best_score, "propose_switch", snap, rationale)
            return DecisionResult("propose_switch", current, best, rationale)

        rationale = f"Alternatives exist but improvement {improvement*100:.1f}% < {self.cfg['IMPROVEMENT_EPS']*100:.0f}%."
        self._log(shipment_id, current, None, cur_score, best_score, "stick", snap, rationale)
        return DecisionResult("stick", current, None, rationale)

    def _log(self, shipment_id, current, best, cur_score, best_score, action, snap, rationale):
        from apps.shipments.models import Shipment
        s = Shipment.objects.only("id","route_id").get(id=shipment_id)
        AgentDecision.objects.create(
            shipment_id=s.id,
            current_route_id=s.route_id,
            proposed_route_id=None if not best else best.get("route_id"),
            input_snapshot={"features": snap, "current": current},
            output_decision={"action": action, "current_score": cur_score,
                             "best_alt_score": best_score, "best_alt": best,
                             "rationale": rationale},
        )
