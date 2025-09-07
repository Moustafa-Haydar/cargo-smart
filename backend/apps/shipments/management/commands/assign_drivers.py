import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from apps.shipments.models import Shipment

class Command(BaseCommand):
    help = 'Assigns drivers to shipments randomly'

    def handle(self, *args, **options):
        # Get the drivers group
        try:
            drivers_group = Group.objects.get(name='Driver')
        except Group.DoesNotExist:
            self.stdout.write(self.style.ERROR('Drivers group does not exist'))
            return

        # Get all users in the drivers group
        drivers = User.objects.filter(groups=drivers_group)
        
        if not drivers.exists():
            self.stdout.write(self.style.ERROR('No drivers found in the drivers group'))
            return

        # Get all unassigned shipments
        unassigned_shipments = Shipment.objects.filter(driver__isnull=True)
        
        if not unassigned_shipments.exists():
            self.stdout.write(self.style.SUCCESS('No unassigned shipments found'))
            return

        drivers_list = list(drivers)
        assigned_count = 0

        # Assign drivers randomly to shipments
        for shipment in unassigned_shipments:
            driver = random.choice(drivers_list)
            shipment.driver = driver
            shipment.save()
            assigned_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully assigned {assigned_count} shipments to {len(drivers_list)} drivers'
            )
        )
