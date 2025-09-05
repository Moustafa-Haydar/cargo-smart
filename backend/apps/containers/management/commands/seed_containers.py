import random, uuid
from datetime import timedelta
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone as tz
from apps.containers.models import Container, ContainerEvent
from apps.geo.models import Location, Facility
from apps.vehicles.models import Vehicle

class Command(BaseCommand):
    help = "Seed 10 Containers + 10 ContainerEvents. Requires geo (and optionally vehicles, facilities)."

    def add_arguments(self, parser):
        parser.add_argument("--fresh", action="store_true")

    def handle(self, *args, **opts):
        if opts["fresh"]:
            ContainerEvent.objects.all().delete()
            Container.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared containers data"))

        if Location.objects.count() == 0:
            raise CommandError("Need Locations. Run: seed_geo.")

        random.seed(42)
        iso_codes = ["45G1","22G1","42G1","L5G1","4510"]
        sizes = ["40' High Cube Dry","20' Dry","40' Dry","L5 Dry","45' Dry"]

        containers = []
        for i in range(1, 11):
            containers.append(Container.objects.create(
                number=f"MSKU{(496560+i):07d}",
                iso_code=random.choice(iso_codes),
                size_type=random.choice(sizes),
                status=random.choice(["IN_TRANSIT","GATE_IN","GATE_OUT","LOADED","ARRIVED"]),
            ))

        locs = list(Location.objects.all())
        facs = list(Facility.objects.all())
        vehicles = list(Vehicle.objects.all())

        # events: respect unique fingerprint (container,event_code,happened_at,location,source)
        for i, c in enumerate(containers):
            l = random.choice(locs)
            f = random.choice([None] + facs)
            v = random.choice([None] + vehicles) if vehicles else None
            happened = tz.now() - timedelta(hours=72 - i*6)
            ContainerEvent.objects.create(
                container=c,
                location=l,
                facility=f,
                vehicle=v,
                voyage=f"{340+i}E" if v else None,
                description=random.choice(["Gate in","Gate out","Load","Vessel departure","Vessel arrival"]),
                event_type=random.choice(["EQUIPMENT","TRANSPORT"]),
                event_code=random.choice(["GTIN","GTOT","LOAD","DEPA","ARRI"]),
                status=random.choice(["CGI","CEP","CLL","VDL","VAD"]),
                route_type=random.choice(["LAND","SEA"]),
                transport_type=random.choice([None,"VESSEL","TRUCK"]),
                happened_at=happened,
                is_actual=(i % 2 == 0),
                is_additional=False,
                source="SEED",
                ingested_at=tz.now(),
            )

        self.stdout.write(self.style.SUCCESS("Seeded containers (+events)."))
