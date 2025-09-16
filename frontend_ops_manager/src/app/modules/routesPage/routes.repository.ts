import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map, Observable, forkJoin, of, catchError } from 'rxjs';
import { Route, Shipment } from '../../shared/models/logistics.model';

interface RoutesResponse { routes: Route[]; }
interface ShipmentsResponse { shipments: Shipment[]; }

// Proposal interface to match the ML system output
export interface RouteProposal {
  action: 'stick' | 'propose_switch';
  current: {
    route_id: string;
    eta_minutes: number;
    toll_cost_usd: number;
    path: string[];
    p_delay: number;
  };
  proposal?: {
    route_id: string;
    eta_minutes: number;
    toll_cost_usd: number;
    path: string[];
    p_delay: number;
  };
  rationale: string;
  requires_approval: boolean;
}

@Injectable({ providedIn: 'root' })
export class RoutesRepository {
  private http = inject(HttpClient);

  getRoutes() {
    return this.http.get<RoutesResponse>('/api/routes/routes/', { withCredentials: true });
  }

  // Get shipments with their route proposals
  getShipmentsWithProposals() {
    return this.http.get<ShipmentsResponse>('/api/shipments/', { withCredentials: true }).pipe(
      map(response => response.shipments || [])
    );
  }

  // Get route proposal for a specific shipment (already evaluated by n8n)
  getRouteProposal(shipmentId: string): Observable<RouteProposal> {
    return this.http.get<RouteProposal>(`/api/agentic/shipments/${shipmentId}/proposal/`, { withCredentials: true });
  }

  // Apply a route proposal
  applyRouteProposal(shipmentId: string, proposal: any): Observable<any> {
    return this.http.post(`/api/agentic/shipments/${shipmentId}/apply/`, {
      proposed_route_id: proposal.route_id,
      path: proposal.path
    }, { withCredentials: true });
  }

}
