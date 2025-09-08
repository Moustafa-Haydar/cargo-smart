import { Routes } from '@angular/router';
import { DashboardComponent } from './modules/dashboard/dashboard.component';
import { LiveMapComponent } from './modules/live-map/live-map.component';
import { RoutesComponent } from './modules/routes/routes.component';
import { Alerts } from './modules/alerts/alerts';
import { Vehicles } from './modules/vehicles/vehicles';
import { Shipments } from './modules/shipments/shipments';


export const routes: Routes = [

  // { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  { path: '', redirectTo: 'live-map', pathMatch: 'full' },
  { path: 'live-map', component: LiveMapComponent },
  // { path: 'dashboard', component: DashboardComponent },
  { path: 'shipments', component: Shipments },
  { path: 'vehicles', component: Vehicles },
  { path: 'routes', component: RoutesComponent },
  { path: 'alerts', component: Alerts },

];