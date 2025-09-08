// import { Injectable } from '@angular/core';
// import { BehaviorSubject, Observable, of } from 'rxjs';
// import { catchError, finalize, tap } from 'rxjs/operators';
// import { ShipmentsService } from './shipments.service';

// @Injectable({
//     providedIn: 'root'
// })
// export class ShipmentsController {
//     private shipmentsSubject = new BehaviorSubject<ShipmentDisplayData[]>([]);
//     private loadingSubject = new BehaviorSubject<boolean>(false);
//     private errorSubject = new BehaviorSubject<string | null>(null);

//     public shipments$ = this.shipmentsSubject.asObservable();
//     public loading$ = this.loadingSubject.asObservable();
//     public error$ = this.errorSubject.asObservable();

//     constructor(private shipmentsService: ShipmentsService) { }

//     /**
//      * Load all shipments from the API
//      */

//     ngOnInit(): void {
//         this.setLoading(true);
//         this.clearError();
//         // if you want, you can control loading via finalize:
//         this.shipments$ = this.shipmentsService.getShipments$().pipe(
//             finalize(() => this.setLoading(false)),
//             catchError(err => {
//             this.setError('Failed to load shipments. Please try again.');
//             console.error('Error loading shipments:', err);
//             return of([] as DisplayShipment[]);
//             })
//         );
//         }


//     /**
//      * Search shipments by query
//      */
//     searchShipments(query: string): void {

//         return;
//         // const currentShipments = this.shipmentsSubject.value;

//         // if (!query.trim()) {
//         //     // If query is empty, reload all shipments
//         //     this.loadShipments();
//         //     return;
//         // }

//         // const filteredShipments = currentShipments.filter(shipment =>
//         //     shipment.ref_no.toLowerCase().includes(query.toLowerCase()) ||
//         //     shipment.origin.toLowerCase().includes(query.toLowerCase()) ||
//         //     shipment.destination.toLowerCase().includes(query.toLowerCase()) ||
//         //     shipment.type.toLowerCase().includes(query.toLowerCase()) ||
//         //     shipment.carrier_name.toLowerCase().includes(query.toLowerCase())
//         // );

//         // this.shipmentsSubject.next(filteredShipments);
//     }

//     /**
//      * Filter shipments by status
//      */
//     filterByStatus(status: string): void {

//         return;
//         // const currentShipments = this.shipmentsSubject.value;

//         // if (status === 'ALL') {
//         //     this.loadShipments();
//         //     return;
//         // }

//         // const filteredShipments = currentShipments.filter(shipment =>
//         //     shipment.status.status === status
//         // );

//         // this.shipmentsSubject.next(filteredShipments);
//     }

//     /**
//      * Get shipment by ID
//      */
//     getShipmentById(id: string): Observable<ShipmentDisplayData | undefined> {
//         return new Observable(observer => {
//             const shipments = this.shipmentsSubject.value;
//             const shipment = shipments.find(s => s.id === id);
//             observer.next(shipment);
//             observer.complete();
//         });
//     }

//     /**
//      * Refresh shipments data
//      */
//     refreshShipments(): void {
//         this.loadShipments();
//     }

//     /**
//      * Get current shipments count
//      */
//     getShipmentsCount(): number {
//         return this.shipmentsSubject.value.length;
//     }

//     /**
//      * Get shipments by status count
//      */
//     getShipmentsCountByStatus(status: string): number {
//         return this.shipmentsSubject.value.filter(shipment =>
//             shipment.status.status === status
//         ).length;
//     }

//     /**
//      * Get shipments by original API status count
//      */
//     getShipmentsCountByOriginalStatus(status: string): number {
//         return this.shipmentsSubject.value.filter(shipment =>
//             shipment.originalStatus === status
//         ).length;
//     }

//     /**
//      * Set loading state
//      */
//     private setLoading(loading: boolean): void {
//         this.loadingSubject.next(loading);
//     }

//     /**
//      * Set error message
//      */
//     private setError(error: string): void {
//         this.errorSubject.next(error);
//     }

//     /**
//      * Clear error message
//      */
//     private clearError(): void {
//         this.errorSubject.next(null);
//     }

//     /**
//      * Get current shipments (synchronous)
//      */
//     getCurrentShipments(): ShipmentDisplayData[] {
//         return this.shipmentsSubject.value;
//     }

//     /**
//      * Check if shipments are loaded
//      */
//     hasShipments(): boolean {
//         return this.shipmentsSubject.value.length > 0;
//     }
// }
