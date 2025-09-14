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

export interface VehicleInfo {
  id: string;
  plate_number: string;
  model: string;
  status: string;
}

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
  status: ShipmentStatus | string;
  carrier_name: string;
  origin: NamedEntity;
  destination: NamedEntity;
  current_location: NamedEntity;
  scheduled_at: ISODateTime;
  delivered_at: ISODateTime | null;
  route: NamedEntity;
  vehicle: VehicleInfo | null;  // Direct vehicle assignment
  api_updated_at?: ISODateTime;
  milestones?: Milestone[];
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

// Full vehicle entity (updated to match backend)
export interface TransportVehicle {
  id: string;
  plate_number: string;
  model: string;
  status: string;                     // e.g., "ACTIVE", "IN_TRANSIT", "MAINTENANCE"

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
  geometry: string;          // WKT/GeoJSON string (as in your example)
  eta_start: ISODateTime | null;
  eta_end: ISODateTime | null;
}

// In the route example, `vehicles` inside a route are small refs
export interface RouteVehicleRef {
  id: string;
  plate_number: string;
  model: string;
  status: string;
}

// Full Route entity
export interface Route {
  id: string;
  name: string;
  geometry: string;           // stored as stringified GeoJSON or WKT
  segments: RouteSegment[];

  shipments?: RouteShipmentRef[];     // may be empty or omitted
  vehicles?: RouteVehicleRef[];
}

// Route shipment reference (simplified shipment info in routes)
export interface RouteShipmentRef {
  id: string;
  ref_no: string;
  status: string;
  carrier_name: string;
  origin_id: string;
  destination_id: string;
  scheduled_at: ISODateTime;
  vehicle: VehicleInfo | null;
}

// Envelope if your API returns { routes: [...] }
export interface RoutesResponse {
  routes: Route[];
}

export interface GeoLocation {
  id: string;          // UUID
  name: string;
  state?: string;      // optional because blank=True
  country: string;
  country_code: string;
  locode?: string;     // optional because blank=True
  lat: number;
  lng: number;
  timezone: string;
}