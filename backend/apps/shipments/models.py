import uuid
from django.db import models

class Shipment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ref_no = models.CharField(max_length=64, unique=True)
    shipment_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    carrier_code = models.CharField(max_length=20, blank=True)
    carrier_name = models.CharField(max_length=100, blank=True)
    api_updated_at = models.DateTimeField(null=True, blank=True)

    origin = models.ForeignKey("geo.Location", on_delete=models.PROTECT, related_name="origin_shipments")
    destination = models.ForeignKey("geo.Location", on_delete=models.PROTECT, related_name="destination_shipments")
    current_location = models.ForeignKey("geo.Location", on_delete=models.SET_NULL, null=True, blank=True, related_name="current_shipments")
    route = models.ForeignKey("routes.Route", on_delete=models.SET_NULL, null=True, blank=True, related_name="shipments")

    scheduled_at = models.DateTimeField()
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.ref_no


class ShipmentMilestone(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shipment = models.ForeignKey("shipments.Shipment", on_delete=models.CASCADE, related_name="milestones")
    kind = models.CharField(max_length=20)  # PREPOL | POL | POD | POSTPOD
    location = models.ForeignKey("geo.Location", on_delete=models.PROTECT, related_name="shipment_milestones")
    date = models.DateTimeField()
    actual = models.BooleanField(default=False)
    predictive_eta = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.kind} - {self.shipment.ref_no}"


class ShipmentVehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shipment = models.ForeignKey("shipments.Shipment", on_delete=models.CASCADE, related_name="shipment_vehicles")
    vehicle = models.ForeignKey("vehicles.Vehicle", on_delete=models.CASCADE, related_name="shipment_vehicles")
    voyage = models.CharField(max_length=50, blank=True)
    role = models.CharField(max_length=50, blank=True)


class ShipmentContainer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shipment = models.ForeignKey("shipments.Shipment", on_delete=models.CASCADE, related_name="shipment_containers")
    container = models.ForeignKey("containers.Container", on_delete=models.CASCADE, related_name="shipment_containers")
    is_active = models.BooleanField(default=True)
    loaded_at = models.DateTimeField(null=True, blank=True)
    discharged_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["shipment", "container"], name="uniq_shipment_container")
        ]
