import random
from datetime import timedelta
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone as tz
from apps.shipments.models import Shipment, ShipmentMilestone, ShipmentVehicle, ShipmentContainer
from apps.geo.models import Location
from apps.routes.models import Route
from apps.vehicles.models import Vehicle
from apps.containers.models import Container

class Command(BaseCommand):
    help = "Seed 10 Shipments + 10 Milestones + 10 ShipmentVehicles + 10 ShipmentContainers. Requires geo, routes, vehicles, containers."

    def add_arguments(self, parser):
        parser.add_argument("--fresh", action="store_true")

    def handle(self, *args, **opts):
        if opts["fresh"]:
            ShipmentContainer.objects.all().delete()
            ShipmentVehicle.objects.all().delete()
            ShipmentMilestone.objects.all().delete()
            Shipment.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared shipments data"))

        if Location.objects.count() < 2 or Route.objects.count() == 0:
            raise CommandError("Need Locations (>=2) and Routes. Run: seed_geo, seed_routes.")

        random.seed(42)
        locs = list(Location.objects.all())
        routes = list(Route.objects.all())
        vehicles = list(Vehicle.objects.all())
        containers = list(Container.objects.all())

        shipments = []
        for i in range(1, 11):
            a, b = random.sample(locs, 2)
            s = Shipment.objects.create(
                ref_no=f"SHP{i:04d}",
                shipment_type=random.choice(["CT","BBK","LCL"]),
                status=random.choice(["IN_TRANSIT","CREATED","DELIVERED"]),
                carrier_code=random.choice(["MAEU","MSCU","CMA"]),
                carrier_name=random.choice(["Maersk","MSC","CMA CGM"]),
                api_updated_at=tz.now() - timedelta(hours=2),
                origin=a,
                destination=b,
                current_location=random.choice([a,b] + locs),
                route=random.choice(routes),
                scheduled_at=tz.now() - timedelta(hours=96 - i*8),
                delivered_at=None if i < 8 else (tz.now() - timedelta(hours=24 - i)),
            )
            shipments.append(s)

        kinds = ["PREPOL","POL","POD","POSTPOD"]
        for i, s in enumerate(shipments):
            ShipmentMilestone.objects.create(
                shipment=s,
                kind=random.choice(kinds),
                location=random.choice([s.origin, s.destination] + locs),
                date=tz.now() - timedelta(hours=72 - i*5),
                actual=(i % 2 == 0),
                predictive_eta=None if (i % 2 == 0) else tz.now() + timedelta(hours=i*3 + 12),
            )

        # Link first 10 vehicles/containers if available, else reuse random
        for i, s in enumerate(shipments):
            v = vehicles[i] if i < len(vehicles) else random.choice(vehicles) if vehicles else None
            if v:
                ShipmentVehicle.objects.create(
                    shipment=s, vehicle=v, voyage=f"{330+i}E", role=random.choice(["MAIN","FEEDER"])
                )

        used_pairs = set()
        for i, s in enumerate(shipments):
            if not containers: break
            c = containers[i] if i < len(containers) else random.choice(containers)
            if (s.id, c.id) in used_pairs:
                continue
            ShipmentContainer.objects.create(
                shipment=s, container=c,
                is_active=True,
                loaded_at=tz.now() - timedelta(hours=48 - i),
                discharged_at=None if i < 8 else tz.now() - timedelta(hours=12 - i),
            )
            used_pairs.add((s.id, c.id))

        self.stdout.write(self.style.SUCCESS("Seeded shipments (+milestones, +links to vehicles/containers)."))
