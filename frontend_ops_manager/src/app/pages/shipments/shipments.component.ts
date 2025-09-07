import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ShipmentCardComponent } from '../../components/shipment-card/shipment-card.component';

interface Shipment {
  id: string;
  type: string;
  origin: string;
  destination: string;
  status: {
    status: 'Delivered' | 'In-Transit' | 'Delayed';
    percentage: number;
  };
  eta?: string;
  deliveryDate?: string;
  daysRemaining?: number;
}

@Component({
  selector: 'app-shipments',
  standalone: true,
  imports: [CommonModule, FormsModule, ShipmentCardComponent],
  templateUrl: './shipments.component.html',
  styleUrls: ['./shipments.component.css']
})

export class ShipmentsComponent {
  searchQuery: string = '';
  shipments: Shipment[] = [
    {
      id: 'SH-2024-001',
      type: 'Electronics',
      origin: 'San Francisco',
      destination: 'New York',
      status: { status: 'Delivered', percentage: 100 },
      deliveryDate: 'Dec 26, 2024'
    },
    {
      id: 'SH-2024-002',
      type: 'Electronics',
      origin: 'San Francisco',
      destination: 'New York',
      status: { status: 'In-Transit', percentage: 78 },
      eta: 'Dec 28, 2024',
      daysRemaining: 236
    },
    {
      id: 'SH-2024-003',
      type: 'Electronics',
      origin: 'San Francisco',
      destination: 'New York',
      status: { status: 'Delayed', percentage: 45 },
      eta: 'Dec 28, 2024',
      daysRemaining: 236
    }
  ];

  onSearch() {
    // Implement search logic here
    console.log('Searching for:', this.searchQuery);
  }

  toggleFilters() {
    // Implement filter toggle logic here
    console.log('Toggle filters');
  }
}