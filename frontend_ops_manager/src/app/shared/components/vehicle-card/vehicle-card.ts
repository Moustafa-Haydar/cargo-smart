import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Tag } from 'primeng/tag';
import { TransportVehicle } from '../../models/logistics.model';
import { Card } from 'primeng/card';

@Component({
  selector: 'app-vehicle-card',
  standalone: true,
  imports: [CommonModule, Card],
  templateUrl: './vehicle-card.html',
  styleUrls: ['./vehicle-card.css']
})
export class VehicleCard {
  @Input({ required: true }) vehicle!: TransportVehicle;

  get icon(): string {
    // Since we don't have type field, default to truck for all vehicles
    return 'fa-truck';
  }

  get statusSeverity(): 'success' | 'info' | 'warning' | 'danger' {
    switch (this.vehicle.status) {
      case 'IN_TRANSIT': return 'success';
      case 'ACTIVE': return 'info';
      case 'MAINTENANCE': return 'warning';
      default: return 'info';
    }
  }

  // Health status based on vehicle operational status
  get healthStatus(): 'Excellent' | 'Attention' | 'Critical' {
    switch (this.vehicle.status) {
      case 'IN_TRANSIT': return 'Excellent';
      case 'ACTIVE': return 'Excellent';
      case 'MAINTENANCE': return 'Critical';
      default: return 'Attention';
    }
  }

  // Health percentage based on status
  get healthPercentage(): number {
    switch (this.vehicle.status) {
      case 'IN_TRANSIT': return 96;
      case 'ACTIVE': return 85;
      case 'MAINTENANCE': return 15;
      default: return 50;
    }
  }

  // Estimated mileage based on vehicle status
  get estimatedMileage(): number {
    const baseMileage = 89432; // Default truck mileage

    // Add some variation based on status
    const multiplier = this.vehicle.status === 'IN_TRANSIT' ? 1.1 :
      this.vehicle.status === 'ACTIVE' ? 1.0 : 0.8;

    return Math.round(baseMileage * multiplier);
  }
}
