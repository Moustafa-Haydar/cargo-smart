// import { Injectable } from '@angular/core';
// import { HttpClient, HttpErrorResponse } from '@angular/common/http';
// import { Observable, throwError } from 'rxjs';
// import { catchError, map } from 'rxjs/operators';
// import { Shipment, ShipmentsResponse, ShipmentDisplayData, ShipmentStatus } from '../models/shipments.model';

// @Injectable({
//     providedIn: 'root'
// })
// export class ShipmentsService {
//     private baseURL = 'http://localhost:8000';

//     constructor(private http: HttpClient) { }

//     /**
//      * Fetch all shipments from the API
//      */
//     // returns display-ready rows
//     getShipments$(): Observable<DisplayShipment[]> {
//         return this.http
//             .get<ShipmentsResponse>(`${this.baseURL}/shipments/shipments`)
//             .pipe(
//             map(res => res.shipments.map(s => this.transformShipmentForDisplay(s)))
//             );
//     }



//     /**
//      * Transform raw shipment data to display format
//      */
//     transformShipmentForDisplay(shipment: Shipment): ShipmentDisplayData {
//         const status = this.mapStatusToDisplay(shipment.status);
//         const deliveryDate = shipment.delivered_at;

//         return {
//             id: shipment.id,
//             ref_no: shipment.ref_no,
//             type: shipment.shipment_type,
//             origin: shipment.origin.name,
//             destination: shipment.destination.name,
//             status: status,
//             eta: "",
//             // deliveryDate: deliveryDate,
//             carrier_name: shipment.carrier_name,
//             current_location: shipment.current_location.name,
//             originalStatus: shipment.status // Keep original status for counting
//         };
//     }

//     private mapStatusToDisplay(status: string): ShipmentStatus {
//         switch (status) {
//             case 'DELIVERED':
//                 return { status: 'Delivered', percentage: 100 };
//             case 'IN_TRANSIT':
//                 return { status: 'In-Transit', percentage: 75 };
//             case 'CREATED':
//                 return { status: 'In-Transit', percentage: 25 };
//             default:
//                 return { status: 'Delayed', percentage: 50 };
//         }
//     }

// }
