import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Vehicle } from '../../shared/models/shipments.model';
import { VehicleCard } from '../../shared/components/vehicle-card/vehicle-card';
import { SearchSection } from '../../shared/components/search-section/search-section';

@Component({
  selector: 'app-vehicles',
  standalone: true,
  imports: [CommonModule, SearchSection, VehicleCard],
  templateUrl: './vehicles.html',
  styleUrls: ['./vehicles.css']
})

export class Vehicles {
  // state
  searchQuery = '';
  selectedType: string | null = null;

  vehicleTypeOptions = [
    { label: 'All', value: null },
    { label: 'Truck', value: 'truck' },
    { label: 'Ship', value: 'ship' },
    { label: 'Plane', value: 'plane' },
  ];

  vehicles: Vehicle[] = [
    { id: 'TRK-1034', type: 'truck', route: 'Seattle Route',  mileage: 89432,  health: { status: 'excellent', percentage: 96 } },
    { id: 'TRK-2847', type: 'truck', route: 'Coast Route',    mileage: 203,    health: { status: 'attention', percentage: 74 } },
    { id: 'TRK-4521', type: 'truck', route: 'Mountain Route', mileage: 125430, health: { status: 'excellent', percentage: 89 } },
    { id: 'TRK-1234', type: 'truck', route: 'Urban Route',    mileage: 45678,  health: { status: 'critical', percentage: 35 } }
  ];

  filteredVehicles: Vehicle[] = [...this.vehicles];

  constructor() {
    this.filterVehicles();
  }

  applySearch(q: string) {
    this.searchQuery = q ?? '';
    this.filterVehicles();
  }

  applyFilter(type: any) {
    this.selectedType = type ?? null;
    this.filterVehicles();
  }

  // search
  private filterVehicles() {
    const q = this.searchQuery.trim().toLowerCase();

    this.filteredVehicles = this.vehicles.filter(v => {
      const matchesType = !this.selectedType || v.type === this.selectedType;
      const matchesQuery =
        !q ||
        v.id.toLowerCase().includes(q) ||
        v.type.toLowerCase().includes(q) ||
        v.route.toLowerCase().includes(q);

      return matchesType && matchesQuery;
    });
  }
}
