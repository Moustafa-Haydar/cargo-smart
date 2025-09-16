import { Component, inject, OnInit, DestroyRef, ChangeDetectorRef } from '@angular/core';
import { SearchSection } from '../../shared/components/search-section/search-section';
import { Shipment, ShipmentType } from '../../shared/models/logistics.model';
import { ShipmentCard } from '../../shared/components/shipment-card/shipment-card';
import { ShipmentsRepository } from './shipment.repository';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { map, takeUntil, } from 'rxjs';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { SkeletonModule } from 'primeng/skeleton';

@Component({
  selector: 'app-shipments',
  standalone: true,
  imports: [CommonModule, FormsModule, SearchSection, ShipmentCard, SkeletonModule],
  templateUrl: './shipments.html',
  styleUrls: ['./shipments.css']
})
export class Shipments implements OnInit {
  private repo = inject(ShipmentsRepository);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

  destroyRef = inject(DestroyRef);

  // keep a concrete array for filtering
  shipments: Shipment[] = [];
  filteredShipments: Shipment[] = [];
  loading = true;

  searchQuery = '';
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
    // load data first, then filter
    this.repo.getShipments().pipe(takeUntilDestroyed(this.destroyRef), map(res => res.shipments ?? []))
      .subscribe({
        next: (data) => {
          this.shipments = data ?? [];
          this.filterShipments();
          this.loading = false;
          this.changeDetectorRef.markForCheck();
        },
        error: (err) => {
          console.error('Failed to load shipments', err);
          this.shipments = [];
          this.filteredShipments = [];
          this.loading = false;
        }
      });
  }

  applySearch(q: string) {
    this.searchQuery = q ?? '';
    this.filterShipments();
  }

  applyFilter(carrier: string | null) {
    this.selectedCarrier = carrier ?? null;
    this.filterShipments();
  }

  private filterShipments() {
    const q = this.searchQuery.trim().toLowerCase();

    this.filteredShipments = this.shipments.filter(s => {
      const matchesCarrier = !this.selectedCarrier || s.carrier_name === this.selectedCarrier;

      const haystack = [
        s.id,
        s.ref_no,
        s.status,
        s.carrier_name,
        s.origin?.name,
        s.destination?.name,
        s.current_location?.name,
        s.route?.name,
        s.vehicle?.plate_number,
        s.vehicle?.model,
      ].filter(Boolean).join(' ').toLowerCase();

      const matchesQuery = !q || haystack.includes(q);
      return matchesCarrier && matchesQuery;
    });
  }
}
