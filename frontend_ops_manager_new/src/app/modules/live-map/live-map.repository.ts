import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { GeoLocation } from '../../shared/models/logistics.model';

interface GeoLocationResponse { locations: GeoLocation[]; }

@Injectable({ providedIn: 'root' })
export class LocationRepository {
  private http = inject(HttpClient);

  getLocations() {
    return this.http.get<GeoLocationResponse>('/api/geo/locations/', { withCredentials: true });
  }

}
