from django.db import models
import uuid

class AgentDecision(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    shipment_id = models.UUIDField(db_index=True)
    current_route_id = models.UUIDField(null=True, blank=True)
    proposed_route_id = models.UUIDField(null=True, blank=True)
    input_snapshot = models.JSONField()    # features + context
    output_decision = models.JSONField()   # scores, choice, rationale
    approved = models.BooleanField(null=True)  # None=pending, True/False

class RouteProposal(models.Model):
    """
    Store route proposals from n8n for frontend display
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shipment_id = models.UUIDField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Proposal data from n8n
    action = models.CharField(max_length=20)  # 'propose_switch' or 'stick'
    current_route_id = models.UUIDField(null=True, blank=True)
    current_eta_minutes = models.IntegerField(null=True, blank=True)
    current_toll_cost_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_path = models.JSONField(null=True, blank=True)
    current_p_delay = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    
    # Proposed alternative
    proposed_route_id = models.UUIDField(null=True, blank=True)
    proposed_eta_minutes = models.IntegerField(null=True, blank=True)
    proposed_toll_cost_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    proposed_path = models.JSONField(null=True, blank=True)
    proposed_p_delay = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    
    rationale = models.TextField()
    requires_approval = models.BooleanField(default=True)
    
    # Status tracking
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('applied', 'Applied'),
    ])
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['shipment_id', 'status']),
        ]
