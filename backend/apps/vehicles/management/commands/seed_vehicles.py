import random
import uuid
from django.core.management.base import BaseCommand
from apps.vehicles.models import Vehicle, VehicleIdentifier
from apps.geo.models import Location


class Command(BaseCommand):
    help = "Seed realistic trucks (vehicles) from actual logistics data. Use --fresh to delete existing first."

    def add_arguments(self, parser):
        parser.add_argument("--fresh", action="store_true")

    def handle(self, *args, **opts):
        if opts["fresh"]:
            VehicleIdentifier.objects.all().delete()
            Vehicle.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared vehicle data"))

        random.seed(42)
        locations = list(Location.objects.all())
        if not locations:
            self.stdout.write(self.style.ERROR("No locations found. Run seed_geo first."))
            return

        # Only realistic vehicles from actual records
        realistic_vehicles = [
            ("HR55AD6502", "32 FT Multi-Axle 14MT - HCV"),
            ("RJ10GB2085", "32 FT Multi-Axle 14MT - HCV"),
            ("tn02ap2662", "Standard Truck"),
            ("TN25M8075", "Standard Truck"),
            ("UP17T8250", "40 FT 3XL Trailer 35MT"),
            ("MH11CH3086", "Standard Truck"),
            ("TN23AA5466", "Standard Truck"),
            ("TN18AB5514", "Standard Truck"),
            ("MH12PQ8289", "32 FT Multi-Axle 14MT - HCV"),
            ("TN30BC6476", "32 FT Multi-Axle 14MT - HCV"),
            ("TN13K3804", "20 FT CLOSE 7MT-MCV"),
            ("TN14T4848", "32 FT Multi-Axle 14MT - HCV"),
            ("KA51C6972", "1 MT Tata Ace (Closed Body)"),
            ("UP17AT4210", "40 FT 3XL Trailer 35MT"),
            ("MH12MV8991", "20 FT CLOSE 7MT-MCV"),
            ("TN28AL5055", "Standard Truck"),
            ("NL01AE2521", "32 FT Single-Axle 7MT - HCV"),
            ("KA51AC7656", "17 FT Container"),
            ("TN60F8519", "Standard Truck"),
            ("TN60D8749", "24 FT SXL Container"),
            # Additional vehicles from comprehensive logistics data
            ("HR47C5324", "32 FT Single-Axle 7MT - HCV"),
            ("KA21A6904", "40 FT 3XL Trailer 35MT"),
            ("TN54K5040", "32 FT Multi-Axle 14MT - HCV"),
            ("TN52Y0785", "Standard Truck"),
            ("TN40X6070", "24 FT SXL Container"),
            ("KA51A7682", "Standard Truck"),
            ("UP17AT0059", "40 FT 3XL Trailer 35MT"),
            ("KA14A0338", "Standard Truck"),
            ("GJ01DY4657", "32 FT Single-Axle 7MT - HCV"),
            ("TN283256", "Standard Truck"),
            ("TN88C3198", "32 FT Multi-Axle 14MT - HCV"),
            ("TN18AB5514", "Standard Truck"),
            ("TN23AA5466", "Standard Truck"),
            ("TN28AL5055", "Standard Truck"),
            ("MH12NX2210", "32 FT Single-Axle 7MT - HCV"),
        ]

        statuses = ["ACTIVE", "IN_TRANSIT", "MAINTENANCE"]

        total_created = 0
        # Only create the realistic vehicles, no additional random ones
        for plate_number, model in realistic_vehicles:

            vehicle = Vehicle.objects.create(
                id=uuid.uuid4(),
                plate_number=plate_number,
                model=model,
                status=random.choice(statuses),
                current_location=random.choice(locations),
                route=None,
            )

            # Add identifiers (e.g., VIN, RFID)
            VehicleIdentifier.objects.create(
                id=uuid.uuid4(),
                vehicle=vehicle,
                scheme="VIN",
                value=f"VIN{random.randint(100000,999999)}"
            )
            VehicleIdentifier.objects.create(
                id=uuid.uuid4(),
                vehicle=vehicle,
                scheme="RFID",
                value=f"RFID{random.randint(100000,999999)}"
            )

            total_created += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {total_created} vehicles with identifiers."))
