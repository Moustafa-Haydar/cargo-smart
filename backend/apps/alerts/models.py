import uuid
from django.conf import settings
from django.db import models


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
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="resolved_alerts"
    )
    shipment = models.ForeignKey("shipments.Shipment", null=True, blank=True, on_delete=models.SET_NULL, related_name="alerts")
    vehicle = models.ForeignKey("core.Vehicle", null=True, blank=True, on_delete=models.SET_NULL, related_name="alerts")
    route = models.ForeignKey("core.Route", null=True, blank=True, on_delete=models.SET_NULL, related_name="alerts")

    class Meta:
        indexes = [models.Index(fields=["status", "severity"], name="alert_state_idx")]
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.severity}/{self.status}] {self.type}"
