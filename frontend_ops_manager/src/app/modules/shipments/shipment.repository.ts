import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map, Observable } from 'rxjs';
import { Shipment } from '../../shared/models/logistics.model';
import { API_BASE_URL } from '../../app.config.server';

interface ShipmentsResponse {
  shipments: Shipment[];
}

@Injectable({ providedIn: 'root' })
export class ShipmentRepository {
  private http = inject(HttpClient);
  private base = `${API_BASE_URL}/shipments/shipments`;

  getShipments(): Observable<Shipment[]> {
    // Your backend list endpoint looked like /shipments/shipments/
    return this.http.get<ShipmentsResponse>(`${this.base}/shipments/`)
      .pipe(map(res => res.shipments)); // map if your API wraps the array
    // If the API already returns Shipment[] directly, just:
    // return this.http.get<Shipment[]>(`${this.base}/shipments/`);
  }

  getShipmentById(id: string): Observable<Shipment> {
    return this.http.get<Shipment>(`${this.base}/shipment/${id}/`);
  }
}
