# === Seed sample logistics data: 3 examples per model ===
# Paste into: python manage.py shell

import json
from datetime import datetime, timezone as tz, timedelta
from django.utils import timezone

from app.models import (
    Location, Facility, Route, RouteSegment,
    Shipment, ShipmentMilestone,
    Vehicle, ShipmentVehicle, VehicleIdentifier, VehiclePosition, PortCall,
    Container, ShipmentContainer, ContainerEvent
)

now = timezone.now()

# ---------- LOCATIONS (3) ----------
houston, _ = Location.objects.get_or_create(
    name="Houston", state="Texas", country="United States", country_code="US",
    locode="USHOU", lat=29.76328, lng=-95.36327, timezone="America/Chicago"
)
bremerhaven, _ = Location.objects.get_or_create(
    name="Bremerhaven", state="Bremen", country="Germany", country_code="DE",
    locode="DEBRV", lat=53.53615, lng=8.59298, timezone="Europe/Berlin"
)
antwerp, _ = Location.objects.get_or_create(
    name="Antwerp", state="Flanders", country="Belgium", country_code="BE",
    locode="BEANR", lat=51.2194, lng=4.4025, timezone="Europe/Brussels"
)

# ---------- FACILITIES (3) ----------
h_barbours, _ = Facility.objects.get_or_create(
    name="Houston Barbours Cut Terminal",
    country_code="US", locode="USUQF",
    bic_code="USUQFGDQQ", smdg_code=None, location=houston
)
msc_bremerhaven, _ = Facility.objects.get_or_create(
    name="MSC Gate Bremerhaven GmbH & Co. KG",
    country_code="DE", locode="", bic_code=None, smdg_code=None, location=bremerhaven
)
psa_antwerp, _ = Facility.objects.get_or_create(
    name="PSA Noordzee Terminal Antwerp",
    country_code="BE", locode="BEANR",
    bic_code="BENZTPSA01", smdg_code=None, location=antwerp
)

# ---------- ROUTES (3) ----------
# Use lightweight GeoJSON strings (you can swap to WKT if you prefer)
route1, _ = Route.objects.get_or_create(
    name="HOU → BRV Sea Route",
    defaults={"geometry": json.dumps({
        "type": "LineString",
        "coordinates": [[-95.36327, 29.76328], [-11.237754, 47.08643], [8.59298, 53.53615]]
    })}
)
route2, _ = Route.objects.get_or_create(
    name="HOU → ANR Sea Route",
    defaults={"geometry": json.dumps({
        "type": "LineString",
        "coordinates": [[-95.36327, 29.76328], [-20.0, 45.0], [4.4025, 51.2194]]
    })}
)
route3, _ = Route.objects.get_or_create(
    name="BRV → ANR Feeder",
    defaults={"geometry": json.dumps({
        "type": "LineString",
        "coordinates": [[8.59298, 53.53615], [6.5, 52.0], [4.4025, 51.2194]]
    })}
)

# ---------- ROUTE SEGMENTS (3 total; 1 per route to keep it simple) ----------
RouteSegment.objects.get_or_create(
    route=route1, seq=1,
    defaults=dict(route_type="SEA", geometry=route1.geometry, mode="VESSEL",
                  eta_start=datetime(2023, 11, 7, 11, 16, tzinfo=tz.utc),
                  eta_end=datetime(2023, 12, 1, 22, 0, tzinfo=tz.utc))
)
RouteSegment.objects.get_or_create(
    route=route2, seq=1,
    defaults=dict(route_type="SEA", geometry=route2.geometry, mode="VESSEL",
                  eta_start=datetime(2023, 11, 10, 10, 0, tzinfo=tz.utc),
                  eta_end=datetime(2023, 12, 3, 18, 0, tzinfo=tz.utc))
)
RouteSegment.objects.get_or_create(
    route=route3, seq=1,
    defaults=dict(route_type="SEA", geometry=route3.geometry, mode="VESSEL",
                  eta_start=datetime(2023, 12, 2, 8, 0, tzinfo=tz.utc),
                  eta_end=datetime(2023, 12, 4, 6, 0, tzinfo=tz.utc))
)

# ---------- SHIPMENTS (3) ----------
sh1, _ = Shipment.objects.get_or_create(
    ref_no="MSKU0496560",
    defaults=dict(
        shipment_type="CT", status="IN_TRANSIT",
        carrier_code="MAEU", carrier_name="Maersk",
        api_updated_at=datetime(2023, 11, 28, 11, 24, 59, tzinfo=tz.utc),
        origin=houston, destination=bremerhaven, current_location=bremerhaven,
        route=route1,
        scheduled_at=datetime(2023, 11, 7, 11, 16, tzinfo=tz.utc),
        delivered_at=None
    )
)
sh2, _ = Shipment.objects.get_or_create(
    ref_no="MSCU2222333",
    defaults=dict(
        shipment_type="CT", status="IN_TRANSIT",
        carrier_code="MSCU", carrier_name="MSC",
        api_updated_at=now - timedelta(days=1),
        origin=houston, destination=antwerp, current_location=None,
        route=route2,
        scheduled_at=datetime(2023, 11, 10, 10, 0, tzinfo=tz.utc),
        delivered_at=None
    )
)
sh3, _ = Shipment.objects.get_or_create(
    ref_no="TGHU7777888",
    defaults=dict(
        shipment_type="CT", status="PLANNED",
        carrier_code="CMDU", carrier_name="CMA CGM",
        api_updated_at=now - timedelta(days=2),
        origin=bremerhaven, destination=antwerp, current_location=None,
        route=route3,
        scheduled_at=datetime(2023, 12, 2, 8, 0, tzinfo=tz.utc),
        delivered_at=None
    )
)

# ---------- SHIPMENT MILESTONES (3) ----------
ShipmentMilestone.objects.get_or_create(
    shipment=sh1, kind="PREPOL", location=houston,
    date=datetime(2023, 11, 7, 11, 16, tzinfo=tz.utc), actual=True, predictive_eta=None
)
ShipmentMilestone.objects.get_or_create(
    shipment=sh1, kind="POL", location=houston,
    date=datetime(2023, 11, 7, 12, 46, tzinfo=tz.utc), actual=True, predictive_eta=None
)
ShipmentMilestone.objects.get_or_create(
    shipment=sh1, kind="POD", location=bremerhaven,
    date=datetime(2023, 12, 1, 22, 0, tzinfo=tz.utc), actual=False, predictive_eta=None
)

# ---------- VEHICLES (3) ----------
v1, _ = Vehicle.objects.get_or_create(
    name="MAERSK OHIO", defaults=dict(
        type="VESSEL", status="SAILING", current_location=bremerhaven,
        route=route1, imo=9298698, mmsi=367775000, call_sign="KABP", flag="US"
    )
)
v2, _ = Vehicle.objects.get_or_create(
    name="MSC SVEVA", defaults=dict(
        type="VESSEL", status="IN_PORT", current_location=antwerp,
        route=route2, imo=9708683, mmsi=636017627, call_sign="D5KY6", flag="LR"
    )
)
v3, _ = Vehicle.objects.get_or_create(
    name="CMA CGM TOSCA", defaults=dict(
        type="VESSEL", status="PLANNED", current_location=None,
        route=route3, imo=9299783, mmsi=228339600, call_sign="FMMM2", flag="FR"
    )
)

# ---------- SHIPMENT ↔ VEHICLE (3) ----------
ShipmentVehicle.objects.get_or_create(shipment=sh1, vehicle=v1, defaults={"voyage": "344E", "role": "Main leg"})
ShipmentVehicle.objects.get_or_create(shipment=sh2, vehicle=v2, defaults={"voyage": "112W", "role": "Main leg"})
ShipmentVehicle.objects.get_or_create(shipment=sh3, vehicle=v3, defaults={"voyage": "205E", "role": "Feeder"})

# ---------- VEHICLE IDENTIFIERS (3) ----------
VehicleIdentifier.objects.get_or_create(vehicle=v1, scheme="CALL_SIGN", value="KABP")
VehicleIdentifier.objects.get_or_create(vehicle=v2, scheme="CALL_SIGN", value="D5KY6")
VehicleIdentifier.objects.get_or_create(vehicle=v3, scheme="CALL_SIGN", value="FMMM2")

# ---------- VEHICLE POSITIONS (3) ----------
VehiclePosition.objects.get_or_create(
    vehicle=v1,
    recorded_at=datetime(2023, 11, 28, 10, 28, tzinfo=tz.utc),
    location=None, lat=51.28157, lng=4.253457, source="AIS"
)
VehiclePosition.objects.get_or_create(
    vehicle=v2,
    recorded_at=now - timedelta(hours=2),
    location=antwerp, lat=51.263, lng=4.34, source="AIS"
)
VehiclePosition.objects.get_or_create(
    vehicle=v3,
    recorded_at=now - timedelta(days=1, hours=5),
    location=bremerhaven, lat=53.54, lng=8.57, source="AIS"
)

# ---------- PORT CALLS (3) ----------
PortCall.objects.get_or_create(
    vehicle=v1, port_location=houston, facility=h_barbours,
    voyage="344E", event="DEPARTURE", label="Vessel departure",
    scheduled_at=datetime(2023, 11, 11, 7, 9, tzinfo=tz.utc),
    actual_at=datetime(2023, 11, 11, 7, 9, tzinfo=tz.utc), status="VDL",
    source_ref="DEPA/GTMS"
)
PortCall.objects.get_or_create(
    vehicle=v1, port_location=bremerhaven, facility=msc_bremerhaven,
    voyage="344E", event="ARRIVAL", label="Vessel arrival",
    scheduled_at=datetime(2023, 12, 1, 22, 0, tzinfo=tz.utc),
    actual_at=None, status="VAD",
    source_ref="ARRI/ETA"
)
PortCall.objects.get_or_create(
    vehicle=v2, port_location=antwerp, facility=psa_antwerp,
    voyage="112W", event="ARRIVAL", label="Vessel arrival",
    scheduled_at=now + timedelta(days=1),
    actual_at=None, status="ETA",
    source_ref="ARRI/ETA"
)

# ---------- CONTAINERS (3) ----------
c1, _ = Container.objects.get_or_create(number="MSKU0496560", defaults=dict(iso_code="45G1", size_type="40' High Cube Dry", status="IN_TRANSIT"))
c2, _ = Container.objects.get_or_create(number="TGHU1111111", defaults=dict(iso_code="22G1", size_type="20' Dry", status="IN_TRANSIT"))
c3, _ = Container.objects.get_or_create(number="MSCU2222222", defaults=dict(iso_code="45R1", size_type="40' High Cube Reefer", status="BOOKED"))

# ---------- SHIPMENT ↔ CONTAINER (3) ----------
ShipmentContainer.objects.get_or_create(shipment=sh1, container=c1, defaults={"is_active": True, "loaded_at": datetime(2023, 11, 11, 4, 57, tzinfo=tz.utc), "discharged_at": None})
ShipmentContainer.objects.get_or_create(shipment=sh2, container=c2, defaults={"is_active": True, "loaded_at": now - timedelta(days=15), "discharged_at": None})
ShipmentContainer.objects.get_or_create(shipment=sh3, container=c3, defaults={"is_active": False, "loaded_at": None, "discharged_at": None})

# ---------- CONTAINER EVENTS (3) ----------
# Mirror the API example where possible
ContainerEvent.objects.get_or_create(
    container=c1, location=houston, facility=h_barbours, vehicle=None, voyage=None,
    description="Gate out", event_type="EQUIPMENT", event_code="GTOT", status="CEP",
    route_type="LAND", transport_type=None,
    happened_at=datetime(2023, 11, 7, 11, 16, tzinfo=tz.utc),
    is_actual=True, is_additional=False, source="SINAY_API",
    ingested_at=datetime(2023, 11, 28, 11, 24, 59, tzinfo=tz.utc)
)
ContainerEvent.objects.get_or_create(
    container=c1, location=houston, facility=None, vehicle=None, voyage=None,
    description="Gate in", event_type="EQUIPMENT", event_code="GTIN", status="CGI",
    route_type="LAND", transport_type=None,
    happened_at=datetime(2023, 11, 7, 12, 46, tzinfo=tz.utc),
    is_actual=True, is_additional=False, source="SINAY_API",
    ingested_at=datetime(2023, 11, 28, 11, 24, 59, tzinfo=tz.utc)
)
ContainerEvent.objects.get_or_create(
    container=c1, location=houston, facility=None, vehicle=v1, voyage="344E",
    description="Load", event_type="EQUIPMENT", event_code="LOAD", status="CLL",
    route_type="SEA", transport_type="VESSEL",
    happened_at=datetime(2023, 11, 11, 4, 57, tzinfo=tz.utc),
    is_actual=True, is_additional=False, source="SINAY_API",
    ingested_at=datetime(2023, 11, 28, 11, 24, 59, tzinfo=tz.utc)
)

