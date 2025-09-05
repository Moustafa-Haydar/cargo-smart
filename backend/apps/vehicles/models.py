import uuid
from django.db import models

class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    current_location = models.ForeignKey("geo.Location", on_delete=models.SET_NULL, null=True, blank=True, related_name="vehicles_here")
    route = models.ForeignKey("routes.Route", on_delete=models.SET_NULL, null=True, blank=True, related_name="vehicles")
    imo = models.BigIntegerField(unique=True, null=True, blank=True)
    mmsi = models.BigIntegerField(unique=True, null=True, blank=True)
    call_sign = models.CharField(max_length=50, blank=True)
    flag = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class VehicleIdentifier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey("vehicles.Vehicle", on_delete=models.CASCADE, related_name="identifiers")
    scheme = models.CharField(max_length=50)
    value = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["scheme", "value"], name="uniq_vehicle_identifier")
        ]


class VehiclePosition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey("vehicles.Vehicle", on_delete=models.CASCADE, related_name="positions")
    recorded_at = models.DateTimeField()
    location = models.ForeignKey("geo.Location", on_delete=models.SET_NULL, null=True, blank=True, related_name="vehicle_positions")
    lat = models.FloatField()
    lng = models.FloatField()
    source = models.CharField(max_length=50)

    class Meta:
        indexes = [
            models.Index(fields=["vehicle", "recorded_at"], name="idx_vehicle_recorded_at"),
        ]


class PortCall(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey("vehicles.Vehicle", on_delete=models.CASCADE, related_name="port_calls")
    port_location = models.ForeignKey("geo.Location", on_delete=models.PROTECT, related_name="port_calls")
    facility = models.ForeignKey("geo.Facility", on_delete=models.SET_NULL, null=True, blank=True, related_name="port_calls")
    voyage = models.CharField(max_length=50, blank=True)
    event = models.CharField(max_length=50)
    label = models.CharField(max_length=100, blank=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    actual_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50)
    source_ref = models.CharField(max_length=100, blank=True)
