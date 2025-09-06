import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home';
import { ShipmentsPage } from './pages/shipments/shipments';

export const routes: Routes = [

  { path: '', component: HomeComponent }, // default page
  { path: 'shipments', component: ShipmentsPage }
  
];