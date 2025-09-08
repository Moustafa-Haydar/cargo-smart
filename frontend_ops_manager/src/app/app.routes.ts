import { Routes } from '@angular/router';
import { Alerts } from './modules/alerts/alerts';
import { Vehicles } from './modules/vehicles/vehicles';
import { Shipments } from './modules/shipments/shipments';
import { RoutesPage } from './modules/routesPage/routes';
import { LiveMap } from './modules/live-map/live-map';

export const routes: Routes = [

  // { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  // { path: 'dashboard', component: Dashboard },

  { path: '', redirectTo: 'live-map', pathMatch: 'full' },
  { path: 'live-map', component: LiveMap },
  { path: 'shipments', component: Shipments },
  { path: 'vehicles', component: Vehicles },
  { path: 'routes', component: RoutesPage },
  { path: 'alerts', component: Alerts },
];