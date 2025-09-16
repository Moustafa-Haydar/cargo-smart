from abc import ABC, abstractmethod
from typing import List, Dict, Any

class RouteOption(dict):
    """keys: route_id, eta_minutes, toll_cost_usd (opt), path (opt), p_delay (opt)"""
    pass

class RoutingProvider(ABC):
    @abstractmethod
    def get_current_option(self, shipment_id) -> RouteOption: ...
    @abstractmethod
    def get_alternatives(self, shipment_id, max_k: int) -> List[RouteOption]: ...
