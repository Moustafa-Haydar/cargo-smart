import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map, Observable } from 'rxjs';
import { Shipment } from '../../shared/models/logistics.model';

interface ShipmentsResponse { shipments: Shipment[]; }

@Injectable({ providedIn: 'root' })
export class ShipmentRepository {
  private http = inject(HttpClient);

  getShipments() {
    return this.http.get<ShipmentsResponse>('/api/shipments/shipments/', { withCredentials: true });
  }
}
