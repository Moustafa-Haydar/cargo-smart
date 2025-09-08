export interface Location {
    id: string;
    name: string;
}

export interface Route {
    id: string;
    name: string;
}

export interface Driver {
    id: string;
    name: string;
}

export interface Milestone {
    id: string;
    kind: string;
    location: Location;
    date: string;
    actual: boolean;
    predictive_eta: string | null;
}

export interface Container {
    id: string;
    container: {
        id: string;
        number: string;
    };
    is_active: boolean;
    loaded_at: string;
    discharged_at: string | null;
}

export interface VehicleHealth {
    status: 'excellent' | 'attention' | 'critical';
    percentage: number;
}

export interface Vehicle {
    id: string;
    type: 'truck' | 'container';
    route: string;
    mileage: number;
    health: VehicleHealth;
}

export interface Shipment {
    id: string;
    ref_no: string;
    shipment_type: string;
    status: string;
    carrier_code: string;
    carrier_name: string;
    api_updated_at: string;
    origin: Location;
    destination: Location;
    current_location: Location;
    route: Route;
    driver: Driver;
    scheduled_at: string;
    delivered_at: string | null;
    milestones: Milestone[];
    vehicles: Vehicle[];
    containers: Container[];
}

export interface ShipmentsResponse {
    shipments: Shipment[];
}

export interface ShipmentStatus {
    status: 'Delivered' | 'In-Transit' | 'Delayed';
    percentage: number;
}

export interface ShipmentDisplayData {
    id: string;
    ref_no: string;
    type: string;
    origin: string;
    destination: string;
    status: ShipmentStatus;
    eta?: string;
    deliveryDate?: string;
    daysRemaining?: number;
    carrier_name: string;
    current_location: string;
    originalStatus: string; // Keep original API status for counting
}
