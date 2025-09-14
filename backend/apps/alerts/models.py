import uuid
from django.db import models


class Alert(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=50)      # e.g., DELAY, BREAKDOWN
    severity = models.CharField(max_length=20)  # LOW, MEDIUM, HIGH
    status = models.CharField(max_length=20, default="OPEN")
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    resolved_by = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="resolved_alerts")
    shipment = models.ForeignKey("shipments.Shipment", on_delete=models.CASCADE, related_name="alerts")
    vehicle = models.ForeignKey("vehicles.Vehicle", on_delete=models.CASCADE, related_name="alerts")
    route = models.ForeignKey("routes.Route", on_delete=models.CASCADE, related_name="alerts")

    def __str__(self):
        return f"{self.type} - {self.status}"
