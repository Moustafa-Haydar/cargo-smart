import random
from django.core.management.base import BaseCommand
from apps.alerts.models import Alert
from apps.shipments.models import Shipment
from apps.vehicles.models import Vehicle
from apps.routes.models import Route

class Command(BaseCommand):
    help = "Seed 10 Alerts (optionally linked to shipments/vehicles/routes)."

    def add_arguments(self, parser):
        parser.add_argument("--fresh", action="store_true")

    def handle(self, *args, **opts):
        if opts["fresh"]:
            Alert.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared alerts data"))

        random.seed(42)
        shipments = list(Shipment.objects.all())
        vehicles = list(Vehicle.objects.all())
        routes = list(Route.objects.all())

        for i in range(10):
            Alert.objects.create(
                type=random.choice(["DELAY","ROUTE_DEVIATION","PORT_CONGESTION","CUSTOMS_HOLD"]),
                severity=random.choice(["LOW","MEDIUM","HIGH"]),
                status=random.choice(["OPEN","ACK","RESOLVED"]) if i % 3 else "OPEN",
                message=random.choice([
                    "ETA slipped by 12 hours.",
                    "Vessel deviated from planned route.",
                    "Port congestion reported.",
                    "Customs inspection required."
                ]),
                shipment=(shipments[i] if i < len(shipments) else (random.choice(shipments) if shipments else None)),
                vehicle=(vehicles[i] if i < len(vehicles) else (random.choice(vehicles) if vehicles else None)),
                route=(routes[i] if i < len(routes) else (random.choice(routes) if routes else None)),
            )

        self.stdout.write(self.style.SUCCESS("Seeded alerts (10)."))
