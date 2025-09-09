import { Component, DestroyRef, inject, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { GoogleMap, GoogleMapsModule, MapInfoWindow } from '@angular/google-maps';
import { SearchSection } from '../../shared/components/search-section/search-section';
import { Shipment, ShipmentType } from '../../shared/models/logistics.model';
import { ShipmentRepository } from '../shipments/shipment.repository';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { map } from 'rxjs';

type LatLng = google.maps.LatLngLiteral;

interface MarkerData {
  position: LatLng;
  shipment: Shipment;
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
  filteredShipments: Shipment[] = [];
  markers: MarkerData[] = [];

  searchQuery = '';
  selectedType: ShipmentType | null = null;

  shipmentTypeOptions = [
    { label: 'All', value: null },
    { label: 'BBK', value: 'BBK' as ShipmentType },
    { label: 'LCL', value: 'LCL' as ShipmentType },
    { label: 'CT', value: 'CT' as ShipmentType },
  ];

  activeShipment: Shipment | null = null;

  ngOnInit(): void {
    // load data first, then filter
    this.repo.getShipments().pipe(takeUntilDestroyed(this.destroyRef),map(res => res.shipments ?? []))
      .subscribe({
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

    this.refreshMarkers();
  }

  private refreshMarkers() {
    this.markers = [];
    const bounds = new google.maps.LatLngBounds();
    let hasPoints = false;

    for (const s of this.filteredShipments) {
      const pos = this.pickDisplayPosition(s);
      if (pos) {
        this.markers.push({ position: pos, shipment: s });
        bounds.extend(pos as any);
        hasPoints = true;
      }
    }

    if (hasPoints && this.googleMap) {
      (this.googleMap as any).fitBounds(bounds, 40);
    } else if (this.googleMap) {
      this.googleMap.googleMap?.setCenter(this.options.center!);
      this.googleMap.googleMap?.setZoom(this.options.zoom!);
    }
  }

  private pickDisplayPosition(s: Shipment): LatLng | null {
    return this.getLatLng(s.current_location) ?? this.getLatLng(s.origin) ?? null;
  }

  private getLatLng(entity: any): LatLng | null {
    if (!entity) return null;
    if (typeof entity.lat === 'number' && typeof entity.lng === 'number') {
      return { lat: entity.lat, lng: entity.lng };
    }
    if (typeof entity.latitude === 'number' && typeof entity.longitude === 'number') {
      return { lat: entity.latitude, lng: entity.longitude };
    }
    if (entity.location && typeof entity.location.lat === 'number' && typeof entity.location.lng === 'number') {
      return { lat: entity.location.lat, lng: entity.location.lng };
    }
    if (Array.isArray(entity.coordinates) && entity.coordinates.length >= 2) {
      const [lng, lat] = entity.coordinates;
      if (typeof lat === 'number' && typeof lng === 'number') return { lat, lng };
    }
    if (entity.geojson && Array.isArray(entity.geojson.coordinates)) {
      const [lng, lat] = entity.geojson.coordinates;
      if (typeof lat === 'number' && typeof lng === 'number') return { lat, lng };
    }
    return null;
  }

  openInfo(marker: any, m: MarkerData) {
    this.activeShipment = m.shipment;
    this.infoWindow.open(marker);
  }

}

