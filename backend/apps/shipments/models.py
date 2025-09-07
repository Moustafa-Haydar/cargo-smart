import uuid
from django.db import models
from django.conf import settings
from django.apps import apps

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
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_shipments")

    scheduled_at = models.DateTimeField()
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.ref_no

    def create_notification(self, notification_type, message):
        """Helper method to create notifications after shipment exists"""
        # Get the model class dynamically to avoid circular imports
        ShipmentNotification = apps.get_model('shipments', 'ShipmentNotification')
        ShipmentNotification.objects.create(
            shipment=self,
            notification_type=notification_type,
            message=message
        )

    def save(self, *args, **kwargs):
        # Store if this is a new instance
        is_new = self.pk is None
        
        if not is_new:
            # Get old values directly from database
            old_values = type(self).objects.filter(pk=self.pk).values(
                'route_id', 'status', 'driver_id'
            ).first()
        
        # Call the original save method first
        super().save(*args, **kwargs)
        
        try:
            # Now create notifications after the instance exists
            if is_new:
                # Create initial notifications for new shipment
                if self.driver:
                    self.create_notification(
                        'DRIVER_CHANGE',
                        f'Initial driver assigned to shipment {self.ref_no}'
                    )
                if self.route:
                    self.create_notification(
                        'ROUTE_CHANGE',
                        f'Initial route assigned to shipment {self.ref_no}'
                    )
            else:
                # Create notifications for changes
                if old_values['route_id'] != self.route_id:
                    self.create_notification(
                        'ROUTE_CHANGE',
                        f'Route updated for shipment {self.ref_no}'
                    )
                
                if old_values['status'] != self.status:
                    self.create_notification(
                        'STATUS_CHANGE',
                        f'Status updated to {self.status}'
                    )
                
                if old_values['driver_id'] != self.driver_id:
                    self.create_notification(
                        'DRIVER_CHANGE',
                        f'Driver updated for shipment {self.ref_no}'
                    )
        except Exception as e:
            # Log notification errors but don't prevent shipment save
            print(f"Error creating notification: {str(e)}")


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


class ShipmentNotification(models.Model):
    NOTIFICATION_TYPES = [
        ('ROUTE_CHANGE', 'Route Change'),
        ('STATUS_CHANGE', 'Status Change'),
        ('DRIVER_CHANGE', 'Driver Change'),
        ('MILESTONE_REACHED', 'Milestone Reached'),
        ('DELAY', 'Delay')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shipment = models.ForeignKey("shipments.Shipment", on_delete=models.CASCADE, related_name="notifications")
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.notification_type} - {self.shipment.ref_no}"