import uuid
from django.db import models


class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=120)
    country_code = models.CharField(max_length=2)
    locode = models.CharField(max_length=10, blank=True)  # UN/LOCODE (e.g., USHOU)
    lat = models.FloatField()
    lng = models.FloatField()
    timezone = models.CharField(max_length=64)

    class Meta:
        indexes = [models.Index(fields=["locode"], name="locode_idx")]

    def __str__(self):
        return f"{self.name} ({self.country_code})"


class Route(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    geometry = models.TextField()  # WKT/GeoJSON/encoded polyline

    def __str__(self):
        return self.name


class RouteSegment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    route = models.ForeignKey("core.Route", on_delete=models.CASCADE, related_name="segments")
    seq = models.PositiveIntegerField()
    route_type = models.CharField(max_length=16)  # SEA | LAND | RAIL | AIR
    geometry = models.TextField()
    mode = models.CharField(max_length=16, blank=True)  # VESSEL/TRUCK/RAIL
    eta_start = models.DateTimeField(null=True, blank=True)
    eta_end = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["route", "seq"], name="route_seq_idx")]
        ordering = ["route", "seq"]

    def __str__(self):
        return f"{self.route} seg {self.seq}"


class Facility(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    country_code = models.CharField(max_length=2)
    locode = models.CharField(max_length=10, blank=True)  # facility sub-code if provided
    bic_code = models.CharField(max_length=11, null=True, blank=True, unique=True)
    smdg_code = models.CharField(max_length=11, null=True, blank=True, unique=True)
    location = models.ForeignKey("core.Location", on_delete=models.CASCADE, related_name="facilities")

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=32)   # VESSEL | TRUCK | TRAIN | ...
    status = models.CharField(max_length=32)
    current_location = models.ForeignKey("core.Location", null=True, blank=True, on_delete=models.SET_NULL, related_name="current_vehicles")
    route = models.ForeignKey("core.Route", null=True, blank=True, on_delete=models.SET_NULL, related_name="vehicles")
    imo = models.BigIntegerField(null=True, blank=True, unique=True)
    mmsi = models.BigIntegerField(null=True, blank=True, unique=True)
    call_sign = models.CharField(max_length=50, blank=True)
    flag = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return self.name


class VehicleIdentifier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey("core.Vehicle", on_delete=models.CASCADE, related_name="identifiers")
    scheme = models.CharField(max_length=30)  # IMO | MMSI | CALLSIGN | VIN | ...
    value = models.CharField(max_length=120)

    class Meta:
        unique_together = (("scheme", "value"),)

    def __str__(self):
        return f"{self.scheme}:{self.value}"


class VehiclePosition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey("core.Vehicle", on_delete=models.CASCADE, related_name="positions")
    recorded_at = models.DateTimeField()
    location = models.ForeignKey("core.Location", null=True, blank=True, on_delete=models.SET_NULL, related_name="vehicle_positions")
    lat = models.FloatField()
    lng = models.FloatField()
    source = models.CharField(max_length=60, blank=True)

    class Meta:
        indexes = [models.Index(fields=["vehicle", "recorded_at"], name="vehpos_time_idx")]
        ordering = ["-recorded_at"]

    def __str__(self):
        return f"{self.vehicle} @ {self.recorded_at}"


class PortCall(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey("core.Vehicle", on_delete=models.CASCADE, related_name="port_calls")
    port_location = models.ForeignKey("core.Location", on_delete=models.CASCADE, related_name="port_calls")
    facility = models.ForeignKey("core.Facility", null=True, blank=True, on_delete=models.SET_NULL, related_name="port_calls")
    voyage = models.CharField(max_length=40)
    event = models.CharField(max_length=16)   # ARRIVAL | DEPARTURE
    label = models.CharField(max_length=8)    # ETA | ATA | ETD | ATD
    scheduled_at = models.DateTimeField(null=True, blank=True)
    actual_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, blank=True)  # OK/DELAYED/CANCELLED...
    source_ref = models.CharField(max_length=120, blank=True)

    class Meta:
        indexes = [models.Index(fields=["vehicle", "scheduled_at"], name="portcall_sched_idx")]
        ordering = ["-scheduled_at"]

    def __str__(self):
        return f"{self.vehicle} {self.event} {self.port_location}"
