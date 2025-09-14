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

        if not shipments:
            self.stdout.write(self.style.ERROR("No shipments found. Run seed_shipments first."))
            return
        if not vehicles:
            self.stdout.write(self.style.ERROR("No vehicles found. Run seed_vehicles first."))
            return
        if not routes:
            self.stdout.write(self.style.ERROR("No routes found. Run seed_routes first."))
            return

        total_created = 0
        for i in range(10):
            # Ensure we have valid references
            shipment = shipments[i % len(shipments)]
            vehicle = vehicles[i % len(vehicles)]
            route = routes[i % len(routes)]
            
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
                shipment=shipment,
                vehicle=vehicle,
                route=route,
            )
            total_created += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {total_created} alerts."))
