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

  options: any = {
    center: { lat: 20, lng: 80 },
    zoom: 5,
    streetViewControl: false,
    mapTypeControl: false,  // Disable internal map type control - use external controls only
    zoomControl: true,      // Keep zoom controls
    fullscreenControl: true, // Keep fullscreen control
    mapTypeId: 'roadmap',  // Use string instead of enum to avoid initialization issues
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
  selectedMapTheme: string = 'minimal';

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
      setTimeout(() => this.ngOnInit(), 1000); // Increased timeout
      return;
    }

    console.log('Google Maps API loaded successfully');

    // load shipments
    this.repo.getShipments()
      .pipe(takeUntilDestroyed(this.destroyRef), map(res => res.shipments ?? []))
      .subscribe({
        next: (data) => {
          this.shipments = data ?? [];
          this.filterData();
          console.log('Shipments loaded:', this.shipments.length, this.shipments);
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
          console.log('Locations loaded:', this.locations.length);
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

    // Apply the default minimal theme after a short delay to ensure map is ready
    setTimeout(() => {
      this.changeMapTheme();
    }, 500);

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
        case 'minimal':
          // Custom minimal theme - clean and light
          map.setOptions({
            styles: [
              { elementType: "geometry", stylers: [{ color: "#f1ebea" }] },
              { elementType: "labels.text.stroke", stylers: [{ color: "#ffffff" }] },
              { elementType: "labels.text.fill", stylers: [{ color: "#666666" }] },
              {
                featureType: "administrative.locality",
                elementType: "labels.text.fill",
                stylers: [{ color: "#333333" }]
              },
              {
                featureType: "poi",
                elementType: "labels.text.fill",
                stylers: [{ color: "#333333" }]
              },
              {
                featureType: "poi.park",
                elementType: "geometry",
                stylers: [{ color: "#e8f5e8" }]
              },
              {
                featureType: "poi.park",
                elementType: "labels.text.fill",
                stylers: [{ color: "#2d5a2d" }]
              },
              {
                featureType: "road",
                elementType: "geometry",
                stylers: [{ color: "#ffffff" }]
              },
              {
                featureType: "road",
                elementType: "geometry.stroke",
                stylers: [{ color: "#e0e0e0" }]
              },
              {
                featureType: "road",
                elementType: "labels.text.fill",
                stylers: [{ color: "#666666" }]
              },
              {
                featureType: "road.highway",
                elementType: "geometry",
                stylers: [{ color: "#f0f0f0" }]
              },
              {
                featureType: "road.highway",
                elementType: "geometry.stroke",
                stylers: [{ color: "#d0d0d0" }]
              },
              {
                featureType: "road.highway",
                elementType: "labels.text.fill",
                stylers: [{ color: "#333333" }]
              },
              {
                featureType: "transit",
                elementType: "geometry",
                stylers: [{ color: "#f8f8f8" }]
              },
              {
                featureType: "transit.station",
                elementType: "labels.text.fill",
                stylers: [{ color: "#333333" }]
              },
              {
                featureType: "water",
                elementType: "geometry",
                stylers: [{ color: "#add3db" }]
              },
              {
                featureType: "water",
                elementType: "labels.text.fill",
                stylers: [{ color: "#4682B4" }]
              },
              {
                featureType: "water",
                elementType: "labels.text.stroke",
                stylers: [{ color: "#ffffff" }]
              }
            ]
          });
          break;
        case 'roadmap':
          map.setMapTypeId('roadmap');
          break;
        case 'satellite':
          map.setMapTypeId('satellite');
          break;
        case 'hybrid':
          map.setMapTypeId('hybrid');
          break;
        case 'terrain':
          map.setMapTypeId('terrain');
          break;
      }
    }
  }

  private filterData() {
    const q = this.searchQuery.trim().toLowerCase();

    // Removed custom SVG content since we're using regular markers now

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

      console.log('Shipment markers created:', this.shipmentLocations.length, this.shipmentLocations);
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
          let color = '#F68716'; // secondary color for truck routes

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
