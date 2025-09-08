import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouteCard } from '../../shared/components/route-card/route-card';
import { Route, RouteSegment, RouteType, TransportMode } from '../../shared/models/logistics.model';

@Component({
  selector: 'app-routes',
  standalone: true,
  imports: [CommonModule, RouteCard],
  templateUrl: './routes.html',
  styleUrls: ['./routes.css']
})
export class RoutesPage {
  routes: Route[] = [
    {
      id: 'rt-sf-nyc',
      name: 'SF-NYC Express',
      geometry: 'LINESTRING(-122.4194 37.7749, -74.0060 40.7128)',
      segments: [
        {
          id: 'seg-1',
          seq: 1,
          route_type: 'LAND' as RouteType,
          geometry: 'LINESTRING(-122.4194 37.7749, -74.0060 40.7128)',
          mode: 'TRUCK' as TransportMode,
          eta_start: '2025-01-15T08:00:00Z',
          eta_end: '2025-01-17T10:00:00Z'
        }
      ],
      vehicles: [],
      shipments: []
    },
    {
      id: 'rt-la-chi',
      name: 'LA-Chicago Route',
      geometry: 'LINESTRING(-118.2437 34.0522, -87.6298 41.8781)',
      segments: [
        {
          id: 'seg-2',
          seq: 1,
          route_type: 'LAND' as RouteType,
          geometry: 'LINESTRING(-118.2437 34.0522, -87.6298 41.8781)',
          mode: 'TRUCK' as TransportMode,
          eta_start: '2025-01-16T06:00:00Z',
          eta_end: '2025-01-18T14:00:00Z'
        }
      ],
      vehicles: [],
      shipments: []
    },
    {
      id: 'rt-sea-air',
      name: 'Seattle-Air Express',
      geometry: 'LINESTRING(-122.3321 47.6062, -74.0060 40.7128)',
      segments: [
        {
          id: 'seg-3',
          seq: 1,
          route_type: 'AIR' as RouteType,
          geometry: 'LINESTRING(-122.3321 47.6062, -74.0060 40.7128)',
          mode: 'PLANE' as TransportMode,
          eta_start: '2025-01-15T12:00:00Z',
          eta_end: '2025-01-15T20:00:00Z'
        }
      ],
      vehicles: [],
      shipments: []
    },
    {
      id: 'rt-miami-atlanta',
      name: 'Miami-Atlanta Route',
      geometry: 'LINESTRING(-80.1918 25.7617, -84.3880 33.7490)',
      segments: [
        {
          id: 'seg-4',
          seq: 1,
          route_type: 'LAND' as RouteType,
          geometry: 'LINESTRING(-80.1918 25.7617, -84.3880 33.7490)',
          mode: 'TRUCK' as TransportMode,
          eta_start: '2025-01-16T08:00:00Z',
          eta_end: '2025-01-16T18:00:00Z'
        }
      ],
      vehicles: [],
      shipments: []
    },
    {
      id: 'rt-boston-nyc',
      name: 'Boston-NYC Route',
      geometry: 'LINESTRING(-71.0589 42.3601, -74.0060 40.7128)',
      segments: [
        {
          id: 'seg-5',
          seq: 1,
          route_type: 'LAND' as RouteType,
          geometry: 'LINESTRING(-71.0589 42.3601, -74.0060 40.7128)',
          mode: 'TRUCK' as TransportMode,
          eta_start: '2025-01-17T06:00:00Z',
          eta_end: '2025-01-17T12:00:00Z'
        }
      ],
      vehicles: [],
      shipments: []
    }
  ];
}