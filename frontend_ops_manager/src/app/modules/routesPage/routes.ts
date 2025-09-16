import { ChangeDetectorRef, Component, DestroyRef, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouteCard } from '../../shared/components/route-card/route-card';
import { Route } from '../../shared/models/logistics.model';
import { SearchSection } from '../../shared/components/search-section/search-section';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { map } from 'rxjs';

import { RoutesRepository } from './routes.repository';

@Component({
  selector: 'app-routes',
  standalone: true,
  imports: [CommonModule, RouteCard, SearchSection],
  templateUrl: './routes.html',
  styleUrls: ['./routes.css']
})
export class RoutesPage {
  private routesRepo = inject(RoutesRepository);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

  destroyRef = inject(DestroyRef);

  // state
  routes: Route[] = [];
  filteredRoutes: Route[] = [...this.routes];

  searchQuery = '';

  // filter state (mirror shipments page)
  selectedCarrier: string | null = null;
  carrierOptions = [
    { label: 'All', value: null },
    { label: 'VRL Logistics', value: 'VRL Logistics' },
    { label: 'Delhivery', value: 'Delhivery' },
    { label: 'GATI', value: 'GATI' },
    { label: 'BlueDart', value: 'BlueDart' },
    { label: 'TCI Express', value: 'TCI Express' },
  ];

  ngOnInit(): void {
    // load routes data
    this.routesRepo.getRoutes().pipe(takeUntilDestroyed(this.destroyRef), map(res => res.routes ?? []))
      .subscribe({
        next: (data) => {
          this.routes = data ?? [];
          this.filterRoutes();
          this.changeDetectorRef.markForCheck();
        },
        error: (err) => {
          console.error('Failed to load routes', err);
          this.routes = [];
          this.filteredRoutes = [];
        }
      });
  }

  applySearch(q: string) {
    this.searchQuery = q ?? '';
    this.filterRoutes();
  }

  applyFilter(carrier: string | null) {
    this.selectedCarrier = carrier ?? null;
    this.filterRoutes();
  }

  private filterRoutes() {
    const q = this.searchQuery.trim().toLowerCase();

    this.filteredRoutes = this.routes.filter(route => {
      // Carrier filter: if selectedCarrier, any shipment on this route should match
      const matchesCarrier = !this.selectedCarrier || (route.shipments || []).some(s => s.carrier_name === this.selectedCarrier);

      const haystack = [
        route.id,
        route.name
      ]
        .filter(Boolean)
        .join(' ')
        .toLowerCase();

      const matchesQuery = !q || haystack.includes(q);
      return matchesCarrier && matchesQuery;
    });
  }
}