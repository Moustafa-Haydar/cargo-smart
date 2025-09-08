import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SearchSection } from '../../shared/components/search-section/search-section';
import { Shipment, ShipmentType } from '../../shared/models/logistics.model';
import { ShipmentCard } from '../../shared/components/shipment-card/shipment-card';
import { ShipmentRepository } from './shipment.repository';

@Component({
  selector: 'app-shipments',
  standalone: true,
  imports: [CommonModule, FormsModule, SearchSection, ShipmentCard],
  templateUrl: './shipments.html',
  styleUrls: ['./shipments.css']
})
export class Shipments implements OnInit {
  private repo = inject(ShipmentRepository);

  // keep a concrete array for filtering
  shipments: Shipment[] = [];
  filteredShipments: Shipment[] = [];

  searchQuery = '';
  selectedType: ShipmentType | null = null;

  shipmentTypeOptions = [
    { label: 'All', value: null },
    { label: 'BBK', value: 'BBK' as ShipmentType },
    { label: 'LCL', value: 'LCL' as ShipmentType },
    { label: 'CT', value: 'CT' as ShipmentType },
  ];

  ngOnInit(): void {
    // load data first, then filter
    this.repo.getShipments().subscribe({
      next: (data) => {
        this.shipments = data ?? [];
        this.filterShipments();
      },
      error: (err) => {
        console.error('Failed to load shipments', err);
        this.shipments = [];
        this.filteredShipments = [];
      }
    });
  }

  applySearch(q: string) {
    this.searchQuery = q ?? '';
    this.filterShipments();
  }

  applyFilter(type: ShipmentType | null) {
    this.selectedType = type ?? null;
    this.filterShipments();
  }

  private filterShipments() {
    const q = this.searchQuery.trim().toLowerCase();

    this.filteredShipments = this.shipments.filter(s => {
      const matchesType = !this.selectedType || s.shipment_type === this.selectedType;

      const haystack = [
        s.id,
        s.ref_no,
        s.shipment_type,
        s.status,
        s.carrier_code,
        s.carrier_name,
        s.origin?.name,
        s.destination?.name,
        s.current_location?.name,
        s.route?.name,
      ].filter(Boolean).join(' ').toLowerCase();

      const matchesQuery = !q || haystack.includes(q);
      return matchesType && matchesQuery;
    });
  }
}
