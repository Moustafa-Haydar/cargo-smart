import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SearchSection } from '../../shared/components/search-section/search-section';
import { VehicleCard } from '../../shared/components/vehicle-card/vehicle-card';
import { TransportVehicle, VehicleType } from '../../shared/models/logistics.model';

@Component({
  selector: 'app-vehicles',
  standalone: true,
  imports: [CommonModule, FormsModule, SearchSection, VehicleCard],
  templateUrl: './vehicles.html',
  styleUrls: ['./vehicles.css']
})
export class Vehicles {
  // state
  searchQuery = '';
  selectedType: VehicleType | null = null;

  vehicleTypeOptions = [
    { label: 'All', value: null },
    { label: 'Truck', value: 'TRUCK' as VehicleType },
    { label: 'Vessel', value: 'VESSEL' as VehicleType },
    { label: 'Plane', value: 'PLANE' as VehicleType },
  ];

  vehicles: TransportVehicle[] = [
    {
      id: 'TRK-1034',
      name: 'Truck 1034',
      type: 'TRUCK',
      status: 'UNDERWAY',
      current_location: { id: 'loc-sea', name: 'Seattle' },
      route: { id: 'rt-seattle', name: 'Seattle Route' },
      identifiers: [], // trucks typically no IMO/MMSI
      last_position: {
        recorded_at: '2025-09-04T10:12:00Z',
        lat: 47.6062, lng: -122.3321, source: 'SEED', location: 'Seattle'
      },
      positions: []
    },
    {
      id: 'VSL-0004',
      name: 'MAERSK DEMO 04',
      type: 'VESSEL',
      status: 'AT_PORT',
      imo: 9298004,
      mmsi: 367770004,
      call_sign: 'CALL004',
      flag: 'BE',
      current_location: { id: 'loc-hou', name: 'Houston' },
      route: { id: 'rt-02', name: 'Route 02' },
      identifiers: [{ scheme: 'IMO', value: '9298004' }],
      last_position: {
        recorded_at: '2025-09-04T18:58:13.833Z',
        lat: 25.2786457, lng: 55.40794077, source: 'SEED', location: 'Dubai'
      },
      positions: [],
      port_calls: [
        {
          id: 'pc-51655699',
          voyage: '303E',
          event: 'DEPARTURE',
          label: 'Vessel departure',
          scheduled_at: null,
          actual_at: null,
          status: 'PLANNED',
          source_ref: '',
          port_location: { id: 'port-sha', name: 'Shanghai' },
          facility: { id: 'fac-bre', name: 'MSC Gate Bremerhaven Gmbh & Co. KG' }
        }
      ]
    },
    {
      id: 'PLN-8821',
      name: 'Flight ABC123',
      type: 'PLANE',
      status: 'UNDERWAY',
      current_location: { id: 'loc-lax', name: 'Los Angeles' },
      route: { id: 'rt-transcon', name: 'Transcon Air Route' },
      identifiers: [{ scheme: 'IATA', value: 'ABC123' }],
      last_position: {
        recorded_at: '2025-09-04T09:00:00Z',
        lat: 36.1147, lng: -115.1728, source: 'ADS-B', location: 'Las Vegas FIR'
      },
      positions: []
    },
    {
      id: 'TRK-4521',
      name: 'Truck 4521',
      type: 'TRUCK',
      status: 'IDLE',
      current_location: { id: 'loc-den', name: 'Denver' },
      route: { id: 'rt-mountain', name: 'Mountain Route' },
      identifiers: [],
      positions: [],
      last_position: {
        recorded_at: '2025-09-03T18:00:00Z',
        lat: 39.7392, lng: -104.9903, source: 'SEED', location: 'Denver'
      }
    }
  ];

  filteredVehicles: TransportVehicle[] = [...this.vehicles];

  constructor() {
    this.filterVehicles();
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
