import { Component, DestroyRef, inject, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { GoogleMap, GoogleMapsModule, MapAdvancedMarker, MapInfoWindow } from '@angular/google-maps';
import { SearchSection } from '../../shared/components/search-section/search-section';
import { FilterComponent, SelectOption } from '../../shared/components/filter/filter';
import { GeoLocation, Route, Shipment, TransportVehicle } from '../../shared/models/logistics.model';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { map } from 'rxjs';
import { ShipmentsRepository } from '../shipments/shipment.repository';
import { LocationRepository } from './live-map.repository';
import { VehiclesRepository } from '../vehicles/vehicles.repository';
import { RoutesRepository } from '../routesPage/routes.repository';

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
  imports: [CommonModule, FormsModule, GoogleMapsModule, SearchSection, FilterComponent, MapAdvancedMarker],
  templateUrl: './live-map.html',
  styleUrl: './live-map.css'
})
export class LiveMap implements OnInit {
  private repo = inject(ShipmentsRepository);
  private geoRepo = inject(LocationRepository);
  private vehicleRepo = inject(VehiclesRepository);
  private routeRepo = inject(RoutesRepository)
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
  selectedMapTheme: string = 'light';

  // Data type selection
  selectedDataType: 'routes' | 'shipments' | 'vehicles' = 'routes';

  // New filter properties
  selectedShipment: string | null = null;
  selectedVehicle: string | null = null;
  selectedRoute: string | null = null;


  // Custom icons for markers
  shipmentIcon: any;
  vehicleIcon: any;

  // Map theme options for the search component dropdown
  themeOptions = [
    { label: 'Light Theme', value: 'light' },
    { label: 'Dark Theme', value: 'dark' },
    { label: 'Satellite', value: 'satellite' },
    { label: 'Terrain', value: 'terrain' }
  ];

  // Data type options
  dataTypeOptions = [
    { label: 'Routes', value: 'routes' },
    { label: 'Shipments', value: 'shipments' },
    { label: 'Vehicles', value: 'vehicles' }
  ];

  // Filter options
  shipmentOptions: SelectOption[] = [];
  vehicleOptions: SelectOption[] = [];
  routeOptions: SelectOption[] = [];

  // fetch all data (shipments, locations, routes, vehicles, ...)
  ngOnInit(): void {
    // Wait for Google Maps to be available
    if (typeof google === 'undefined' || !google.maps) {
      console.warn('Google Maps API not loaded yet, retrying...');
      setTimeout(() => this.ngOnInit(), 1000); // Increased timeout
      return;
    }

    console.log('Google Maps API loaded successfully');

    // Initialize custom icons
    this.initializeIcons();

    // load shipments
    this.repo.getShipments()
      .pipe(takeUntilDestroyed(this.destroyRef), map(res => res.shipments ?? []))
      .subscribe({
        next: (data) => {
          this.shipments = data ?? [];
          this.shipmentOptions = this.shipments.map(shipment => ({
            label: shipment.ref_no || shipment.id,
            value: shipment.id
          }));
          this.filterData();
          console.log('Shipments loaded:', this.shipments.length, this.shipments);
        },
        error: (err) => {
          console.error('Failed to load shipments', err);
          this.shipments = [];
          this.filteredShipments = [];
          this.shipmentOptions = [];
        }
      });

    // load vehicles
    this.vehicleRepo.getVehicles()
      .pipe(takeUntilDestroyed(this.destroyRef), map((res: any) => res.vehicles ?? []))
      .subscribe({
        next: (data: TransportVehicle[]) => {
          this.vehicles = data ?? [];
          this.vehicleOptions = this.vehicles.map(vehicle => ({
            label: vehicle.plate_number || vehicle.id,
            value: vehicle.id
          }));
          this.filterData();
          console.log(this.vehicles);
        },
        error: (err: any) => {
          console.error('Failed to load vehicles', err);
          this.vehicles = [];
          this.vehicleOptions = [];
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
      .pipe(takeUntilDestroyed(this.destroyRef), map((res: any) => res.routes ?? []))
      .subscribe({
        next: (data: Route[]) => {
          console.log('routes: ', data);
          this.routes = data ?? [];
          this.routeOptions = this.routes.map(route => ({
            label: route.name || route.id,
            value: route.id
          }));
        },
        error: (err: any) => {
          console.error('Failed to load routes', err);
          this.routes = [];
          this.routeOptions = [];
        }
      });

    // Apply the default minimal theme after a short delay to ensure map is ready
    setTimeout(() => {
      this.changeMapTheme();
    }, 500);

  }

  private initializeIcons() {
    // Use simple icon URLs without Google Maps constructors
    this.shipmentIcon = {
      url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(`
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#358C9C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M22 7.7c0-.6-.4-1.2-.8-1.5l-6.3-3.9a1.72 1.72 0 0 0-1.7 0l-10.3 6c-.5.2-.9.8-.9 1.4v6.6c0 .5.4 1.2.8 1.5l6.3 3.9a1.72 1.72 0 0 0 1.7 0l10.3-6c.5-.3.9-1 .9-1.5Z"/>
          <path d="M10 21.9V14L2.1 9.1"/>
          <path d="m10 14 11.9-6.9"/>
          <path d="M14 19.8v-8.1"/>
          <path d="M18 17.5V9.4"/>
        </svg>
      `),
      scaledSize: { width: 24, height: 24 },
      anchor: { x: 12, y: 12 }
    };

    this.vehicleIcon = {
      url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(`
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#F68716" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9L18.7 9.2c-.3-.8-1-1.2-1.7-1.2H5c-.7 0-1.4.4-1.7 1.2L2.5 11.1C1.7 11.3 1 12.1 1 13v3c0 .6.4 1 1 1h2"/>
          <circle cx="7" cy="17" r="2"/>
          <path d="M9 17h6"/>
          <circle cx="17" cy="17" r="2"/>
        </svg>
      `),
      scaledSize: { width: 24, height: 24 },
      anchor: { x: 12, y: 12 }
    };
  }

  trackById(index: number, item: { id: string }) {
    return item.id;
  }

  applySearch(q: string) {
    this.searchQuery = q ?? '';
    this.filterData();
  }

  applyTypeFilter(selectedTheme: any) {
    this.selectedMapTheme = selectedTheme;
    console.log('Theme changed to:', this.selectedMapTheme);
    this.changeMapTheme();
  }

  onDataTypeChange(selectedDataType: any) {
    this.selectedDataType = selectedDataType;
    // Clear all specific filters when changing data type
    this.selectedShipment = null;
    this.selectedVehicle = null;
    this.selectedRoute = null;
    this.filterData();
  }

  onShipmentFilterChange(selectedShipment: any) {
    this.selectedShipment = selectedShipment;
    this.filterData();
  }

  onVehicleFilterChange(selectedVehicle: any) {
    this.selectedVehicle = selectedVehicle;
    this.filterData();
  }

  onRouteFilterChange(selectedRoute: any) {
    this.selectedRoute = selectedRoute;
    this.filterData();
  }

  changeMapTheme() {
    if (this.googleMap && this.googleMap.googleMap) {
      const map = this.googleMap.googleMap;

      switch (this.selectedMapTheme) {
        case 'light':
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
        case 'dark':
          // Dark theme
          map.setOptions({
            styles: [
              { elementType: "geometry", stylers: [{ color: "#212121" }] },
              { elementType: "labels.text.stroke", stylers: [{ color: "#212121" }] },
              { elementType: "labels.text.fill", stylers: [{ color: "#757575" }] },
              {
                featureType: "administrative.locality",
                elementType: "labels.text.fill",
                stylers: [{ color: "#bdbdbd" }]
              },
              {
                featureType: "poi",
                elementType: "labels.text.fill",
                stylers: [{ color: "#757575" }]
              },
              {
                featureType: "poi.park",
                elementType: "geometry",
                stylers: [{ color: "#263238" }]
              },
              {
                featureType: "poi.park",
                elementType: "labels.text.fill",
                stylers: [{ color: "#6b9b37" }]
              },
              {
                featureType: "road",
                elementType: "geometry",
                stylers: [{ color: "#2b2b2b" }]
              },
              {
                featureType: "road",
                elementType: "geometry.stroke",
                stylers: [{ color: "#212121" }]
              },
              {
                featureType: "road",
                elementType: "labels.text.fill",
                stylers: [{ color: "#9ca3af" }]
              },
              {
                featureType: "road.highway",
                elementType: "geometry",
                stylers: [{ color: "#373737" }]
              },
              {
                featureType: "road.highway",
                elementType: "geometry.stroke",
                stylers: [{ color: "#212121" }]
              },
              {
                featureType: "road.highway",
                elementType: "labels.text.fill",
                stylers: [{ color: "#b3b3b3" }]
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
        case 'satellite':
          map.setMapTypeId('satellite');
          break;
        case 'terrain':
          map.setMapTypeId('terrain');
          break;
      }
    }
  }

  private filterData() {
    const q = this.searchQuery.trim().toLowerCase();

    // Clear all data first
    this.shipmentLocations = [];
    this.vehicleLocations = [];
    this.routeSegments = [];
    this.filteredShipments = [];

    // Show data based on selected data type
    switch (this.selectedDataType) {
      case 'routes':
        this.showRoutesData(q);
        break;
      case 'shipments':
        this.showShipmentsData(q);
        break;
      case 'vehicles':
        this.showVehiclesData(q);
        break;
    }

    console.log('Filtered data:', {
      dataType: this.selectedDataType,
      shipments: this.shipmentLocations.length,
      vehicles: this.vehicleLocations.length,
      routes: this.routeSegments.length
    });
  }

  private showRoutesData(q: string) {
    // Filter routes based on search query and selected route
    let filteredRoutes = this.routes.filter(r => {
      const haystack = [r.id, r.name].filter(Boolean).join(' ').toLowerCase();
      const matchesQuery = !q || haystack.includes(q);
      const matchesRoute = !this.selectedRoute || r.id === this.selectedRoute;
      return matchesQuery && matchesRoute;
    });

    // Show route segments
    this.routeSegments = this.createRouteSegments(filteredRoutes);

    // If a specific route is selected, show related shipments and vehicles
    if (this.selectedRoute) {
      const selectedRoute = this.routes.find(r => r.id === this.selectedRoute);
      if (selectedRoute) {
        // Show shipments using this route
        const shipmentsUsingRoute = this.shipments.filter(s =>
          s.route && s.route.id === this.selectedRoute
        );
        this.filteredShipments = shipmentsUsingRoute;
        this.shipmentLocations = this.createShipmentMarkers(shipmentsUsingRoute);

        // Show vehicles used by these shipments
        const vehicleIds = new Set(shipmentsUsingRoute.map(s => s.vehicle?.id).filter(Boolean));
        const associatedVehicles = this.vehicles.filter(v => vehicleIds.has(v.id));
        this.vehicleLocations = this.createVehicleMarkers(associatedVehicles);
      }
    }
  }

  private showShipmentsData(q: string) {
    // Filter shipments based on search query and selected shipment
    let filteredShipments = this.shipments.filter(s => {
      const haystack = [
        s.id, s.ref_no, s.status, s.carrier_name,
        s.origin?.name, s.destination?.name, s.current_location?.name,
        s.route?.name, s.vehicle?.plate_number, s.vehicle?.model,
      ].filter(Boolean).join(' ').toLowerCase();
      const matchesQuery = !q || haystack.includes(q);
      const matchesShipment = !this.selectedShipment || s.id === this.selectedShipment;
      return matchesQuery && matchesShipment;
    });

    this.filteredShipments = filteredShipments;
    this.shipmentLocations = this.createShipmentMarkers(filteredShipments);

    // If a specific shipment is selected, show its route and vehicle
    if (this.selectedShipment) {
      const selectedShipment = this.shipments.find(s => s.id === this.selectedShipment);
      if (selectedShipment) {
        // Show the route associated with this shipment
        if (selectedShipment.route) {
          const route = this.routes.find(r => r.id === selectedShipment.route?.id);
          if (route) {
            this.routeSegments = this.createRouteSegments([route]);
          }
        }

        // Show the vehicle associated with this shipment
        if (selectedShipment.vehicle) {
          const vehicle = this.vehicles.find(v => v.id === selectedShipment.vehicle?.id);
          if (vehicle) {
            this.vehicleLocations = this.createVehicleMarkers([vehicle]);
          }
        }
      }
    }
  }

  private showVehiclesData(q: string) {
    // Filter vehicles based on search query and selected vehicle
    let filteredVehicles = this.vehicles.filter(v => {
      const haystack = [
        v.id, v.plate_number, v.model, v.status, v.current_location?.name,
      ].filter(Boolean).join(' ').toLowerCase();
      const matchesQuery = !q || haystack.includes(q);
      const matchesVehicle = !this.selectedVehicle || v.id === this.selectedVehicle;
      return matchesQuery && matchesVehicle;
    });

    this.vehicleLocations = this.createVehicleMarkers(filteredVehicles);

    // If a specific vehicle is selected, show its shipments and routes
    if (this.selectedVehicle) {
      const selectedVehicle = this.vehicles.find(v => v.id === this.selectedVehicle);
      if (selectedVehicle) {
        // Find shipments using this vehicle
        const shipmentsUsingVehicle = this.shipments.filter(s =>
          s.vehicle && s.vehicle.id === this.selectedVehicle
        );
        this.filteredShipments = shipmentsUsingVehicle;
        this.shipmentLocations = this.createShipmentMarkers(shipmentsUsingVehicle);

        // Show routes associated with these shipments
        const routeIds = new Set(shipmentsUsingVehicle.map(s => s.route?.id).filter(Boolean));
        const associatedRoutes = this.routes.filter(r => routeIds.has(r.id));
        this.routeSegments = this.createRouteSegments(associatedRoutes);
      }
    }
  }

  private createShipmentMarkers(shipments: Shipment[]): ShipmentLocation[] {
    return shipments.flatMap(s => {
      const markers: ShipmentLocation[] = [];
      const resolveLoc = (id?: string) => this.locations.find(loc => loc.id === id);
      const current = resolveLoc(s.current_location?.id);

      if (current) {
        markers.push({
          id: `${s.id}-current`,
          name: current.name,
          lat: current.lat,
          lng: current.lng,
          shipment: s,
        } as any);
      }
      return markers;
    });
  }

  private createVehicleMarkers(vehicles: TransportVehicle[]): VehicleLocation[] {
    return vehicles.flatMap(v => {
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

      // Or fallback to current_location
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
  }

  private createRouteSegments(routes: Route[]): RouteSegmentLine[] {
    return routes.flatMap(r => {
      return (r.segments ?? []).map(seg => {
        const geo = JSON.parse(seg.geometry);
        const path: LatLng[] = geo.coordinates.map(
          (c: [number, number]) => ({ lat: c[1], lng: c[0] })
        );

        return {
          id: seg.id,
          routeId: r.id,
          routeName: r.name,
          seq: seg.seq,
          path,
          color: '#F68716'
        };
      });
    });
  }

}
