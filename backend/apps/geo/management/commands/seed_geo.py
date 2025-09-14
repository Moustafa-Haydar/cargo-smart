import random
from django.core.management.base import BaseCommand
from apps.geo.models import Location


class Command(BaseCommand):
    help = "Seed ~25 Indian Locations for truck logistics. Use --fresh to delete existing first."

    def add_arguments(self, parser):
        parser.add_argument("--fresh", action="store_true")

    def handle(self, *args, **opts):
        if opts["fresh"]:
            Location.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared geo data"))

        random.seed(42)

        # Smaller base list (~12 cities)
        base_locations = [
            ("Chennai", "Tamil Nadu", 13.0827, 80.2707),
            ("Bengaluru", "Karnataka", 12.9716, 77.5946),
            ("Mumbai", "Maharashtra", 19.0760, 72.8777),
            ("Delhi", "Delhi", 28.7041, 77.1025),
            ("Hyderabad", "Telangana", 17.3850, 78.4867),
            ("Kolkata", "West Bengal", 22.5726, 88.3639),
            ("Lucknow", "Uttar Pradesh", 26.8467, 80.9462),
            ("Ahmedabad", "Gujarat", 23.0225, 72.5714),
            ("Jaipur", "Rajasthan", 26.9124, 75.7873),
            ("Nagpur", "Maharashtra", 21.1458, 79.0882),
            ("Coimbatore", "Tamil Nadu", 11.0168, 76.9558),
            ("Visakhapatnam", "Andhra Pradesh", 17.6868, 83.2185),
        ]

        suffixes = ["Depot", "Hub"]

        total_created = 0
        for city, state, lat, lng in base_locations:
            # Always insert base city
            obj, created = Location.objects.get_or_create(
                name=city,
                state=state,
                country="India",
                country_code="IN",
                defaults=dict(lat=lat, lng=lng, timezone="Asia/Kolkata"),
            )
            if created:
                total_created += 1

            # Add at most 1 variation
            name = f"{city} {random.choice(suffixes)}"
            obj, created = Location.objects.get_or_create(
                name=name,
                state=state,
                country="India",
                country_code="IN",
                defaults=dict(
                    lat=lat + random.uniform(-0.05, 0.05),
                    lng=lng + random.uniform(-0.05, 0.05),
                    timezone="Asia/Kolkata",
                ),
            )
            if created:
                total_created += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {total_created} Indian locations for geo."))
