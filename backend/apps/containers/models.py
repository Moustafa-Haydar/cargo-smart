import uuid
from django.db import models

class Container(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=20, unique=True)
    iso_code = models.CharField(max_length=10)
    size_type = models.CharField(max_length=20)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.number


class ContainerEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    container = models.ForeignKey("containers.Container", on_delete=models.CASCADE, related_name="events")
    location = models.ForeignKey("geo.Location", on_delete=models.SET_NULL, null=True, blank=True, related_name="container_events")
    facility = models.ForeignKey("geo.Facility", on_delete=models.SET_NULL, null=True, blank=True, related_name="container_events")
    vehicle = models.ForeignKey("vehicles.Vehicle", on_delete=models.SET_NULL, null=True, blank=True, related_name="container_events")
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
        indexes = [
            models.Index(fields=["container", "happened_at"], name="idx_container_event_timeline"),
        ]
