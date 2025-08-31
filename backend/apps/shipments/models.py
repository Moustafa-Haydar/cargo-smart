import uuid
from django.db import models

# ---------- Locations & Facilities ----------

class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100)
    country_code = models.CharField(max_length=3)
    locode = models.CharField(max_length=10, blank=True)
    lat = models.FloatField()
    lng = models.FloatField()
    timezone = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name} ({self.country_code})"


class Facility(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    country_code = models.CharField(max_length=3)
    locode = models.CharField(max_length=10, blank=True)
    bic_code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    smdg_code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="facilities")

    def __str__(self):
        return self.name


# ---------- Routes ----------

class Route(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    geometry = models.TextField()  # store WKT/GeoJSON string (swap to GIS later)

    def __str__(self):
        return self.name


class RouteSegment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="segments")
    seq = models.PositiveIntegerField()
    route_type = models.CharField(max_length=50)
    geometry = models.TextField()
    mode = models.CharField(max_length=50)
    eta_start = models.DateTimeField(null=True, blank=True)
    eta_end = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["route", "seq"], name="uniq_route_seq")
        ]
        ordering = ["seq"]


# ---------- Shipments & Milestones ----------

class Shipment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ref_no = models.CharField(max_length=64, unique=True)
    shipment_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    carrier_code = models.CharField(max_length=20, blank=True)
    carrier_name = models.CharField(max_length=100, blank=True)
    api_updated_at = models.DateTimeField(null=True, blank=True)

    origin = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="origin_shipments")
    destination = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="destination_shipments")
    current_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name="current_shipments")
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True, related_name="shipments")

    scheduled_at = models.DateTimeField()
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.ref_no


class ShipmentMilestone(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name="milestones")
    kind = models.CharField(max_length=20)  # PREPOL | POL | POD | POSTPOD
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="shipment_milestones")
    date = models.DateTimeField()
    actual = models.BooleanField(default=False)
    predictive_eta = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.kind} - {self.shipment.ref_no}"


# ---------- Vehicles & Movement ----------

class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    current_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name="vehicles_here")
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True, related_name="vehicles")
    imo = models.BigIntegerField(unique=True, null=True, blank=True)
    mmsi = models.BigIntegerField(unique=True, null=True, blank=True)
    call_sign = models.CharField(max_length=50, blank=True)
    flag = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class ShipmentVehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name="shipment_vehicles")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="shipment_vehicles")
    voyage = models.CharField(max_length=50, blank=True)
    role = models.CharField(max_length=50, blank=True)


class VehicleIdentifier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="identifiers")
    scheme = models.CharField(max_length=50)
    value = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["scheme", "value"], name="uniq_vehicle_identifier")
        ]


class VehiclePosition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="positions")
    recorded_at = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name="vehicle_positions")
    lat = models.FloatField()
    lng = models.FloatField()
    source = models.CharField(max_length=50)

    class Meta:
        indexes = [
            models.Index(fields=["vehicle", "recorded_at"], name="idx_vehicle_recorded_at"),
        ]


class PortCall(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="port_calls")
    port_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="port_calls")
    facility = models.ForeignKey('Facility', on_delete=models.SET_NULL, null=True, blank=True, related_name="port_calls")
    voyage = models.CharField(max_length=50, blank=True)
    event = models.CharField(max_length=50)
    label = models.CharField(max_length=100, blank=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    actual_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50)
    source_ref = models.CharField(max_length=100, blank=True)


# ---------- Containers & Events ----------

class Container(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=20, unique=True)
    iso_code = models.CharField(max_length=10)
    size_type = models.CharField(max_length=20)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.number


class ShipmentContainer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name="shipment_containers")
    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name="shipment_containers")
    is_active = models.BooleanField(default=True)
    loaded_at = models.DateTimeField(null=True, blank=True)
    discharged_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["shipment", "container"], name="uniq_shipment_container")
        ]


class ContainerEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name="events")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name="container_events")
    facility = models.ForeignKey(Facility, on_delete=models.SET_NULL, null=True, blank=True, related_name="container_events")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name="container_events")
    voyage = models.CharField(max_length=50, blank=True, null=True)

    description = models.TextField(blank=True)
    event_type = models.CharField(max_length=50)
    event_code = models.CharField(max_length=20)
    status = models.CharField(max_length=50)
    route_type = models.CharField(max_length=50)
    transport_type = models.CharField(max_length=50, null=True, blank=True)

    happened_at = models.DateTimeField()
    is_actual = models.BooleanField(default=False)
    is_additional = models.BooleanField(default=False)
    source = models.CharField(max_length=50)
    ingested_at = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["container", "event_code", "happened_at", "location", "source"],
                name="uniq_container_event_fingerprint",
            )
        ]
