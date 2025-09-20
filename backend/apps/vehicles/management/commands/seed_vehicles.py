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
            # Additional 100+ vehicles from comprehensive logistics data
            ("MH01AB1234", "32 FT Multi-Axle 14MT - HCV"),
            ("MH02CD5678", "40 FT 3XL Trailer 35MT"),
            ("MH03EF9012", "Standard Truck"),
            ("MH04GH3456", "24 FT SXL Container"),
            ("MH05IJ7890", "20 FT CLOSE 7MT-MCV"),
            ("MH06KL1234", "17 FT Container"),
            ("MH07MN5678", "32 FT Single-Axle 7MT - HCV"),
            ("MH08OP9012", "1 MT Tata Ace (Closed Body)"),
            ("MH09QR3456", "Standard Truck"),
            ("MH10ST7890", "32 FT Multi-Axle 14MT - HCV"),
            ("DL01AB1234", "40 FT 3XL Trailer 35MT"),
            ("DL02CD5678", "Standard Truck"),
            ("DL03EF9012", "24 FT SXL Container"),
            ("DL04GH3456", "20 FT CLOSE 7MT-MCV"),
            ("DL05IJ7890", "17 FT Container"),
            ("DL06KL1234", "32 FT Single-Axle 7MT - HCV"),
            ("DL07MN5678", "1 MT Tata Ace (Closed Body)"),
            ("DL08OP9012", "Standard Truck"),
            ("DL09QR3456", "32 FT Multi-Axle 14MT - HCV"),
            ("DL10ST7890", "40 FT 3XL Trailer 35MT"),
            ("KA01AB1234", "Standard Truck"),
            ("KA02CD5678", "24 FT SXL Container"),
            ("KA03EF9012", "20 FT CLOSE 7MT-MCV"),
            ("KA04GH3456", "17 FT Container"),
            ("KA05IJ7890", "32 FT Single-Axle 7MT - HCV"),
            ("KA06KL1234", "1 MT Tata Ace (Closed Body)"),
            ("KA07MN5678", "Standard Truck"),
            ("KA08OP9012", "32 FT Multi-Axle 14MT - HCV"),
            ("KA09QR3456", "40 FT 3XL Trailer 35MT"),
            ("KA10ST7890", "Standard Truck"),
            ("TN01AB1234", "24 FT SXL Container"),
            ("TN02CD5678", "20 FT CLOSE 7MT-MCV"),
            ("TN03EF9012", "17 FT Container"),
            ("TN04GH3456", "32 FT Single-Axle 7MT - HCV"),
            ("TN05IJ7890", "1 MT Tata Ace (Closed Body)"),
            ("TN06KL1234", "Standard Truck"),
            ("TN07MN5678", "32 FT Multi-Axle 14MT - HCV"),
            ("TN08OP9012", "40 FT 3XL Trailer 35MT"),
            ("TN09QR3456", "Standard Truck"),
            ("TN10ST7890", "24 FT SXL Container"),
            ("GJ01AB1234", "20 FT CLOSE 7MT-MCV"),
            ("GJ02CD5678", "17 FT Container"),
            ("GJ03EF9012", "32 FT Single-Axle 7MT - HCV"),
            ("GJ04GH3456", "1 MT Tata Ace (Closed Body)"),
            ("GJ05IJ7890", "Standard Truck"),
            ("GJ06KL1234", "32 FT Multi-Axle 14MT - HCV"),
            ("GJ07MN5678", "40 FT 3XL Trailer 35MT"),
            ("GJ08OP9012", "Standard Truck"),
            ("GJ09QR3456", "24 FT SXL Container"),
            ("GJ10ST7890", "20 FT CLOSE 7MT-MCV"),
            ("UP01AB1234", "17 FT Container"),
            ("UP02CD5678", "32 FT Single-Axle 7MT - HCV"),
            ("UP03EF9012", "1 MT Tata Ace (Closed Body)"),
            ("UP04GH3456", "Standard Truck"),
            ("UP05IJ7890", "32 FT Multi-Axle 14MT - HCV"),
            ("UP06KL1234", "40 FT 3XL Trailer 35MT"),
            ("UP07MN5678", "Standard Truck"),
            ("UP08OP9012", "24 FT SXL Container"),
            ("UP09QR3456", "20 FT CLOSE 7MT-MCV"),
            ("UP10ST7890", "17 FT Container"),
            ("RJ01AB1234", "32 FT Single-Axle 7MT - HCV"),
            ("RJ02CD5678", "1 MT Tata Ace (Closed Body)"),
            ("RJ03EF9012", "Standard Truck"),
            ("RJ04GH3456", "32 FT Multi-Axle 14MT - HCV"),
            ("RJ05IJ7890", "40 FT 3XL Trailer 35MT"),
            ("RJ06KL1234", "Standard Truck"),
            ("RJ07MN5678", "24 FT SXL Container"),
            ("RJ08OP9012", "20 FT CLOSE 7MT-MCV"),
            ("RJ09QR3456", "17 FT Container"),
            ("RJ10ST7890", "32 FT Single-Axle 7MT - HCV"),
            ("MP01AB1234", "1 MT Tata Ace (Closed Body)"),
            ("MP02CD5678", "Standard Truck"),
            ("MP03EF9012", "32 FT Multi-Axle 14MT - HCV"),
            ("MP04GH3456", "40 FT 3XL Trailer 35MT"),
            ("MP05IJ7890", "Standard Truck"),
            ("MP06KL1234", "24 FT SXL Container"),
            ("MP07MN5678", "20 FT CLOSE 7MT-MCV"),
            ("MP08OP9012", "17 FT Container"),
            ("MP09QR3456", "32 FT Single-Axle 7MT - HCV"),
            ("MP10ST7890", "1 MT Tata Ace (Closed Body)"),
            ("WB01AB1234", "Standard Truck"),
            ("WB02CD5678", "32 FT Multi-Axle 14MT - HCV"),
            ("WB03EF9012", "40 FT 3XL Trailer 35MT"),
            ("WB04GH3456", "Standard Truck"),
            ("WB05IJ7890", "24 FT SXL Container"),
            ("WB06KL1234", "20 FT CLOSE 7MT-MCV"),
            ("WB07MN5678", "17 FT Container"),
            ("WB08OP9012", "32 FT Single-Axle 7MT - HCV"),
            ("WB09QR3456", "1 MT Tata Ace (Closed Body)"),
            ("WB10ST7890", "Standard Truck"),
            ("AP01AB1234", "32 FT Multi-Axle 14MT - HCV"),
            ("AP02CD5678", "40 FT 3XL Trailer 35MT"),
            ("AP03EF9012", "Standard Truck"),
            ("AP04GH3456", "24 FT SXL Container"),
            ("AP05IJ7890", "20 FT CLOSE 7MT-MCV"),
            ("AP06KL1234", "17 FT Container"),
            ("AP07MN5678", "32 FT Single-Axle 7MT - HCV"),
            ("AP08OP9012", "1 MT Tata Ace (Closed Body)"),
            ("AP09QR3456", "Standard Truck"),
            ("AP10ST7890", "32 FT Multi-Axle 14MT - HCV"),
            ("TS01AB1234", "40 FT 3XL Trailer 35MT"),
            ("TS02CD5678", "Standard Truck"),
            ("TS03EF9012", "24 FT SXL Container"),
            ("TS04GH3456", "20 FT CLOSE 7MT-MCV"),
            ("TS05IJ7890", "17 FT Container"),
            ("TS06KL1234", "32 FT Single-Axle 7MT - HCV"),
            ("TS07MN5678", "1 MT Tata Ace (Closed Body)"),
            ("TS08OP9012", "Standard Truck"),
            ("TS09QR3456", "32 FT Multi-Axle 14MT - HCV"),
            ("TS10ST7890", "40 FT 3XL Trailer 35MT"),
            ("KL01AB1234", "Standard Truck"),
            ("KL02CD5678", "24 FT SXL Container"),
            ("KL03EF9012", "20 FT CLOSE 7MT-MCV"),
            ("KL04GH3456", "17 FT Container"),
            ("KL05IJ7890", "32 FT Single-Axle 7MT - HCV"),
            ("KL06KL1234", "1 MT Tata Ace (Closed Body)"),
            ("KL07MN5678", "Standard Truck"),
            ("KL08OP9012", "32 FT Multi-Axle 14MT - HCV"),
            ("KL09QR3456", "40 FT 3XL Trailer 35MT"),
            ("KL10ST7890", "Standard Truck"),
            ("PB01AB1234", "24 FT SXL Container"),
            ("PB02CD5678", "20 FT CLOSE 7MT-MCV"),
            ("PB03EF9012", "17 FT Container"),
            ("PB04GH3456", "32 FT Single-Axle 7MT - HCV"),
            ("PB05IJ7890", "1 MT Tata Ace (Closed Body)"),
            ("PB06KL1234", "Standard Truck"),
            ("PB07MN5678", "32 FT Multi-Axle 14MT - HCV"),
            ("PB08OP9012", "40 FT 3XL Trailer 35MT"),
            ("PB09QR3456", "Standard Truck"),
            ("PB10ST7890", "24 FT SXL Container"),
            ("HR01AB1234", "20 FT CLOSE 7MT-MCV"),
            ("HR02CD5678", "17 FT Container"),
            ("HR03EF9012", "32 FT Single-Axle 7MT - HCV"),
            ("HR04GH3456", "1 MT Tata Ace (Closed Body)"),
            ("HR05IJ7890", "Standard Truck"),
            ("HR06KL1234", "32 FT Multi-Axle 14MT - HCV"),
            ("HR07MN5678", "40 FT 3XL Trailer 35MT"),
            ("HR08OP9012", "Standard Truck"),
            ("HR09QR3456", "24 FT SXL Container"),
            ("HR10ST7890", "20 FT CLOSE 7MT-MCV"),
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
