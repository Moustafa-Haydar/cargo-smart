import random
import uuid
from django.core.management.base import BaseCommand
from apps.vehicles.models import Vehicle, VehicleIdentifier
from apps.geo.models import Location


class Command(BaseCommand):
    help = "Seed demo trucks (vehicles) for India. Use --fresh to delete existing first."

    def add_arguments(self, parser):
        parser.add_argument("--fresh", action="store_true")
        parser.add_argument("--count", type=int, default=30, help="Number of vehicles to create")

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

        truck_models = [
            "Tata 407",
            "Ashok Leyland Dost",
            "Eicher Pro 3015",
            "Mahindra Blazo X",
            "BharatBenz 1617R",
            "Tata Signa 4825.T",
            "Eicher Pro 2049",
            "Mahindra Furio 14",
        ]

        statuses = ["ACTIVE", "IN_TRANSIT", "MAINTENANCE"]

        total_created = 0
        for i in range(opts["count"]):
            plate_number = f"{random.choice(['TN','MH','KA','DL','GJ','UP'])}{random.randint(10,99)}" \
                           f"{random.choice(['A','B','C','D','E'])}{random.randint(1000,9999)}"

            vehicle = Vehicle.objects.create(
                id=uuid.uuid4(),
                plate_number=plate_number,
                model=random.choice(truck_models),
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
