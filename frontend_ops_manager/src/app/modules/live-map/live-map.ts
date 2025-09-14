import { Component, DestroyRef, inject, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { GoogleMap, GoogleMapsModule, MapAdvancedMarker, MapInfoWindow } from '@angular/google-maps';
import { SearchSection } from '../../shared/components/search-section/search-section';
import { GeoLocation, Route, Shipment, TransportVehicle } from '../../shared/models/logistics.model';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { map } from 'rxjs';
import { ShipmentRepository } from '../shipments/shipment.repository';
import { VehicleRepository } from '../vehicles/vehicles.repository';
import { LocationRepository } from './live-map.repository';
import { RouteRepository } from '../routesPage/routes.repository';

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
  content: Node | null;
}

interface VehicleLocation {
  id: string;
  name: string;
  lat: number;
  lng: number;
  vehicle: TransportVehicle;
}

interface RouteSegmentLine {
  id: string;
  routeId: string;
  routeName: string;
  seq: number;
  path: LatLng[];
  color: string;
}

@Component({
  selector: 'app-live-map',
  standalone: true,
  imports: [CommonModule, FormsModule, GoogleMapsModule, SearchSection, MapAdvancedMarker],
  templateUrl: './live-map.html',
  styleUrl: './live-map.css'
})
export class LiveMap implements OnInit {
  private repo = inject(ShipmentRepository);
  private geoRepo = inject(LocationRepository);
  private vehicleRepo = inject(VehicleRepository);
  private routeRepo = inject(RouteRepository)
  destroyRef = inject(DestroyRef);

  @ViewChild(GoogleMap) googleMap!: GoogleMap;
  @ViewChild(MapInfoWindow) infoWindow!: MapInfoWindow;

  options: google.maps.MapOptions = {
    center: { lat: 40, lng: -20 },
    zoom: 3,
    streetViewControl: false,
    mapTypeControl: true,  // Enable map type control to switch themes
    mapTypeId: 'roadmap' as any,  // Use string instead of enum to avoid initialization issues
    // mapId: '80701f24f0f842f7eba9f816'  // Commented out to use default themes
  };

  shipments: Shipment[] = [];
  routes: Route[] = [];
  routeSegments: RouteSegmentLine[] = [];
  locations: GeoLocation[] = [];
  vehicles: TransportVehicle[] = [];
  vehicleLocations: VehicleLocation[] = [];
  shipmentLocations: ShipmentLocation[] = [];
  filteredShipments: Shipment[] = [];

  searchQuery = '';
  selectedTypeOption: TypeOption = 'Shipments';
  selectedMapTheme: string = 'roadmap';

  typeOptions = [
    { label: 'All', value: null },
    { label: 'Shipments', value: 'Shipments' as TypeOption },
    { label: 'Vehicles', value: 'Vehicles' as TypeOption },
    { label: 'Routes', value: 'Routes' as TypeOption },
  ];

  // fetch all data (shipments, locations, routes, vehicles, ...)
  ngOnInit(): void {
    // Wait for Google Maps to be available
    if (typeof google === 'undefined' || !google.maps) {
      console.warn('Google Maps API not loaded yet, retrying...');
      setTimeout(() => this.ngOnInit(), 100);
      return;
    }

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

    // load routes
    this.routeRepo.getRoutes()
      .pipe(takeUntilDestroyed(this.destroyRef), map(res => res.routes ?? []))
      .subscribe({
        next: (data) => {
          console.log('routes: ', data);
          this.routes = data ?? [];
        },
        error: (err) => {
          console.error('Failed to load routes', err);
          this.routes = [];
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

  onThemeChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    this.selectedMapTheme = target.value;
    console.log('Theme changed to:', this.selectedMapTheme);
    this.changeMapTheme();
  }

  changeMapTheme() {
    if (this.googleMap && this.googleMap.googleMap) {
      const map = this.googleMap.googleMap;

      switch (this.selectedMapTheme) {
        case 'roadmap':
          map.setMapTypeId('roadmap' as any);
          break;
        case 'satellite':
          map.setMapTypeId('satellite' as any);
          break;
        case 'hybrid':
          map.setMapTypeId('hybrid' as any);
          break;
        case 'terrain':
          map.setMapTypeId('terrain' as any);
          break;
        case 'dark':
          // Custom dark theme
          map.setOptions({
            styles: [
              { elementType: "geometry", stylers: [{ color: "#242f3e" }] },
              { elementType: "labels.text.stroke", stylers: [{ color: "#242f3e" }] },
              { elementType: "labels.text.fill", stylers: [{ color: "#746855" }] },
              {
                featureType: "administrative.locality",
                elementType: "labels.text.fill",
                stylers: [{ color: "#d59563" }]
              },
              {
                featureType: "poi",
                elementType: "labels.text.fill",
                stylers: [{ color: "#d59563" }]
              },
              {
                featureType: "poi.park",
                elementType: "geometry",
                stylers: [{ color: "#263c3f" }]
              },
              {
                featureType: "poi.park",
                elementType: "labels.text.fill",
                stylers: [{ color: "#6b9a76" }]
              },
              {
                featureType: "road",
                elementType: "geometry",
                stylers: [{ color: "#38414e" }]
              },
              {
                featureType: "road",
                elementType: "geometry.stroke",
                stylers: [{ color: "#212a37" }]
              },
              {
                featureType: "road",
                elementType: "labels.text.fill",
                stylers: [{ color: "#9ca5b3" }]
              },
              {
                featureType: "road.highway",
                elementType: "geometry",
                stylers: [{ color: "#746855" }]
              },
              {
                featureType: "road.highway",
                elementType: "geometry.stroke",
                stylers: [{ color: "#1f2835" }]
              },
              {
                featureType: "road.highway",
                elementType: "labels.text.fill",
                stylers: [{ color: "#f3d19c" }]
              },
              {
                featureType: "transit",
                elementType: "geometry",
                stylers: [{ color: "#2f3948" }]
              },
              {
                featureType: "transit.station",
                elementType: "labels.text.fill",
                stylers: [{ color: "#d59563" }]
              },
              {
                featureType: "water",
                elementType: "geometry",
                stylers: [{ color: "#17263c" }]
              },
              {
                featureType: "water",
                elementType: "labels.text.fill",
                stylers: [{ color: "#515c6d" }]
              },
              {
                featureType: "water",
                elementType: "labels.text.stroke",
                stylers: [{ color: "#17263c" }]
              }
            ]
          });
          break;
      }
    }
  }

  private filterData() {
    const q = this.searchQuery.trim().toLowerCase();

    const parser = new DOMParser();

    const svgString = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#358c99" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-container-icon lucide-container"><path d="M22 7.7c0-.6-.4-1.2-.8-1.5l-6.3-3.9a1.72 1.72 0 0 0-1.7 0l-10.3 6c-.5.2-.9.8-.9 1.4v6.6c0 .5.4 1.2.8 1.5l6.3 3.9a1.72 1.72 0 0 0 1.7 0l10.3-6c.5-.3.9-1 .9-1.5Z"/><path d="M10 21.9V14L2.1 9.1"/><path d="m10 14 11.9-6.9"/><path d="M14 19.8v-8.1"/><path d="M18 17.5V9.4"/></svg>`;
    const svgNode = parser.parseFromString(svgString, "image/svg+xml").documentElement;

    // --- Shipments ---
    if (this.selectedTypeOption === 'Shipments') {
      this.vehicleLocations = [];
      this.routeSegments = [];

      this.filteredShipments = this.shipments.filter(s => {
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
            content: svgNode.cloneNode(true) as HTMLElement,
          } as any);
        }

        return markers;
      });

      console.log('Markers:', this.shipmentLocations);
    }

    // --- Vehicles ---
    if (this.selectedTypeOption === 'Vehicles') {
      this.shipmentLocations = [];
      this.routeSegments = [];

      this.vehicleLocations = this.vehicles.flatMap(v => {
        const markers: VehicleLocation[] = [];

        // Prefer last_position if it exists
        if (v.last_position?.lat && v.last_position?.lng) {
          markers.push({
            id: `${v.id}-lastpos`,
            name: v.last_position.location || v.plate_number,
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

    // --- Routes ---
    if (this.selectedTypeOption === 'Routes') {
      this.shipmentLocations = [];
      this.vehicleLocations = [];

      this.routeSegments = this.routes.flatMap(r => {
        if (q && !r.name.toLowerCase().includes(q)) return [];

        return (r.segments ?? []).map(seg => {
          // Parse GeoJSON
          const geo = JSON.parse(seg.geometry);
          const path: LatLng[] = geo.coordinates.map(
            (c: [number, number]) => ({ lat: c[1], lng: c[0] })
          );

          // Color by route (simplified - all routes are truck routes)
          let color = '#4CAF50'; // green for truck routes

          return {
            id: seg.id,
            routeId: r.id,
            routeName: r.name,
            seq: seg.seq,
            path,
            color
          };
        });
      });

      console.log('Route polylines:', this.routeSegments);
    }


  }

}
