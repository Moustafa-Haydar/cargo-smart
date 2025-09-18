import { Routes } from '@angular/router';
import { Alerts } from './modules/alerts/alerts';
import { Vehicles } from './modules/vehicles/vehicles';
import { Shipments } from './modules/shipments/shipments';
import { RoutesPage } from './modules/routesPage/routes';
import { ProposalsPage } from './modules/proposalsPage/proposals';
import { LiveMap } from './modules/live-map/live-map';
import { Login } from './modules/login/login';
import { AuthGuard } from './core/auth/auth.guard';

export const routes: Routes = [

  // { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  // { path: 'dashboard', component: Dashboard },

  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: Login },
  { path: 'live-map', component: LiveMap, canActivate: [AuthGuard] },
  { path: 'shipments', component: Shipments, canActivate: [AuthGuard] },
  { path: 'vehicles', component: Vehicles, canActivate: [AuthGuard] },
  { path: 'routes', component: RoutesPage, canActivate: [AuthGuard] },
  { path: 'proposals', component: ProposalsPage, canActivate: [AuthGuard] },
  { path: 'alerts', component: Alerts, canActivate: [AuthGuard] },
];