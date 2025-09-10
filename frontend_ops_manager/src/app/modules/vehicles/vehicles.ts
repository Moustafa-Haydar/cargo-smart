import { Component, DestroyRef, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SearchSection } from '../../shared/components/search-section/search-section';
import { VehicleCard } from '../../shared/components/vehicle-card/vehicle-card';
import { TransportVehicle, VehicleType } from '../../shared/models/logistics.model';
import { VehicleRepository } from './vehicles.repository';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { map } from 'rxjs';

@Component({
  selector: 'app-vehicles',
  standalone: true,
  imports: [CommonModule, FormsModule, SearchSection, VehicleCard],
  templateUrl: './vehicles.html',
  styleUrls: ['./vehicles.css']
})
export class Vehicles {
  private repo = inject(VehicleRepository);

  destroyRef = inject(DestroyRef);

  vehicles: TransportVehicle[] = [];
  filteredVehicles: TransportVehicle[] = [];

  searchQuery = '';
  selectedType: VehicleType | null = null;

  vehicleTypeOptions = [
    { label: 'All', value: null },
    { label: 'Truck', value: 'TRUCK' as VehicleType },
    { label: 'Vessel', value: 'VESSEL' as VehicleType },
    { label: 'Plane', value: 'PLANE' as VehicleType },
  ];

  ngOnInit(): void {
    // load data first, then filter
    this.repo.getVehicles().pipe(takeUntilDestroyed(this.destroyRef),map(res => res.vehicles ?? []))
      .subscribe({
      next: (data) => {
        this.vehicles = data ?? [];
        this.filterVehicles();
      },
      error: (err) => {
        console.error('Failed to load vehicles', err);
        this.vehicles = [];
        this.filteredVehicles = [];
      }
    });
  }

  applySearch(q: string) {
    this.searchQuery = q ?? '';
    this.filterVehicles();
  }

  applyFilter(type: VehicleType | null) {
    this.selectedType = type ?? null;
    this.filterVehicles();
  }

  private filterVehicles() {
    const q = this.searchQuery.trim().toLowerCase();

    this.filteredVehicles = this.vehicles.filter(v => {
      const matchesType = !this.selectedType || v.type === this.selectedType;

      const haystack = [
        v.id,
        v.name,
        v.type,
        v.status,
        v.current_location?.name,
        v.route?.name
      ].filter(Boolean).join(' ').toLowerCase();

      const matchesQuery = !q || haystack.includes(q);
      return matchesType && matchesQuery;
    });
  }
}
