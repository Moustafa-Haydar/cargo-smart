import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
// import { SearchSection } from '../../shared/components/search-section/search-section';

@Component({
  selector: 'app-alerts',
  imports: [CommonModule, FormsModule],
  templateUrl: './alerts.html',
  styleUrl: './alerts.css'
})
export class Alerts {

  // searchQuery = '';
  // selectedType: ShipmentType | null = null;

  // shipmentTypeOptions = [
  //   { label: 'All', value: null },
  //   { label: 'BBK', value: 'BBK' as ShipmentType },
  //   { label: 'LCL', value: 'LCL' as ShipmentType },
  //   { label: 'CT', value: 'CT' as ShipmentType },
  // ];

  // filteredShipments: Shipment[] = [];

  // ngOnInit(): void {
  //   this.filterShipments();
  // }

  // applySearch(q: string) {
  //   this.searchQuery = q ?? '';
  //   this.filterShipments();
  // }

  // applyFilter(type: ShipmentType | null) {
  //   this.selectedType = type ?? null;
  //   this.filterShipments();
  // }

  // private filterShipments() {
  //   const q = this.searchQuery.trim().toLowerCase();

  //   this.filteredShipments = this.shipments.filter(s => {
  //     const matchesType = !this.selectedType || s.shipment_type === this.selectedType;

  //     const haystack = [
  //       s.id,
  //       s.ref_no,
  //       s.shipment_type,
  //       s.status,
  //       s.carrier_code,
  //       s.carrier_name,
  //       s.origin?.name,
  //       s.destination?.name,
  //       s.current_location?.name,
  //       s.route?.name,
  //     ]
  //       .filter(Boolean)
  //       .join(' ')
  //       .toLowerCase();

  //     const matchesQuery = !q || haystack.includes(q);
  //     return matchesType && matchesQuery;
  //   });
  // }
}