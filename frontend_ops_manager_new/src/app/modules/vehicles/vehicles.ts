import { ChangeDetectorRef, Component, DestroyRef, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SearchSection } from '../../shared/components/search-section/search-section';
import { VehicleCard } from '../../shared/components/vehicle-card/vehicle-card';
import { TransportVehicle, VehicleType } from '../../shared/models/logistics.model';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { map } from 'rxjs';
import { VehiclesRepository } from './vehicles.repository';

@Component({
  selector: 'app-vehicles',
  standalone: true,
  imports: [CommonModule, FormsModule, SearchSection, VehicleCard],
  templateUrl: './vehicles.html',
  styleUrls: ['./vehicles.css']
})
export class Vehicles {
  private repo = inject(VehiclesRepository);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

  destroyRef = inject(DestroyRef);

  vehicles: TransportVehicle[] = [];
  filteredVehicles: TransportVehicle[] = [];

  searchQuery = '';
  selectedStatus: string | null = null;

  statusOptions = [
    { label: 'All', value: null },
    { label: 'Active', value: 'ACTIVE' },
    { label: 'In Transit', value: 'IN_TRANSIT' },
    { label: 'Maintenance', value: 'MAINTENANCE' },
  ];

  ngOnInit(): void {
    // load data first, then filter
    this.repo.getVehicles().pipe(takeUntilDestroyed(this.destroyRef), map(res => res.vehicles ?? []))
      .subscribe({
        next: (data) => {
          this.vehicles = data ?? [];
          this.filterVehicles();
          this.changeDetectorRef.markForCheck();
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

  applyFilter(status: string | null) {
    this.selectedStatus = status ?? null;
    this.filterVehicles();
  }

  private filterVehicles() {
    const q = this.searchQuery.trim().toLowerCase();

    this.filteredVehicles = this.vehicles.filter(v => {
      const matchesStatus = !this.selectedStatus || v.status === this.selectedStatus;

      const haystack = [
        v.id,
        v.plate_number,
        v.model,
        v.status,
        v.current_location?.name
      ].filter(Boolean).join(' ').toLowerCase();

      const matchesQuery = !q || haystack.includes(q);
      return matchesStatus && matchesQuery;
    });
  }
}
