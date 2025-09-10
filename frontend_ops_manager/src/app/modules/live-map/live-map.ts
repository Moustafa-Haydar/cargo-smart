import { Component, DestroyRef, inject, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { GoogleMap, GoogleMapsModule, MapInfoWindow } from '@angular/google-maps';
import { SearchSection } from '../../shared/components/search-section/search-section';
import { GeoLocation, Shipment, TransportVehicle } from '../../shared/models/logistics.model';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { map } from 'rxjs';
import { ShipmentRepository } from '../shipments/shipment.repository';
import { VehicleRepository } from '../vehicles/vehicles.repository';
import { LocationRepository } from './live-map.repository';

type LatLng = google.maps.LatLngLiteral;
type TypeOption = 'Shipments' | 'Vehicles' | 'Routes' | null;

interface MarkerData {
  position: LatLng;
  shipment?: Shipment;
}

interface ShipmentLocation {
  id: string;
  name: string;
  lat: number;
  lng: number;
  shipment: Shipment;
}

interface VehicleLocation {
  id: string;
  name: string;
  lat: number;
  lng: number;
  vehicle: TransportVehicle;
}

@Component({
  selector: 'app-live-map',
  standalone: true,
  imports: [CommonModule, FormsModule, GoogleMapsModule, SearchSection],
  templateUrl: './live-map.html',
  styleUrl: './live-map.css'
})
export class LiveMap implements OnInit {
  private repo = inject(ShipmentRepository);
  private geoRepo = inject(LocationRepository);
  private vehicleRepo = inject(VehicleRepository);
  destroyRef = inject(DestroyRef);

  @ViewChild(GoogleMap) googleMap!: GoogleMap;
  @ViewChild(MapInfoWindow) infoWindow!: MapInfoWindow;

  options: google.maps.MapOptions = {
    center: { lat: 30, lng: 0 },
    zoom: 2,
    streetViewControl: false,
    mapTypeControl: false,
  };

  shipments: Shipment[] = [];
  locations: GeoLocation[] = [];
  vehicles: TransportVehicle[] = [];
  vehicleLocations: VehicleLocation[] = [];
  shipmentLocations: ShipmentLocation[] = [];
  filteredShipments: Shipment[] = [];

  searchQuery = '';
  selectedTypeOption: TypeOption = 'Shipments';

  typeOptions = [
    { label: 'All', value: null },
    { label: 'Shipments', value: 'Shipments' as TypeOption },
    { label: 'Vehicles', value: 'Vehicles' as TypeOption },
    { label: 'Routes', value: 'Routes' as TypeOption },
  ];

  // fetch all data (shipments, locations, routes, vehicles, ...)
  ngOnInit(): void {
    // load shipments
    this.repo.getShipments()
      .pipe(takeUntilDestroyed(this.destroyRef), map(res => res.shipments ?? []))
      .subscribe({
        next: (data) => {
          this.shipments = data ?? [];
          this.filterData();
          console.log(this.shipments);
        },
        error: (err) => {
          console.error('Failed to load shipments', err);
          this.shipments = [];
          this.filteredShipments = [];
        }
      });

    // load vehicles
    this.vehicleRepo.getVehicles()
      .pipe(takeUntilDestroyed(this.destroyRef), map(res => res.vehicles ?? []))
      .subscribe({
        next: (data) => {
          this.vehicles = data ?? [];
          this.filterData();
          console.log(this.vehicles);
        },
        error: (err) => {
          console.error('Failed to load vehicles', err);
          this.vehicles = [];
        }
      });

    // load locations
    this.geoRepo.getLocations()
      .pipe(takeUntilDestroyed(this.destroyRef), map(res => res.locations ?? []))
      .subscribe({
        next: (data) => {
          this.locations = data ?? [];
        },
        error: (err) => {
          console.error('Failed to load locations', err);
          this.locations = [];
        }
      });
  }

  trackById(index: number, item: { id: string }) {
    return item.id;
  }

  applySearch(q: string) {
    this.searchQuery = q ?? '';
    this.filterData();
  }

  applyTypeFilter(type: TypeOption) {
    this.selectedTypeOption = type ?? null;
    this.filterData();
  }

  private filterData() {
  const q = this.searchQuery.trim().toLowerCase();

  if (this.selectedTypeOption === 'Shipments') {
    this.filteredShipments = this.shipments.filter(s => {
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

      return !q || haystack.includes(q);
    });

    this.shipmentLocations = this.filteredShipments.flatMap(s => {
      const markers: ShipmentLocation[] = [];

      // helper to resolve a location by id
      const resolveLoc = (id?: string) =>
        this.locations.find(loc => loc.id === id);

      const current = resolveLoc(s.current_location?.id);
      if (current) {
        markers.push({
          id: `${s.id}-current`,
          name: current.name,
          lat: current.lat,
          lng: current.lng,
          shipment: s,
        });
      }

      return markers;
    });

    console.log('Markers:', this.shipmentLocations);
  }

  if (this.selectedTypeOption === 'Vehicles') {
    this.vehicleLocations = this.vehicles.flatMap(v => {
      const markers: VehicleLocation[] = [];

      // Prefer last_position if it exists
      if (v.last_position?.lat && v.last_position?.lng) {
        markers.push({
          id: `${v.id}-lastpos`,
          name: v.last_position.location || v.name,
          lat: v.last_position.lat,
          lng: v.last_position.lng,
          vehicle: v,
        });
      }

      // Or fallback to current_location linked with your locations array
      const current = this.locations.find(loc => loc.id === v.current_location?.id);
      if (current) {
        markers.push({
          id: `${v.id}-current`,
          name: current.name,
          lat: current.lat,
          lng: current.lng,
          vehicle: v,
        });
      }

      return markers;
    });

    console.log('Vehicle markers:', this.vehicleLocations);
  }


  }

}
