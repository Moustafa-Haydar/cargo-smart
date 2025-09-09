import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map, Observable } from 'rxjs';
import { Shipment } from '../../shared/models/logistics.model';

interface ShipmentsResponse { shipments: Shipment[]; }

@Injectable({ providedIn: 'root' })
export class ShipmentRepository {
  private http = inject(HttpClient);

  getShipments(): Observable<Shipment[]> {
    return this.http
      .get<ShipmentsResponse>('/shipments/shipments/', { withCredentials: true })
      .pipe(
        map(res => res.shipments ?? [])
      );
  }

  getShipmentById(id: string): Observable<Shipment> {
    return this.http.get<Shipment>(`/shipments/shipment/${id}/`, { withCredentials: true });
  }
}
