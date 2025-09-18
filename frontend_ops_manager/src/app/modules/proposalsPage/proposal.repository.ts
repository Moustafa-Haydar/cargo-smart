import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ProposalsResponse } from '../../shared/models/logistics.model';

@Injectable({ providedIn: 'root' })
export class ProposalsRepository {
  private http = inject(HttpClient);
  private readonly API_BASE_URL = 'http://localhost:8000';

  getProposals() {
    return this.http.get<ProposalsResponse>(`${this.API_BASE_URL}/api/agentic/proposals/`, { withCredentials: true });
  }

  acceptProposal(shipmentId: string, proposedRouteId: string) {
    return this.http.post(
      `${this.API_BASE_URL}/api/agentic/shipments/${shipmentId}/apply/`,
      { proposed_route_id: proposedRouteId },
      { withCredentials: true }
    );
  }
}
