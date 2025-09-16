from django.db import models

class AgentDecision(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    shipment_id = models.UUIDField(db_index=True)
    current_route_id = models.UUIDField(null=True, blank=True)
    proposed_route_id = models.UUIDField(null=True, blank=True)
    input_snapshot = models.JSONField()    # features + context
    output_decision = models.JSONField()   # scores, choice, rationale
    approved = models.BooleanField(null=True)  # None=pending, True/False
