import os
import joblib
import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand
from cargosmart import settings


def parse_latlon(s):
    try:
        lat, lon = [float(x.strip()) for x in str(s).split(",")]
        return lat, lon
    except Exception:
        return np.nan, np.nan


def haversine_km(lat1, lon1, lat2, lon2):
    if any(pd.isna([lat1, lon1, lat2, lon2])):
        return np.nan
    R = 6371
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2)**2
    return 2 * R * np.arcsin(np.sqrt(a))


class Command(BaseCommand):
    help = "Test trained delay model on a new Excel table"

    def add_arguments(self, parser):
        parser.add_argument(
            "--input",
            type=str,
            default="data/test.xlsx",
            help="Path to test Excel file"
        )

    def handle(self, *args, **options):
        # 1. Load model
        model_path = os.path.join(settings.BASE_DIR, "models", "delay_classifier.joblib")
        if not os.path.exists(model_path):
            self.stderr.write("No trained model found. Run train command first.")
            return
        pipe = joblib.load(model_path)

        # 2. Load test data
        test_file = options["input"]
        df = pd.read_excel(test_file, sheet_name="Sheet1")

        # 3. Feature engineering (same as training)
        for col in ["BookingID_Date", "Planned_ETA"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")

        df[["org_lat", "org_lon"]] = df["Org_lat_lon"].apply(lambda s: pd.Series(parse_latlon(s)))
        df[["dst_lat", "dst_lon"]] = df["Dest_lat_lon"].apply(lambda s: pd.Series(parse_latlon(s)))
        df["haversine_km"] = df.apply(lambda r: haversine_km(r.org_lat, r.org_lon, r.dst_lat, r.dst_lon), axis=1)

        df["planned_hour"] = df["Planned_ETA"].dt.hour
        df["planned_dow"] = df["Planned_ETA"].dt.dayofweek
        df["planned_month"] = df["Planned_ETA"].dt.month
        df["is_weekend"] = df["planned_dow"].isin([5, 6]).astype(int)
        df["lead_time_hours"] = (df["Planned_ETA"] - df["BookingID_Date"]).dt.total_seconds() / 3600

        df["rain_flag"] = (df["precipitation"].fillna(0).astype(float) > 0).astype(int)
        df["wind_flag"] = (df["wind_speed"].fillna(0).astype(float) > 10).astype(int)

        # 4. Predict
        X = df.drop(columns=[c for c in ["delay_hours", "delayed_flag"] if c in df.columns], errors="ignore")
        preds = pipe.predict(X)
        probs = pipe.predict_proba(X)[:, 1]

        # 5. Save results
        df["predicted_delay"] = preds
        df["delay_probability"] = probs
        out_file = test_file.replace(".xlsx", "_predictions.xlsx")
        df.to_excel(out_file, index=False)

        self.stdout.write(self.style.SUCCESS(f"Predictions saved to {out_file}"))
