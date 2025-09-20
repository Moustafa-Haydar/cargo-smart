import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Shipment, TransportVehicle, Route } from '../../../shared/models/logistics.model';

@Component({
    selector: 'app-hover-tooltip',
    standalone: true,
    imports: [CommonModule],
    template: `
    <div class="tooltip" [ngClass]="tooltipClass">
      <div class="tooltip-content">
        <div class="tooltip-header">
          <h4>{{ title }}</h4>
          <span class="tooltip-type">{{ type }}</span>
        </div>
        
        <div class="tooltip-body">
          <div *ngIf="shipment" class="shipment-details">
            <div class="detail-row">
              <span class="label">ID:</span>
              <span class="value">{{ shipment.id }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Reference:</span>
              <span class="value">{{ shipment.ref_no || 'N/A' }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Status:</span>
              <span class="value status" [ngClass]="'status-' + shipment.status">{{ shipment.status }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Carrier:</span>
              <span class="value">{{ shipment.carrier_name || 'N/A' }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Origin:</span>
              <span class="value">{{ shipment.origin.name || 'N/A' }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Destination:</span>
              <span class="value">{{ shipment.destination.name || 'N/A' }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Current Location:</span>
              <span class="value">{{ shipment.current_location.name || 'N/A' }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Scheduled:</span>
              <span class="value">{{ formatDate(shipment.scheduled_at) }}</span>
            </div>
            <div class="detail-row" *ngIf="shipment.delivered_at">
              <span class="label">Delivered:</span>
              <span class="value">{{ formatDate(shipment.delivered_at) }}</span>
            </div>
            <div class="detail-row" *ngIf="shipment.progress_pct">
              <span class="label">Progress:</span>
              <span class="value">{{ shipment.progress_pct }}%</span>
            </div>
            <div class="detail-row" *ngIf="shipment.route">
              <span class="label">Route:</span>
              <span class="value">{{ shipment.route.name || shipment.route.id }}</span>
            </div>
            <div class="detail-row" *ngIf="shipment.vehicle">
              <span class="label">Vehicle:</span>
              <span class="value">{{ shipment.vehicle.plate_number || shipment.vehicle.id }}</span>
            </div>
          </div>

          <div *ngIf="vehicle" class="vehicle-details">
            <div class="detail-row">
              <span class="label">ID:</span>
              <span class="value">{{ vehicle.id }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Plate Number:</span>
              <span class="value">{{ vehicle.plate_number || 'N/A' }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Model:</span>
              <span class="value">{{ vehicle.model || 'N/A' }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Status:</span>
              <span class="value status" [ngClass]="'status-' + vehicle.status">{{ vehicle.status }}</span>
            </div>
            <div class="detail-row" *ngIf="vehicle.current_location">
              <span class="label">Current Location:</span>
              <span class="value">{{ vehicle.current_location.name || 'N/A' }}</span>
            </div>
            <div class="detail-row" *ngIf="vehicle.last_position">
              <span class="label">Last Position:</span>
              <span class="value">{{ vehicle.last_position.location || 'N/A' }}</span>
            </div>
            <div class="detail-row" *ngIf="vehicle.last_position && vehicle.last_position.lat != null && vehicle.last_position.lng != null">
              <span class="label">Coordinates:</span>
              <span class="value">{{ (vehicle.last_position.lat || 0) | number:'1.0-4' }}, {{ (vehicle.last_position.lng || 0) | number:'1.0-4' }}</span>
            </div>
            <div class="detail-row" *ngIf="vehicle.identifiers && vehicle.identifiers.length > 0">
              <span class="label">Identifiers:</span>
              <span class="value">{{ vehicle.identifiers.length }} items</span>
            </div>
            <div class="detail-row" *ngIf="vehicle.port_calls && vehicle.port_calls.length > 0">
              <span class="label">Port Calls:</span>
              <span class="value">{{ vehicle.port_calls.length }} calls</span>
            </div>
          </div>

          <div *ngIf="route" class="route-details">
            <div class="detail-row">
              <span class="label">Name:</span>
              <span class="value">{{ route.name || 'N/A' }}</span>
            </div>
            <div class="detail-row">
              <span class="label">ID:</span>
              <span class="value">{{ route.id || 'N/A' }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Segments:</span>
              <span class="value">{{ route.segments.length || 0 }}</span>
            </div>
            <div class="detail-row" *ngIf="route.shipments && route.shipments.length > 0">
              <span class="label">Shipments:</span>
              <span class="value">{{ route.shipments.length }}</span>
            </div>
            <div class="detail-row" *ngIf="route.geometry">
              <span class="label">Geometry:</span>
              <span class="value">Available</span>
            </div>
          </div>

          <!-- Fallback for when route data is not found -->
          <div *ngIf="!route && type === 'route'" class="route-details">
            <div class="detail-row">
              <span class="label">Route Segment:</span>
              <span class="value">Route data not available</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
    styleUrls: ['./hover-tooltip.component.css']
})
export class HoverTooltipComponent {
    @Input() title: string = '';
    @Input() type: 'shipment' | 'vehicle' | 'route' = 'shipment';
    @Input() shipment?: Shipment;
    @Input() vehicle?: TransportVehicle;
    @Input() route?: Route;
    @Input() tooltipClass: string = '';

    formatDate(dateString?: string): string {
        if (!dateString) return 'N/A';
        try {
            return new Date(dateString).toLocaleDateString();
        } catch {
            return 'N/A';
        }
    }

    formatDuration(minutes?: number): string {
        if (!minutes) return 'N/A';
        const hours = Math.floor(minutes / 60);
        const mins = minutes % 60;
        return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;
    }
}
