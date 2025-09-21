import os
import time
import requests
import pandas as pd

from django.core.management.base import BaseCommand
from cargosmart import settings


API_KEY = "4e7a807935f6925a289a5dbdd951c3dc"


def get_weather(lat, lon, dt):
    url = "https://api.openweathermap.org/data/3.0/onecall/timemachine"
    params = {
        "lat": lat,
        "lon": lon,
        "dt": dt,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        # Extract some useful features from the hourly data closest to dt
        weather = data.get("data", data.get("hourly", []))[0]
        return {
            "temp_c": weather.get("temp"),
            "wind_speed": weather.get("wind_speed"),
            "humidity": weather.get("humidity"),
            "precipitation": weather.get("rain", {}).get("1h", 0),
            "condition": weather["weather"][0]["main"] if "weather" in weather else None
        }
    else:
        print("Error:", response.json())
        return None


class Command(BaseCommand):
    help = "Enrich shipment dataset with historical weather data"

    def handle(self, *args, **options):
        # Load truck delivery dataset
        file_path = os.path.join(settings.BASE_DIR, "data", "delivery_truck_data.xlsx")
        df = pd.read_excel(file_path, sheet_name="Sheet1")

        for i, row in df.iloc[800:1500].iterrows():
            try:
                dt = int(row["trip_start_date"].timestamp())  # UTC timestamp
                lat, lon = map(float, row["Org_lat_lon"].split(","))
                self.stdout.write(f"Fetching weather for {dt} {lat} {lon}")

                weather = get_weather(lat, lon, dt)
                if weather:
                    for k, v in weather.items():
                        df.loc[i, k] = v  # add/update weather columns
                time.sleep(1)  # avoid hammering the API
            except Exception as e:
                self.stderr.write(f"Error processing row {i}: {e}")

        # Overwrite the same Excel file with enriched data
        df.to_excel(file_path, sheet_name="Sheet1", index=False)

        self.stdout.write(self.style.SUCCESS(f"Updated Excel file with {len(df)} rows enriched"))
