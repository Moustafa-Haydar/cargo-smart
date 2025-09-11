import pandas as pd
import openrouteservice
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Enrich dataset with realistic route polylines and segments using OpenRouteService"

    def add_arguments(self, parser):
        parser.add_argument(
            "--input",
            type=str,
            default="delivery_truck_data.xlsx",
            help="Path to input Excel file",
        )
        parser.add_argument(
            "--output",
            type=str,
            default="delivery_truck_data_with_routes.xlsx",
            help="Path to save enriched Excel file",
        )
        parser.add_argument(
            "--apikey",
            type=str,
            required=True,
            help="OpenRouteService API key",
        )

    def handle(self, *args, **options):
        input_file = options["input"]
        output_file = options["output"]
        api_key = options["apikey"]

        self.stdout.write(self.style.SUCCESS(f"Loading {input_file}..."))
        df = pd.read_excel(input_file, sheet_name="VTS Data 280820")

        client = openrouteservice.Client(key=api_key)

        def parse_latlon(s):
            try:
                lat, lon = [float(x.strip()) for x in str(s).split(",")]
                return lat, lon
            except Exception:
                return None, None

        def get_route(origin, destination):
            try:
                coords = [(origin[1], origin[0]), (destination[1], destination[0])]
                route = client.directions(coords, profile="driving-car", format="geojson")
                polyline = route["features"][0]["geometry"]["coordinates"]
                polyline = [(lat, lon) for lon, lat in polyline]
                segments = [
                    f"{polyline[i]} -> {polyline[i+1]}"
                    for i in range(len(polyline) - 1)
                ]
                return polyline, segments
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Route error: {e}"))
                return None, None

        df["route_polyline"] = None
        df["route_segments"] = None

        for idx, row in df.iterrows():
            origin = parse_latlon(row["Org_lat_lon"])
            dest = parse_latlon(row["Dest_lat_lon"])
            if None not in origin and None not in dest:
                polyline, segments = get_route(origin, dest)
                df.at[idx, "route_polyline"] = str(polyline)
                df.at[idx, "route_segments"] = str(segments)

        df.to_excel(output_file, index=False)
        self.stdout.write(self.style.SUCCESS(f"Saved enriched dataset to {output_file}"))
