import { ChangeDetectorRef, Component, DestroyRef, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouteCard } from '../../shared/components/route-card/route-card';
import { Route } from '../../shared/models/logistics.model';
import { SearchSection } from '../../shared/components/search-section/search-section';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { map, catchError, of, forkJoin } from 'rxjs';
import { RoutesRepository } from './routes.repository';

@Component({
  selector: 'app-routes',
  standalone: true,
  imports: [CommonModule, SearchSection],
  templateUrl: './routes.html',
  styleUrls: ['./routes.css']
})
export class RoutesPage {
  private routesRepo = inject(RoutesRepository);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

  destroyRef = inject(DestroyRef);

  // state
  routes: Route[] = [];
  filteredRoutes: Route[] = [];

  loading = true;
  error: string | null = null;

  searchQuery = '';


  ngOnInit(): void {
    this.routesRepo.getRoutes().pipe(takeUntilDestroyed(this.destroyRef), map(res => res.routes ?? []))
      .subscribe({
        next: (data) => {
          this.routes = data ?? [];
          this.filterRoutes();
          this.loading = false;
          this.changeDetectorRef.markForCheck();
        },
        error: (err) => {
          console.error('Failed to load routes', err);
          this.routes = [];
          this.filteredRoutes = [];
          this.loading = false;
        }
      });
  }

  applySearch(q: string) {
    this.searchQuery = q ?? '';
    this.filterRoutes();
  }

  applyFilter(_: string | null) { this.filterRoutes(); }

  private filterRoutes() {
    const q = this.searchQuery.trim().toLowerCase();

    this.filteredRoutes = this.routes.filter(route => {
      const haystack = [
        route.id,
        route.name
      ]
        .filter(Boolean as any)
        .join(' ')
        .toLowerCase();

      const matchesQuery = !q || haystack.includes(q);
      return matchesQuery;
    });
  }
}