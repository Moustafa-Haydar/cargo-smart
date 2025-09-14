import random
import uuid
from datetime import timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand
from apps.shipments.models import Shipment, ShipmentMilestone
from apps.geo.models import Location
from apps.routes.models import Route
from apps.vehicles.models import Vehicle


class Command(BaseCommand):
    help = "Seed demo shipments for India truck logistics. Use --fresh to delete existing first."

    def add_arguments(self, parser):
        parser.add_argument("--fresh", action="store_true")
        parser.add_argument("--count", type=int, default=20, help="Number of shipments to create")

    def handle(self, *args, **opts):
        if opts["fresh"]:
            ShipmentMilestone.objects.all().delete()
            Shipment.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared shipment data"))

        random.seed(42)
        locations = list(Location.objects.all())
        routes = list(Route.objects.all())
        vehicles = list(Vehicle.objects.all())

        if len(locations) < 2:
            self.stdout.write(self.style.ERROR("Not enough locations. Run seed_geo first."))
            return

        if not routes:
            self.stdout.write(self.style.ERROR("No routes found. Run seed_routes first."))
            return

        if not vehicles:
            self.stdout.write(self.style.ERROR("No vehicles found. Run seed_vehicles first."))
            return

        total_shipments = 0
        total_milestones = 0

        for i in range(opts["count"]):
            origin, destination = random.sample(locations, 2)
            route = random.choice(routes)
            vehicle = random.choice(vehicles)

            ref_no = f"SHP-{uuid.uuid4().hex[:8].upper()}"
            scheduled_time = timezone.now() + timedelta(days=random.randint(-5, 5))
            delivered_time = scheduled_time + timedelta(hours=random.randint(8, 72))

            shipment = Shipment.objects.create(
                id=uuid.uuid4(),
                ref_no=ref_no,
                status=random.choice(["PLANNED", "ENROUTE", "DELIVERED"]),
                carrier_name=random.choice(["VRL Logistics", "Delhivery", "GATI", "BlueDart", "TCI Express"]),
                origin=origin,
                destination=destination,
                current_location=random.choice([origin, destination, random.choice(locations)]),
                route=route,
                scheduled_at=scheduled_time,
                delivered_at=delivered_time if random.random() > 0.3 else None,
            )
            total_shipments += 1

            # Add milestones
            milestones = [
                ("LOADED", origin, scheduled_time, True),
                ("ENROUTE", random.choice(locations), scheduled_time + timedelta(hours=random.randint(2, 12)), False),
                ("DELIVERED", destination, delivered_time, bool(shipment.delivered_at)),
            ]

            for kind, loc, date, actual in milestones:
                ShipmentMilestone.objects.create(
                    id=uuid.uuid4(),
                    shipment=shipment,
                    kind=kind,
                    location=loc,
                    date=date,
                    actual=actual,
                    predictive_eta=date + timedelta(hours=random.randint(1, 6)) if not actual else None,
                )
                total_milestones += 1

        self.stdout.write(
            self.style.SUCCESS(f"Seeded {total_shipments} shipments with {total_milestones} milestones.")
        )
