from django.core.management.base import BaseCommand
from apps.shipments.models import Shipment

class Command(BaseCommand):
    help = 'Lists all shipments (driver assignment not supported in current model)'

    def handle(self, *args, **options):
        # Get all shipments
        shipments = Shipment.objects.all()
        
        if not shipments.exists():
            self.stdout.write(self.style.WARNING('No shipments found'))
            return

        self.stdout.write(f'Found {shipments.count()} shipments:')
        for shipment in shipments:
            self.stdout.write(f'  - {shipment.ref_no} ({shipment.status}) - {shipment.carrier_name}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Total shipments: {shipments.count()}'
            )
        )
