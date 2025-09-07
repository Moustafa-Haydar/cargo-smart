import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

export interface VehicleHealth {
    status: 'excellent' | 'attention' | 'critical';
    percentage: number;
}

export interface Vehicle {
    id: string;
    type: 'truck' | 'container';
    route: string;
    mileage: number;
    health: VehicleHealth;
}

@Component({
    selector: 'app-vehicle-card',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './vehicle-card.component.html',
    styleUrls: ['./vehicle-card.component.css']
})
export class VehicleCardComponent {
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
}
