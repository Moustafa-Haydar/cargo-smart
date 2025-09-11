import os
import time
import pandas as pd
import openrouteservice
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Enrich dataset with realistic route polylines and segments using OpenRouteService"

    def add_arguments(self, parser):
        parser.add_argument(
            "--input",
            type=str,
            default="data/delivery_truck_data.xlsx",
            help="Path to input Excel file (default: data/delivery_truck_data.xlsx)",
        )
        parser.add_argument(
            "--output",
            type=str,
            default="data/delivery_truck_data_with_routes.xlsx",
            help="Path to save enriched Excel file (default: data/delivery_truck_data_with_routes.xlsx)",
        )
        parser.add_argument(
            "--apikey",
            type=str,
            help="OpenRouteService API key (optional, falls back to ORS_API_KEY env var)",
        )

    def handle(self, *args, **options):
        input_file = options["input"]
        output_file = options["output"]
        api_key = options["apikey"] or os.getenv("ORS_API_KEY")

        if not api_key:
            self.stderr.write(self.style.ERROR(
                "No API key provided. Use --apikey or set ORS_API_KEY in .env"
            ))
            return

        self.stdout.write(self.style.SUCCESS(f"Loading {input_file}..."))
        df = pd.read_excel(input_file, sheet_name="Sheet1")

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
                route = client.directions(
                    coords,
                    profile="driving-car",
                    format="geojson",
                    radiuses=[1000, 1000],
                    geometry_simplify=True
                )
                polyline = route["features"][0]["geometry"]["coordinates"]
                polyline = [(lat, lon) for lon, lat in polyline]  # back to (lat,lon)

                # ✅ Downsample polyline (max 50 points)
                if len(polyline) > 50:
                    step = len(polyline) // 50
                    polyline = polyline[::step]
                    if polyline[-1] != destination:
                        polyline.append(destination)

                # ✅ Ensure start and end match input
                polyline[0] = origin
                polyline[-1] = destination

                # ✅ Keep segments short (origin → middle → destination)
                segments = [
                    f"{polyline[0]} -> {polyline[len(polyline)//2]} -> {polyline[-1]}"
                ]

                return polyline, segments
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Route error: {e}"))
                return None, None



        # Add new columns if not already there
        if "route_polyline" not in df.columns:
            df["route_polyline"] = None
        if "route_segments" not in df.columns:
            df["route_segments"] = None

        # Cache to avoid duplicate requests
        cache = {}

        rows = len(df)
        max_per_minute = 35
        calls_done = 0


        for start in range(0, rows, max_per_minute):
            end = min(start + max_per_minute, rows)
            batch = df.iloc[start:end]

            self.stdout.write(self.style.SUCCESS(f"Processing rows {start} to {end-1}..."))

            for idx, row in batch.iterrows():

                # limit api calls for testing
                # if calls_done >= 5:
                #     break

                origin = parse_latlon(row["Org_lat_lon"])
                dest = parse_latlon(row["Dest_lat_lon"])

                if None not in origin and None not in dest:
                    key = (row["Org_lat_lon"], row["Dest_lat_lon"])

                    if key not in cache:
                        polyline, segments = get_route(origin, dest)
                        cache[key] = (polyline, segments)
                        calls_done += 1
                    else:
                        polyline, segments = cache[key]

                    df.at[idx, "route_polyline"] = str(polyline)
                    df.at[idx, "route_segments"] = str(segments)

            # Save progress every batch
            df.to_excel(output_file, index=False)
            self.stdout.write(self.style.SUCCESS(f"Saved progress to {output_file}"))

            if end < rows:
                self.stdout.write(self.style.WARNING("Sleeping 70 seconds to respect API limits..."))
                time.sleep(70)

        self.stdout.write(self.style.SUCCESS(f"Finished! Final file saved to {output_file}"))
