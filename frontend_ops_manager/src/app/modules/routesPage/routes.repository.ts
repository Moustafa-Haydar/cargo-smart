import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map, Observable } from 'rxjs';
import { Route } from '../../shared/models/logistics.model';

interface RoutesResponse { routes: Route[]; }

@Injectable({ providedIn: 'root' })
export class RoutesRepository {
  private http = inject(HttpClient);

  getRoutes() {
    return this.http.get<RoutesResponse>('/api/routes/routes/', { withCredentials: true });
  }
}
