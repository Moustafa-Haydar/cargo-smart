import random, uuid
from datetime import timedelta
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone as tz
from apps.vehicles.models import Vehicle, VehicleIdentifier, VehiclePosition, PortCall
from apps.geo.models import Location, Facility
from apps.routes.models import Route

class Command(BaseCommand):
    help = "Seed 10 Vehicles + 10 Identifiers + 10 Positions + 10 PortCalls. Requires geo & routes."

    def add_arguments(self, parser):
        parser.add_argument("--fresh", action="store_true")

    def handle(self, *args, **opts):
        if opts["fresh"]:
            PortCall.objects.all().delete()
            VehiclePosition.objects.all().delete()
            VehicleIdentifier.objects.all().delete()
            Vehicle.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared vehicles data"))

        if Location.objects.count() == 0 or Route.objects.count() == 0:
            raise CommandError("Need Locations and Routes. Run: seed_geo, seed_routes.")

        random.seed(42)
        locs = list(Location.objects.all())
        routes = list(Route.objects.all())

        vehicles = []
        for i in range(1, 11):
            v = Vehicle.objects.create(
                name=f"MAERSK DEMO {i:02d}",
                type="VESSEL",
                status=random.choice(["IDLE","IN_TRANSIT","AT_PORT"]),
                current_location=random.choice(locs),
                route=random.choice(routes),
                imo=9298000+i,
                mmsi=367770000+i,
                call_sign=f"CALL{i:03d}",
                flag=random.choice(["US","DE","NL","BE","SG","CN","AE","BR"]),
            )
            vehicles.append(v)

        # identifiers
        for v in vehicles:
            VehicleIdentifier.objects.create(vehicle=v, scheme="IMO", value=str(v.imo))

        # positions
        for i in range(10):
            l = random.choice(locs)
            VehiclePosition.objects.create(
                vehicle=random.choice(vehicles),
                recorded_at=tz.now() - timedelta(hours=48 - i*4),
                location=l,
                lat=l.lat + random.uniform(-0.2, 0.2),
                lng=l.lng + random.uniform(-0.2, 0.2),
                source="SEED",
            )

        # port calls
        facs = list(Facility.objects.all())
        for i in range(10):
            v = vehicles[i]
            l = random.choice(locs)
            f = random.choice([None] + facs)
            PortCall.objects.create(
                vehicle=v,
                port_location=l,
                facility=f,
                voyage=f"{300+i}E",
                event=random.choice(["ARRIVAL","DEPARTURE","BERTH"]),
                label=random.choice(["Vessel arrival","Vessel departure","Alongside"]),
                status=random.choice(["PLANNED","CONFIRMED","COMPLETED"]),
            )

        self.stdout.write(self.style.SUCCESS("Seeded vehicles (+identifiers, positions, port calls)."))
