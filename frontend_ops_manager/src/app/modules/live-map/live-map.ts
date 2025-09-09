import { Component, inject, OnInit } from '@angular/core';
import { GoogleMapsModule } from '@angular/google-maps';
import { SearchSection } from '../../shared/components/search-section/search-section';
import { Route } from '../../shared/models/logistics.model';
import { Shipment, ShipmentType } from '../../shared/models/logistics.model';
import { ShipmentRepository } from '../shipments/shipment.repository';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-live-map',
  standalone: true,
  imports: [CommonModule, FormsModule, GoogleMapsModule, SearchSection],
  templateUrl: './live-map.html',
  styleUrl: './live-map.css'
})

export class LiveMap implements OnInit {
  private repo = inject(ShipmentRepository);

  options: google.maps.MapOptions = {
    mapId: "DEMO_MAP_ID",
    center: { lat: -31, lng: 147 },
    zoom: 4,
  }
    
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


  // locations on the map
  
  nzLocations: any[] = [
    { lat: -36.817685, lng: 175.699196 },
    { lat: -36.828611, lng: 175.790222 },
    { lat: -39.927193, lng: 175.053218 },
    { lat: -41.330162, lng: 174.865694 },
    { lat: -43.999792, lng: 170.463352 },
  ];
  auLocations: any[] = [
    { lat: -31.56391, lng: 147.154312 },
    { lat: -33.718234, lng: 150.363181 },
    { lat: -33.727111, lng: 150.371124 },
    { lat: -33.848588, lng: 151.209834 },
    { lat: -33.851702, lng: 151.216968 },
    { lat: -34.671264, lng: 150.863657 },
    { lat: -35.304724, lng: 148.662905 },
    { lat: -37.75, lng: 145.116667 },
    { lat: -37.759859, lng: 145.128708 },
    { lat: -37.765015, lng: 145.133858 },
    { lat: -37.770104, lng: 145.143299 },
    { lat: -37.7737, lng: 145.145187 },
    { lat: -37.774785, lng: 145.137978 },
    { lat: -37.819616, lng: 144.968119 },
    { lat: -38.330766, lng: 144.695692 },
    { lat: -42.734358, lng: 147.439506 },
    { lat: -42.734358, lng: 147.501315 },
    { lat: -42.735258, lng: 147.438 },
  ];

}
