import pandas as pd
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Clean dataset by removing rows where destination == origin"

    def handle(self, *args, **options):
        # Load dataset
        df = pd.read_excel("data/delivery_truck_data.xlsx", sheet_name="Sheet1")

        # Remove rows where destination == origin
        df_cleaned = df[df["Org_lat_lon"] != df["Dest_lat_lon"]].reset_index(drop=True)

        # Save cleaned dataset
        output_file = "data/delivery_truck_data_cleaned.xlsx"
        df_cleaned.to_excel(output_file, index=False)

        self.stdout.write(self.style.SUCCESS(f"Cleaned dataset saved to {output_file}"))
