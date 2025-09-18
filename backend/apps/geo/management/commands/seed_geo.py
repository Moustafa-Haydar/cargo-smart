import random
from django.core.management.base import BaseCommand
from apps.geo.models import Location


class Command(BaseCommand):
    help = "Seed realistic Indian locations from actual logistics data. Use --fresh to delete existing first."

    def add_arguments(self, parser):
        parser.add_argument("--fresh", action="store_true")

    def handle(self, *args, **opts):
        if opts["fresh"]:
            Location.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared geo data"))

        random.seed(42)

        # Only realistic locations from actual logistics data
        realistic_locations = [
            ("TVSLSL-JAMALPURL-HUB", "Gurgaon, Haryana", 28.3540, 76.9390),
            ("TVSLSL HUB MATHIGIRI", "Hosur, Tamil Nadu", 12.7400, 77.8200),
            ("TVSLSL HUB (CHAKAN)", "Pune, Maharashtra", 18.7680, 73.8630),
            ("LUCAS TVS LTD-PONDY", "Pondy, Pondicherry", 11.8720, 79.6320),
            ("LUCAS TVS LTD-AMBATTUR", "Chennai, Tamil Nadu", 13.1020, 80.1940),
            ("ASHOK LEYLAND ENNORE", "Chennai, Tamil Nadu", 13.2150, 80.3200),
            ("ASHOK LEYLAND PLANT 2-HOSUR", "Hosur, Karnataka", 12.7660, 77.7860),
            ("Shive", "Pune, Maharashtra", 18.750621, 73.87719),
            ("Pondur", "Kanchipuram, Tamil Nadu", 12.930429, 79.931163),
            ("Ramte Ram Road", "Ghaziabad, Uttar Pradesh", 28.927021, 77.642158),
            ("I. E. Partapur", "Meerut, Uttar Pradesh", 28.927021, 77.642158),
            ("Mookandapalli", "Krishnagiri, Tamil Nadu", 12.746894, 77.806168),
            ("Athipattu", "Tiruvallur, Tamil Nadu", 13.092058, 80.156813),
            ("Jagadambigainagar", "Tiruvallur, Tamil Nadu", 13.087428, 80.184717),
            ("Pozhal", "Tiruvallur, Tamil Nadu", 13.165101, 80.204244),
            ("Guruvoyal", "Tiruvallur, Tamil Nadu", 13.202214, 80.131693),
            ("Onnalvadi", "Krishnagiri, Tamil Nadu", 12.683589, 77.859239),
            ("Vellaripatti", "Madurai, Tamil Nadu", 9.973636, 78.281783),
            ("Devalapura", "Mysore, Karnataka", 12.223062, 76.690357),
        ]

        total_created = 0
        for name, state, lat, lng in realistic_locations:
            obj, created = Location.objects.get_or_create(
                name=name,
                state=state,
                country="India",
                country_code="IN",
                defaults=dict(lat=lat, lng=lng, timezone="Asia/Kolkata"),
            )
            if created:
                total_created += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {total_created} Indian locations for geo."))
