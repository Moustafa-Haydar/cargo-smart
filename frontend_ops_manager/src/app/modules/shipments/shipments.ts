import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SearchSection } from '../../shared/components/search-section/search-section';
import { Shipment, ShipmentType } from '../../shared/models/logistics.model';
import { ShipmentCard } from '../../shared/components/shipment-card/shipment-card';

@Component({
  selector: 'app-shipments',
  standalone: true,
  imports: [CommonModule, FormsModule, SearchSection, ShipmentCard],
  templateUrl: './shipments.html',
  styleUrls: ['./shipments.css']
})
export class Shipments implements OnInit {
  // UI state
  searchQuery = '';
  selectedType: ShipmentType | null = null;

  shipmentTypeOptions = [
    { label: 'All', value: null },
    { label: 'BBK', value: 'BBK' as ShipmentType },
    { label: 'LCL', value: 'LCL' as ShipmentType },
    { label: 'CT', value: 'CT' as ShipmentType },
  ];

  shipments: Shipment[] = [
    {
      id: "b2f7e1b8-4b7c-4b3d-8b5f-1a2c3d4e5f61",
      ref_no: "SHP0011",
      shipment_type: "CT",
      status: "IN_TRANSIT",
      carrier_code: "MAEU",
      carrier_name: "Maersk",
      origin: { id: "9ea29a91-3fcd-4257-ae3f-f4dfa8238cab", name: "Rotterdam" },
      destination: { id: "69d99cc1-32cc-4f81-9322-5f3e7dfbe794", name: "Los Angeles" },
      current_location: { id: "093857b4-d332-4f54-a328-d1a1ee285fa0", name: "Santos" },
      scheduled_at: "2025-09-04T14:58:23.499625+00:00",
      delivered_at: null,
      route: { id: "0b6e0f2e-5c1b-4b4f-8e44-0a6c1b2d3e45", name: "Route 11" },
      vehicles: [{ id: "46a025e1-2696-475b-a0f5-56bd7b494dd2", name: "MAERSK DEMO 11", voyage: "340E", role: "MAIN" }],
      containers: [{ id: "2b83c86f-c266-4090-bae5-7c666219862e", number: "MSKU1234567", status: "LOADED" }],
      progress_pct: 35
    },
    {
      id: "c13d9c3f-2a2b-4f5e-9a7b-0f1e2d3c4b5a",
      ref_no: "SHP0012",
      shipment_type: "LCL",
      status: "CREATED",
      carrier_code: "CMA",
      carrier_name: "CMA CGM",
      origin: { id: "11097c08-d557-45aa-a705-abe4bc880b89", name: "Singapore" },
      destination: { id: "5ce4e93b-914e-4595-a4de-0ddc808f7b30", name: "Houston" },
      current_location: { id: "11097c08-d557-45aa-a705-abe4bc880b89", name: "Singapore" },
      scheduled_at: "2025-09-02T09:15:00.000000+00:00",
      delivered_at: null,
      route: { id: "d16e7b20-dd6e-427a-a4b6-36712ec20d83", name: "Route 12" },
      vehicles: [{ id: "a7556615-257b-4076-8cdc-0863ad753e6e", name: "CMA DEMO 12", voyage: "220W", role: "FEEDER" }],
      containers: [{ id: "495fda69-df91-40a6-9a5e-ec682618cb72", number: "MSCU7654321", status: "GATE_IN" }],
      progress_pct: 0
    },
    {
      id: "f91a7e81-0d3f-4b83-8b2f-1f3a2e4b5c6d",
      ref_no: "SHP0014",
      shipment_type: "CT",
      status: "IN_TRANSIT",
      carrier_code: "MAEU",
      carrier_name: "Maersk",
      origin: { id: "2a5e350b-c32b-4a3d-8b03-cb8cf2764164", name: "Bremerhaven" },
      destination: { id: "97585599-8d5f-4480-8941-8d5e18d7801a", name: "New York" },
      current_location: { id: "2a5e350b-c32b-4a3d-8b03-cb8cf2764164", name: "Bremerhaven" },
      scheduled_at: "2025-09-03T07:20:00.000000+00:00",
      delivered_at: null,
      route: { id: "2a2cc74c-9c6b-4ec4-b153-553d90bf5804", name: "Route 14" },
      vehicles: [{ id: "b722faf7-742b-40f3-b954-919cf3405a30", name: "MAERSK DEMO 14", voyage: "341E", role: "MAIN" }],
      containers: [{ id: "3e76081f-533f-4088-a478-8738c0175708", number: "MSKU0496514", status: "IN_TRANSIT" }],
      progress_pct: 60
    },
    {
      id: "a0be2df6-6d2b-4f5e-a2f1-4f6b8c7d9e10",
      ref_no: "SHP0015",
      shipment_type: "LCL",
      status: "CREATED",
      carrier_code: "CMA",
      carrier_name: "CMA CGM",
      origin: { id: "69d99cc1-32cc-4f81-9322-5f3e7dfbe794", name: "Los Angeles" },
      destination: { id: "2a5e350b-c32b-4a3d-8b03-cb8cf2764164", name: "Bremerhaven" },
      current_location: { id: "69d99cc1-32cc-4f81-9322-5f3e7dfbe794", name: "Los Angeles" },
      scheduled_at: "2025-09-04T16:05:00.000000+00:00",
      delivered_at: null,
      route: { id: "cfeb51c6-2bc9-4a61-a687-ccffbfe32444", name: "Route 15" },
      vehicles: [{ id: "762f49d9-412a-4d91-af09-a547410079f7", name: "CMA DEMO 15", voyage: "221W", role: "FEEDER" }],
      containers: [{ id: "a07b8129-1118-4720-833d-ea93a1dc018b", number: "MSKU0496515", status: "GATE_OUT" }],
      progress_pct: 10
    }
  ];

  filteredShipments: Shipment[] = [];

  ngOnInit(): void {
    this.filterShipments();
  }

  applySearch(q: string) {
    this.searchQuery = q ?? '';
    this.filterShipments();
  }

  applyFilter(type: ShipmentType | null) {
    this.selectedType = type ?? null;
    this.filterShipments();
  }

  private filterShipments() {
    const q = this.searchQuery.trim().toLowerCase();

    this.filteredShipments = this.shipments.filter(s => {
      const matchesType = !this.selectedType || s.shipment_type === this.selectedType;

      const haystack = [
        s.id,
        s.ref_no,
        s.shipment_type,
        s.status,
        s.carrier_code,
        s.carrier_name,
        s.origin?.name,
        s.destination?.name,
        s.current_location?.name,
        s.route?.name,
      ]
        .filter(Boolean)
        .join(' ')
        .toLowerCase();

      const matchesQuery = !q || haystack.includes(q);
      return matchesType && matchesQuery;
    });
  }
}
