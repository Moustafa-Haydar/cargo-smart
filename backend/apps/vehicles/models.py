import uuid
from django.db import models


class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plate_number = models.CharField(max_length=20, unique=True)
    model = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=50, default="ACTIVE")  # ACTIVE, IN_TRANSIT, MAINTENANCE
    current_location = models.ForeignKey(
        "geo.Location", on_delete=models.SET_NULL, null=True, blank=True, related_name="vehicles_here"
    )
    route = models.ForeignKey("routes.Route", on_delete=models.SET_NULL, null=True, blank=True, related_name="vehicles")

    def __str__(self):
        return self.plate_number


class VehicleIdentifier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="identifiers")
    scheme = models.CharField(max_length=50)  # e.g., VIN, RFID
    value = models.CharField(max_length=100)

    class Meta:
        unique_together = ("scheme", "value")

    def __str__(self):
        return f"{self.scheme}: {self.value}"


class VehiclePosition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="positions")
    recorded_at = models.DateTimeField()
    location = models.ForeignKey("geo.Location", on_delete=models.SET_NULL, null=True, blank=True, related_name="vehicle_positions")
    lat = models.FloatField()
    lng = models.FloatField()
    source = models.CharField(max_length=50)

    class Meta:
        indexes = [models.Index(fields=["vehicle", "recorded_at"], name="idx_vehicle_recorded_at")]

    def __str__(self):
        return f"{self.vehicle.plate_number} @ {self.recorded_at}"
