"""
Standalone command to generate visualizations for an existing trained model
"""
import os
import joblib
import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand
from cargosmart import settings
from .ml_visualizations import MLVisualizer

class Command(BaseCommand):
    help = "Generate visualizations for an existing trained model"

    def add_arguments(self, parser):
        parser.add_argument(
            '--model-path',
            type=str,
            default=os.path.join(settings.BASE_DIR, "models", "delay_classifier.joblib"),
            help='Path to the trained model file'
        )
        parser.add_argument(
            '--data-path',
            type=str,
            default=os.path.join(settings.BASE_DIR, "data", "delivery_truck_data.xlsx"),
            help='Path to the data file'
        )

    def handle(self, *args, **options):
        model_path = options['model_path']
        data_path = options['data_path']
        
        # Check if model exists
        if not os.path.exists(model_path):
            self.stderr.write(f"Model file not found: {model_path}")
            return
            
        if not os.path.exists(data_path):
            self.stderr.write(f"Data file not found: {data_path}")
            return
        
        # Initialize visualizer
        models_dir = os.path.join(settings.BASE_DIR, "models")
        visualizer = MLVisualizer(os.path.join(models_dir, "plots"))
        
        self.stdout.write("🔄 Loading model and data...")
        
        # Load model
        model = joblib.load(model_path)
        
        # Load and prepare data (same preprocessing as training)
        df = pd.read_excel(data_path, nrows=800)
        
        # Apply same preprocessing as in training
        for col in ["BookingID_Date", "Planned_ETA"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")
        
        if "delay_hours" not in df.columns:
            self.stderr.write("Missing 'delay_hours' column in data")
            return
            
        df["delayed_flag"] = (df["delay_hours"] > 0).astype(int)
        
        # Create features (simplified version of training preprocessing)
        def parse_latlon(s):
            try:
                lat, lon = [float(x.strip()) for x in str(s).split(",")]
                return lat, lon
            except Exception:
                return np.nan, np.nan

        def haversine_km(lat1, lon1, lat2, lon2):
            if any(pd.isna([lat1, lon1, lat2, lon2])):
                return np.nan
            from math import radians, sin, cos, asin, sqrt
            R = 6371
            dlat = radians(lat2 - lat1)
            dlon = radians(lon2 - lon1)
            a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
            return 2 * R * asin(sqrt(a))
        
        # Apply feature engineering
        df[["org_lat","org_lon"]] = df["Org_lat_lon"].apply(lambda s: pd.Series(parse_latlon(s)))
        df[["dst_lat","dst_lon"]] = df["Dest_lat_lon"].apply(lambda s: pd.Series(parse_latlon(s)))
        df["haversine_km"] = df.apply(lambda r: haversine_km(r.org_lat, r.org_lon, r.dst_lat, r.dst_lon), axis=1)
        
        df["planned_hour"] = df["Planned_ETA"].dt.hour
        df["planned_dow"] = df["Planned_ETA"].dt.dayofweek
        df["planned_month"] = df["Planned_ETA"].dt.month
        df["is_weekend"] = df["planned_dow"].isin([5,6]).astype(int)
        df["lead_time_hours"] = (df["Planned_ETA"] - df["BookingID_Date"]).dt.total_seconds() / 3600
        
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
        
        # Select features
        num_feats = [c for c in [
            "temp_c","wind_speed","humidity","precipitation",
            "haversine_km","planned_hour","planned_dow","planned_month",
            "is_weekend","lead_time_hours"
        ] if c in df.columns]
        cat_feats = [c for c in ["GpsProvider","Market/Regular","condition"] if c in df.columns]
        
        # Remove leakage columns
        for leak in ["actual_eta", "delay", "delay_hours"]:
            if leak in df.columns:
                df = df.drop(columns=[leak])
        
        X = df[num_feats + cat_feats].copy()
        y = df["delayed_flag"].copy()
        
        # Make predictions
        self.stdout.write("🔮 Making predictions...")
        probs = model.predict_proba(X)[:, 1]
        preds = (probs >= 0.5).astype(int)
        
        # Generate all visualizations
        self.stdout.write("📊 Creating data distribution visualizations...")
        visualizer.plot_data_distribution(df)
        
        self.stdout.write("🔍 Creating feature analysis visualizations...")
        visualizer.plot_feature_analysis(X, y, num_feats + cat_feats)
        
        self.stdout.write("📈 Creating model performance visualizations...")
        visualizer.plot_model_performance(y, probs, preds)
        
        self.stdout.write("📋 Creating summary report...")
        visualizer.create_summary_report(model, X, y, preds, probs)
        
        self.stdout.write(self.style.SUCCESS("✅ All visualizations generated successfully!"))
        self.stdout.write(self.style.SUCCESS(f"📁 Plots saved to: {visualizer.output_dir}/"))
