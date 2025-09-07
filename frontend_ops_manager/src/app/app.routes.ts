import { Routes } from '@angular/router';
import { ShipmentsComponent } from './pages/shipments/shipments.component';
import { VehiclesComponent } from './pages/vehicles/vehicles.component';
import { RoutesComponent } from './pages/routes/routes.component';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { LiveMapComponent } from './pages/live-map/live-map.component';
import { AlertsComponent } from './pages/alerts/alerts.component';

export const routes: Routes = [

  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'shipments', component: ShipmentsComponent },
  { path: 'vehicles', component: VehiclesComponent },
  { path: 'routes', component: RoutesComponent },
  { path: 'live-map', component: LiveMapComponent },
  { path: 'alerts', component: AlertsComponent },

];