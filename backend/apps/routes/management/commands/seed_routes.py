import random, uuid, json, os
from django.core.management.base import BaseCommand
from apps.geo.models import Location
from apps.routes.models import Route, RouteSegment
import openrouteservice


class Command(BaseCommand):
    help = "Seed truck routes with minimal ORS API calls."

    def add_arguments(self, parser):
        parser.add_argument("--fresh", action="store_true")
        parser.add_argument("--count", type=int, default=20)

    def handle(self, *args, **opts):
        if opts["fresh"]:
            RouteSegment.objects.all().delete()
            Route.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared routes."))

        api_key = os.getenv("ORS_API_KEY")
        client = openrouteservice.Client(key=api_key)

        locations = list(Location.objects.all())
        if len(locations) < 2:
            self.stdout.write(self.style.ERROR("Seed geo first."))
            return

        used_pairs = set()
        total_routes, total_segments = 0, 0

        for i in range(opts["count"]):
            origin, destination = random.sample(locations, 2)
            pair = tuple(sorted([origin.id, destination.id]))

            if pair in used_pairs:  # already seeded this corridor
                continue
            used_pairs.add(pair)

            # Check if already in DB
            existing = Route.objects.filter(name=f"{origin.name} → {destination.name}").first()
            if existing:
                continue

            # One ORS API call
            coords = [(origin.lng, origin.lat), (destination.lng, destination.lat)]
            result = client.directions(coordinates=coords, profile="driving-hgv", format="geojson")

            geometry = result["features"][0]["geometry"]["coordinates"]

            route = Route.objects.create(
                id=uuid.uuid4(),
                name=f"{origin.name} → {destination.name}",
                geometry=json.dumps({"type": "LineString", "coordinates": geometry}),
            )
            total_routes += 1

            # Split into 5 chunks manually
            step = max(1, len(geometry) // 5)
            for seq, idx in enumerate(range(0, len(geometry), step), start=1):
                coords_chunk = geometry[idx: idx + step + 1]
                if len(coords_chunk) < 2:
                    continue

                RouteSegment.objects.create(
                    id=uuid.uuid4(),
                    route=route,
                    seq=seq,
                    geometry=json.dumps({"type": "LineString", "coordinates": coords_chunk}),
                )
                total_segments += 1

        self.stdout.write(self.style.SUCCESS(f"Created {total_routes} routes with {total_segments} segments (fewer ORS calls)."))
