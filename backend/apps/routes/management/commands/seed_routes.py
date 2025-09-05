import json, random, uuid
from django.core.management.base import BaseCommand, CommandError
from apps.routes.models import Route, RouteSegment
from apps.geo.models import Location

class Command(BaseCommand):
    help = "Seed 10 Routes and 10 RouteSegments. Requires geo."

    def add_arguments(self, parser):
        parser.add_argument("--fresh", action="store_true")

    def _line(self, a, b):
        return json.dumps({"type":"LineString","coordinates":[[a.lng,a.lat],[b.lng,b.lat]]})

    def handle(self, *args, **opts):
        if opts["fresh"]:
            RouteSegment.objects.all().delete()
            Route.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared routes data"))

        if Location.objects.count() < 2:
            raise CommandError("Need at least 2 Locations. Run: python manage.py seed_geo")

        random.seed(42)
        routes = []
        locs = list(Location.objects.all())

        for i in range(1, 11):
            a, b = random.sample(locs, 2)
            r = Route.objects.create(name=f"Route {i:02d}", geometry=self._line(a, b))
            routes.append(r)

        # segments with unique (route, seq)
        seq_map = {r.id: 0 for r in routes}
        for _ in range(10):
            r = random.choice(routes[:4])
            seq_map[r.id] += 1
            a, b = random.sample(locs, 2)
            RouteSegment.objects.create(
                route=r, seq=seq_map[r.id],
                route_type=random.choice(["SEA","LAND"]),
                geometry=self._line(a, b),
                mode=random.choice(["VESSEL","TRUCK"])
            )

        self.stdout.write(self.style.SUCCESS("Seeded routes (10 Routes, 10 RouteSegments)."))
