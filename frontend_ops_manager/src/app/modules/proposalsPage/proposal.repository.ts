import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ProposalsResponse } from '../../shared/models/logistics.model';

@Injectable({ providedIn: 'root' })
export class ProposalsRepository {
  private http = inject(HttpClient);

  getProposals() {
    return this.http.get<ProposalsResponse>('/api/agentic/proposals/', { withCredentials: true });
  }
}
