// ------------------------------
// Logistics domain models
// ------------------------------

export type ISODateTime = string;

// Common small named entity (id + label)
export interface NamedEntity {
  id: string;
  name: string;
}

/* =========================================
 *  Shipments
 * =======================================*/

export type ShipmentType = 'LCL' | 'CT' | 'BBK';
export type ShipmentStatus = 'CREATED' | 'IN_TRANSIT' | 'DELIVERED';

// Milestones as used by shipments (optional in case your payload omits them)
export type MilestoneKind = 'POL' | 'POD' | 'POSTPOD';

export interface Milestone {
  id: string;
  kind: MilestoneKind;
  date: ISODateTime;              // actual or planned timestamp
  actual: boolean;                // true if event happened
  predictive_eta: ISODateTime | null;
  location: string;               // human label (e.g., "Shanghai")
}

export type VehicleRole = 'MAIN' | 'FEEDER';

export interface ShipmentVehicleRef {
  id: string;
  name: string;
  voyage?: string;
  role?: VehicleRole;
}

export type ContainerStatus = 'GATE_IN' | 'GATE_OUT' | 'IN_TRANSIT' | 'ARRIVED' | 'LOADED';

export interface Container {
  id: string;
  number: string;
  status: ContainerStatus;
}

export interface Shipment {
  id: string;
  ref_no: string;
  shipment_type: ShipmentType | string;
  status: ShipmentStatus | string;
  carrier_code: string;
  carrier_name: string;
  origin: NamedEntity;
  destination: NamedEntity;
  current_location: NamedEntity;
  scheduled_at: ISODateTime;
  delivered_at: ISODateTime | null;
  route: NamedEntity;
  api_updated_at?: ISODateTime;
  milestones?: Milestone[];
  vehicles: ShipmentVehicleRef[];
  containers: Container[];
  progress_pct?: number;
}

// Envelope if your API returns { shipments: [...] }
export interface ShipmentsResponse {
  shipments: Shipment[];
}

/* =========================================
 *  Vehicles (full entity)
 * =======================================*/

export type VehicleType = 'VESSEL' | 'TRUCK' | 'PLANE';
export type VehicleOperationalStatus = 'IDLE' | 'AT_PORT' | 'UNDERWAY' | 'OUT_OF_SERVICE';

export interface Identifier {
  scheme: string; // e.g., "IMO"
  value: string;  // e.g., "9298004"
}

export interface Position {
  id?: string;
  recorded_at: ISODateTime;
  lat: number;
  lng: number;
  source?: string;     // e.g., "SEED"
  location?: string;   // human label
}

export type PortCallEvent = 'ARRIVAL' | 'DEPARTURE';
export type PortCallStatus = 'PLANNED' | 'COMPLETED' | 'CANCELLED';

export interface PortCall {
  id: string;
  voyage?: string;
  event: PortCallEvent;         // e.g., "DEPARTURE"
  label?: string;               // e.g., "Vessel arrival"
  scheduled_at: ISODateTime | null;
  actual_at: ISODateTime | null;
  status: PortCallStatus;       // e.g., "PLANNED"
  source_ref?: string;

  port_location: NamedEntity;   // e.g., port name/id
  facility?: NamedEntity;       // e.g., terminal
}

// Full vehicle entity (from your "vehicle" example)
export interface TransportVehicle {
  id: string;
  name: string;
  type: VehicleType;                  // e.g., "VESSEL"
  status: VehicleOperationalStatus;   // e.g., "IDLE"

  // Maritime identifiers (present for vessels)
  imo?: number;
  mmsi?: number;
  call_sign?: string;
  flag?: string;                      // e.g., "BE"

  current_location: NamedEntity;
  route: NamedEntity;

  identifiers: Identifier[];
  last_position?: Position;
  positions?: Position[];
  port_calls?: PortCall[];
}

// Envelope if your API returns { vehicles: [...] }
export interface VehiclesResponse {
  vehicles: TransportVehicle[];
}

/* =========================================
 *  Routes
 * =======================================*/

export type RouteType = 'LAND' | 'SEA' | 'AIR';
export type TransportMode = 'VESSEL' | 'TRUCK' | 'PLANE';

export interface RouteSegment {
  id: string;
  seq: number;
  route_type: RouteType;     // e.g., "LAND", "SEA"
  geometry: string;          // WKT/GeoJSON string (as in your example)
  mode: TransportMode;       // e.g., "VESSEL", "TRUCK"
  eta_start: ISODateTime | null;
  eta_end: ISODateTime | null;
}

// In the route example, `vehicles` inside a route are small refs
export interface RouteVehicleRef {
  id: string;
  name: string;
  type: VehicleType;
  status: VehicleOperationalStatus | 'AT_PORT'; // example shows AT_PORT
}

// Full Route entity
export interface Route {
  id: string;
  name: string;
  geometry: string;           // stored as stringified GeoJSON or WKT
  segments: RouteSegment[];

  // The example shows empty arrays; types included for completeness:
  shipments?: Shipment[];     // may be empty or omitted
  vehicles?: RouteVehicleRef[];
}

// Envelope if your API returns { routes: [...] }
export interface RoutesResponse {
  routes: Route[];
}
