import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ProposalsResponse } from '../../shared/models/logistics.model';
import { switchMap, tap } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ProposalsRepository {
  private http = inject(HttpClient);
  private readonly API_BASE_URL = 'http://localhost:8000';

  getProposals() {
    return this.http.get<ProposalsResponse>(`${this.API_BASE_URL}/api/agentic/proposals/`, { withCredentials: true });
  }

  acceptProposal(shipmentId: string, proposedRouteId: string) {
    console.log('Accepting proposal:', { shipmentId, proposedRouteId });

    // First get CSRF token, then make the POST request
    return this.http.get('/api/accounts/csrf/', { withCredentials: true }).pipe(
      switchMap(() => {
        const csrfToken = this.getCookie('csrftoken');
        const requestBody = { proposed_route_id: proposedRouteId };
        const requestUrl = `${this.API_BASE_URL}/api/agentic/shipments/${shipmentId}/apply/`;

        console.log('Making POST request:', {
          url: requestUrl,
          body: requestBody,
          csrfToken: csrfToken ? 'present' : 'missing'
        });

        return this.http.post(
          requestUrl,
          requestBody,
          {
            withCredentials: true,
            headers: { 'X-CSRFToken': csrfToken ?? '' }
          }
        );
      })
    );
  }

  private getCookie(name: string): string {
    const matches = document.cookie.match(
      new RegExp('(?:^|; )' + name + '=([^;]*)')
    );
    return matches ? decodeURIComponent(matches[1]) : '';
  }


}
