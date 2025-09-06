import { Routes } from '@angular/router';
import { ShipmentsComponent } from './pages/shipments/shipments.component';
import { VehiclesComponent } from './pages/vehicles/vehicles.component';
import { RoutesComponent } from './pages/routes/routes.component';

export const routes: Routes = [
  { path: '', redirectTo: 'shipments', pathMatch: 'full' },
  { path: 'shipments', component: ShipmentsComponent },
  { path: 'vehicles', component: VehiclesComponent },
  { path: 'routes', component: RoutesComponent }
];