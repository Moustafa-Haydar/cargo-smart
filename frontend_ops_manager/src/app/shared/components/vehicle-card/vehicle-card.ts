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
    return this.vehicle.type === 'TRUCK'
      ? 'fa-truck'
      : this.vehicle.type === 'VESSEL'
        ? 'fa-ship'
        : 'fa-plane';
  }

  get statusSeverity(): 'success' | 'info' | 'warning' | 'danger' {
    switch (this.vehicle.status) {
      case 'UNDERWAY': return 'success';
      case 'AT_PORT':
      case 'IDLE': return 'info';
      case 'OUT_OF_SERVICE': return 'danger';
      default: return 'warning';
    }
  }

  // Health status based on vehicle operational status
  get healthStatus(): 'Excellent' | 'Attention' | 'Critical' {
    switch (this.vehicle.status) {
      case 'UNDERWAY': return 'Excellent';
      case 'IDLE': return 'Attention';
      case 'OUT_OF_SERVICE': return 'Critical';
      default: return 'Attention';
    }
  }

  // Health percentage based on status
  get healthPercentage(): number {
    switch (this.vehicle.status) {
      case 'UNDERWAY': return 96;
      case 'AT_PORT': return 74;
      case 'IDLE': return 42;
      case 'OUT_OF_SERVICE': return 15;
      default: return 50;
    }
  }

  // Estimated mileage based on vehicle type and status
  get estimatedMileage(): number {
    const baseMileage = this.vehicle.type === 'TRUCK' ? 89432 :
      this.vehicle.type === 'VESSEL' ? 203 : 156;

    // Add some variation based on status
    const multiplier = this.vehicle.status === 'UNDERWAY' ? 1.1 :
      this.vehicle.status === 'AT_PORT' ? 0.9 : 0.8;

    return Math.round(baseMileage * multiplier);
  }
}
