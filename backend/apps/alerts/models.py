import uuid
from django.conf import settings
from django.db import models
from apps.shipments.models import Shipment, Vehicle, Route

class Alert(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=50)
    severity = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resolved_alerts",
    )

    shipment = models.ForeignKey(Shipment, on_delete=models.SET_NULL, null=True, blank=True, related_name="alerts")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name="alerts")
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True, related_name="alerts")

    def __str__(self):
        return f"[{self.severity}] {self.type}"
