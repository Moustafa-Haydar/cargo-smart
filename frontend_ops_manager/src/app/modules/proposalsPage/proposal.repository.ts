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
    return this.http.get('/api/accounts/csrf/', { withCredentials: true }).pipe(
              switchMap(() => {
                  const csrfToken = this.getCookie('csrftoken');
                  return this.http.post(
                    `${this.API_BASE_URL}/api/agentic/shipments/${shipmentId}/apply/`,
                    { proposed_route_id: proposedRouteId },
                    { 
                      withCredentials: true,
                      headers: { 'X-CSRFToken': csrfToken ?? '' }
                     }
                  );
              }),
              tap(res => {
                  console.log('Login repository response:', res);
                  if ((res as any)?.ok === true && (res as any)?.user) {
                    localStorage.setItem('user', JSON.stringify((res as any).user));
                    localStorage.setItem('isAuthenticated', 'true');
                  }
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
