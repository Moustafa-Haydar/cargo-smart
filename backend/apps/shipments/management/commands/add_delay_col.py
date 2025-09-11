import os
import pandas as pd
from django.core.management.base import BaseCommand
from cargosmart import settings


class Command(BaseCommand):
    help = "Add delay_hours column to the truck delivery dataset"

    def handle(self, *args, **options):
        # Load your file
        file_path = os.path.join(settings.BASE_DIR, "data", "delivery_truck_data.xlsx")
        df = pd.read_excel(file_path, sheet_name="Sheet1")

        # Convert to datetime
        df["Planned_ETA"] = pd.to_datetime(df["Planned_ETA"])
        df["actual_eta"] = pd.to_datetime(df["actual_eta"])

        # Compute delay for all rows (hours)
        df["delay_hours"] = (df["actual_eta"] - df["Planned_ETA"]).dt.total_seconds() / 3600

        # Save to a new Excel file
        output_path = os.path.join(settings.BASE_DIR, "data", "delivery_truck_data_with_delay.xlsx")
        df.to_excel(output_path, index=False)

        self.stdout.write(self.style.SUCCESS(f"Delay column added. New file saved at {output_path}"))
