import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { VehicleCardComponent, Vehicle } from '../../components/vehicle-card/vehicle-card.component';

@Component({
    selector: 'app-vehicles',
    standalone: true,
    imports: [CommonModule, FormsModule, VehicleCardComponent],
    templateUrl: './vehicles.component.html',
    styleUrls: ['./vehicles.component.css']
})
export class VehiclesComponent {
    searchQuery: string = '';
    filteredVehicles: Vehicle[] = [];

    vehicles: Vehicle[] = [
        {
            id: 'TRK-1034',
            type: 'truck',
            route: 'Seattle Route',
            mileage: 89432,
            health: { status: 'excellent', percentage: 96 }
        },
        {
            id: 'TRK-2847',
            type: 'truck',
            route: 'Coast Route',
            mileage: 203,
            health: { status: 'attention', percentage: 74 }
        },
        {
            id: 'CNT-5678',
            type: 'container',
            route: 'Pacific Route',
            mileage: 156,
            health: { status: 'critical', percentage: 42 }
        },
        {
            id: 'TRK-4521',
            type: 'truck',
            route: 'Mountain Route',
            mileage: 125430,
            health: { status: 'excellent', percentage: 89 }
        },
        {
            id: 'CNT-7890',
            type: 'container',
            route: 'Desert Route',
            mileage: 67,
            health: { status: 'attention', percentage: 68 }
        },
        {
            id: 'TRK-1234',
            type: 'truck',
            route: 'Urban Route',
            mileage: 45678,
            health: { status: 'critical', percentage: 35 }
        }
    ];

    constructor() {
        this.filteredVehicles = [...this.vehicles];
    }

    onSearch(): void {
        if (!this.searchQuery.trim()) {
            this.filteredVehicles = [...this.vehicles];
            return;
        }

        const query = this.searchQuery.toLowerCase();
        this.filteredVehicles = this.vehicles.filter(vehicle =>
            vehicle.id.toLowerCase().includes(query) ||
            vehicle.type.toLowerCase().includes(query) ||
            vehicle.route.toLowerCase().includes(query)
        );
    }
}