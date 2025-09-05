import uuid
from django.db import models

class Route(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    geometry = models.TextField()  # WKT/GeoJSON string (can move to GIS later)

    def __str__(self):
        return self.name


class RouteSegment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    route = models.ForeignKey("routes.Route", on_delete=models.CASCADE, related_name="segments")
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
