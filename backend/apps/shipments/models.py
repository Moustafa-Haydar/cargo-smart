import uuid
from django.db import models


class Shipment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ref_no = models.CharField(max_length=80, unique=True)             # metadata.shipmentNumber
    shipment_type = models.CharField(max_length=20)                   # e.g., CT
    status = models.CharField(max_length=30)                          # metadata.shippingStatus
    carrier_code = models.CharField(max_length=10)                    # MAEU
    carrier_name = models.CharField(max_length=120)                   # Maersk
    api_updated_at = models.DateTimeField()
    origin = models.ForeignKey("core.Location", on_delete=models.PROTECT, related_name="shipment_origin_set")
    destination = models.ForeignKey("core.Location", on_delete=models.PROTECT, related_name="shipment_destination_set")
    current_location = models.ForeignKey("core.Location", null=True, blank=True, on_delete=models.SET_NULL, related_name="shipment_current_loc_set")
    route = models.ForeignKey("core.Route", null=True, blank=True, on_delete=models.SET_NULL, related_name="shipments")
    scheduled_at = models.DateTimeField(null=True, blank=True)        # planned POL time if used
    delivered_at = models.DateTimeField(null=True, blank=True)        # set when POD actual achieved

    def __str__(self):
        return self.ref_no


class ShipmentMilestone(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shipment = models.ForeignKey("shipments.Shipment", on_delete=models.CASCADE, related_name="milestones")
    kind = models.CharField(max_length=20)                            # PREPOL | POL | POD | POSTPOD
    location = models.ForeignKey("core.Location", on_delete=models.PROTECT, related_name="shipment_milestones")
    date = models.DateTimeField()                                     # API 'date'
    actual = models.BooleanField(default=False)
    predictive_eta = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.shipment.ref_no} {self.kind} @ {self.location}"


class VehicleLeg(models.Model):
    """shipment_vehicles in ERD."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shipment = models.ForeignKey("shipments.Shipment", on_delete=models.CASCADE, related_name="vehicle_legs")
    vehicle = models.ForeignKey("core.Vehicle", on_delete=models.PROTECT, related_name="shipment_legs")
    voyage = models.CharField(max_length=40)                          # e.g., 344E
    role = models.CharField(max_length=20, blank=True)                # MAIN | FEEDER | BARGE

    class Meta:
        db_table = "shipment_vehicles"

    def __str__(self):
        return f"{self.shipment.ref_no} - {self.vehicle} ({self.voyage})"


class Container(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=20, unique=True)             # ISO 6346
    iso_code = models.CharField(max_length=10)                        # 45G1
    size_type = models.CharField(max_length=40)                       # "40' High Cube Dry"
    status = models.CharField(max_length=30)                          # IN_TRANSIT ...

    def __str__(self):
        return self.number


class ShipmentContainer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shipment = models.ForeignKey("shipments.Shipment", on_delete=models.CASCADE, related_name="shipment_containers")
    container = models.ForeignKey("shipments.Container", on_delete=models.CASCADE, related_name="shipment_links")
    is_active = models.BooleanField(default=True)
    loaded_at = models.DateTimeField(null=True, blank=True)
    discharged_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = (("shipment", "container"),)

    def __str__(self):
        return f"{self.shipment.ref_no} ↔ {self.container.number}"


class ContainerEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    container = models.ForeignKey("shipments.Container", on_delete=models.CASCADE, related_name="events")
    location = models.ForeignKey("core.Location", null=True, blank=True, on_delete=models.SET_NULL, related_name="container_events")
    facility = models.ForeignKey("core.Facility", null=True, blank=True, on_delete=models.SET_NULL, related_name="container_events")
    vehicle = models.ForeignKey("core.Vehicle", null=True, blank=True, on_delete=models.SET_NULL, related_name="container_events")
    voyage = models.CharField(max_length=40, null=True, blank=True)
    description = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20)                      # EQUIPMENT | TRANSPORT
    event_code = models.CharField(max_length=10)                      # GTIN | GTOT | LOAD | DEPA | ...
    status = models.CharField(max_length=10)                          # CEP | CGI | CLL | ...
    route_type = models.CharField(max_length=10)                      # SEA | LAND
    transport_type = models.CharField(max_length=16, null=True, blank=True)  # VESSEL | TRUCK | RAIL | null
    happened_at = models.DateTimeField()                              # API 'date'
    is_actual = models.BooleanField(default=False)
    is_additional = models.BooleanField(default=False)
    source = models.CharField(max_length=60, blank=True)              # which API (optional)
    ingested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["container", "event_code", "happened_at", "location"],
                name="uniq_container_event",
            )
        ]
        indexes = [
            models.Index(fields=["container", "happened_at"], name="ce_container_time_idx"),
        ]
        ordering = ["-happened_at"]

    def __str__(self):
        return f"{self.container.number} {self.event_code} @ {self.happened_at}"
