import uuid
from django.db import models


class Route(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    geometry = models.TextField()  # Polyline/GeoJSON string

    def __str__(self):
        return self.name


class RouteSegment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="segments")
    seq = models.PositiveIntegerField()
    geometry = models.TextField()
    eta_start = models.DateTimeField(null=True, blank=True)
    eta_end = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("route", "seq")
        ordering = ["seq"]

    def __str__(self):
        return f"{self.route.name} - Segment {self.seq}"
