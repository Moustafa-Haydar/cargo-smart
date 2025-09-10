import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map, Observable } from 'rxjs';
import { TransportVehicle } from '../../shared/models/logistics.model';

interface VehiclesResponse { vehicles: TransportVehicle[]; }

@Injectable({ providedIn: 'root' })
export class VehicleRepository {
  private http = inject(HttpClient);

  getVehicles() {
    return this.http.get<VehiclesResponse>('/api/vehicles/vehicles/', { withCredentials: true });
  }

}
