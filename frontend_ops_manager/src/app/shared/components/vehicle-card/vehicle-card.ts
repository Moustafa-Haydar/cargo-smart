import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Vehicle } from '../../models/shipments.model';
import { Tag } from 'primeng/tag';
import { Card } from 'primeng/card';

@Component({
    selector: 'app-vehicle-card',
    standalone: true,
    imports: [CommonModule, Tag, Card],
    templateUrl: './vehicle-card.html',
    styleUrls: ['./vehicle-card.css']
})
export class VehicleCard {
    @Input() vehicle!: Vehicle;

    get vehicleIcon(): string {
        return this.vehicle.type === 'truck' ? 'fa-truck' : 'fa-cube';
    }

    get statusText(): string {
        return this.vehicle.health.status.charAt(0).toUpperCase() + this.vehicle.health.status.slice(1);
    }

    get formattedMileage(): string {
        return this.vehicle.mileage.toLocaleString();
    }

    getTagSeverity(statusText : string) : string {
        switch (statusText) { 
            case 'excellent':
                return 'success';
            case 'attention':
                return 'warn';
            case 'critical':
                return 'danger';
            default:
                return 'danger';
        }

    }
}
