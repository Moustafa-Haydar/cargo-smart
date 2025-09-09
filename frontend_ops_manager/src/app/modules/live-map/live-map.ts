import { Component } from '@angular/core';
import { GoogleMapsModule } from '@angular/google-maps';

@Component({
  selector: 'app-live-map',
  standalone: true,
  imports: [GoogleMapsModule],
  templateUrl: './live-map.html',
  styleUrl: './live-map.css'
})
export class LiveMap {
  options: google.maps.MapOptions = {
    mapId: "DEMO_MAP_ID",
    center: { lat: -31, lng: 147 },
    zoom: 4,
  };
}
