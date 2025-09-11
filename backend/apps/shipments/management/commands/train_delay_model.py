import os
import joblib
import numpy as np
import pandas as pd
from math import radians, sin, cos, asin, sqrt

from django.core.management.base import BaseCommand
from cargosmart import settings

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score, f1_score, classification_report


def parse_latlon(s):
    try:
        lat, lon = [float(x.strip()) for x in str(s).split(",")]
        return lat, lon
    except Exception:
        return np.nan, np.nan

def haversine_km(lat1, lon1, lat2, lon2):
    """Great-circle distance in KM; returns NaN if any input missing."""
    if any(pd.isna([lat1, lon1, lat2, lon2])):
        return np.nan
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    return 2 * R * asin(sqrt(a))

class Command(BaseCommand):
    help = "Train a simple delay classifier and save the model to models/delay_classifier.joblib"

    def handle(self, *args, **options):
        # 1) Load data
        data_path = os.path.join(settings.BASE_DIR, "data", "delivery_truck_data.xlsx")
        # df = pd.read_excel(data_path)
        # only the first 800 record are ready
        df = pd.read_excel(data_path, nrows=800)


        # 2) Parse times (best effort)
        for col in ["BookingID_Date", "Planned_ETA"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")

        # 3) Create binary label: delayed if delay_hours > 0
        if "delay_hours" not in df.columns:
            self.stderr.write("Missing 'delay_hours' column. Run add_delay_col first.")
            return
        df["delayed_flag"] = (df["delay_hours"] > 0).astype(int)

        # 4) Drop rows missing core fields
        required_cols = ["BookingID_Date", "Planned_ETA", "Org_lat_lon", "Dest_lat_lon"]
        keep_mask = np.ones(len(df), dtype=bool)
        for c in required_cols:
            if c in df.columns:
                keep_mask &= df[c].notna()
        df = df.loc[keep_mask].copy()
        if len(df) < 100:
            self.stderr.write(f"Warning: after cleaning, only {len(df)} rows remain. Training might be weak.")

        # 5) Geo features
        df[["org_lat","org_lon"]] = df["Org_lat_lon"].apply(lambda s: pd.Series(parse_latlon(s)))
        df[["dst_lat","dst_lon"]] = df["Dest_lat_lon"].apply(lambda s: pd.Series(parse_latlon(s)))
        df["haversine_km"] = df.apply(lambda r: haversine_km(r.org_lat, r.org_lon, r.dst_lat, r.dst_lon), axis=1)

        # 6) Temporal features
        df["planned_hour"]  = df["Planned_ETA"].dt.hour
        df["planned_dow"]   = df["Planned_ETA"].dt.dayofweek
        df["planned_month"] = df["Planned_ETA"].dt.month
        df["is_weekend"]    = df["planned_dow"].isin([5,6]).astype(int)
        df["lead_time_hours"] = (df["Planned_ETA"] - df["BookingID_Date"]).dt.total_seconds() / 3600

        # 7) Weather flags (if available)
        if "precipitation" in df.columns:
            df["rain_flag"] = (df["precipitation"].fillna(0) > 0).astype(int)
        else:
            df["precipitation"] = 0.0
            df["rain_flag"] = 0

        if "wind_speed" in df.columns:
            df["wind_flag"] = (df["wind_speed"].fillna(0) > 10).astype(int)
        else:
            df["wind_speed"] = 0.0
            df["wind_flag"] = 0

        # 8) Select features (keep it small & robust)
        num_feats = [
            c for c in [
                "temp_c","wind_speed","humidity","precipitation",
                "haversine_km","planned_hour","planned_dow","planned_month",
                "is_weekend","lead_time_hours"
            ] if c in df.columns
        ]
        cat_feats = [c for c in ["GpsProvider","Market/Regular","condition"] if c in df.columns]

        # Remove leakage columns from features
        for leak in ["actual_eta", "delay", "delay_hours"]:
            if leak in df.columns:
                df = df.drop(columns=[leak])

        X = df[num_feats + cat_feats].copy()
        y = df["delayed_flag"].copy()

        # 9) Train/test split (simple random split; later you can switch to time-based)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # 10) Preprocess + model
        numeric_transformer = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore"))
        ])

        preprocess = ColumnTransformer(
            transformers=[
                ("num", numeric_transformer, num_feats),
                ("cat", categorical_transformer, cat_feats),
            ]
        )

        model = LogisticRegression(max_iter=300, class_weight="balanced")

        pipe = Pipeline(steps=[("prep", preprocess), ("clf", model)])
        pipe.fit(X_train, y_train)

        # 11) Evaluate
        probs = pipe.predict_proba(X_test)[:, 1]
        preds = (probs >= 0.5).astype(int)

        roc = roc_auc_score(y_test, probs)
        pr  = average_precision_score(y_test, probs)
        f1  = f1_score(y_test, preds)

        self.stdout.write(f"ROC-AUC: {roc:.3f}")
        self.stdout.write(f"PR-AUC : {pr:.3f}")
        self.stdout.write(f"F1     : {f1:.3f}")
        self.stdout.write("\nClassification report:\n" + classification_report(y_test, preds))

        # 12) Save model
        models_dir = os.path.join(settings.BASE_DIR, "models")
        os.makedirs(models_dir, exist_ok=True)
        model_path = os.path.join(models_dir, "delay_classifier.joblib")
        joblib.dump(pipe, model_path)

        self.stdout.write(self.style.SUCCESS(f"Model saved to {model_path}"))