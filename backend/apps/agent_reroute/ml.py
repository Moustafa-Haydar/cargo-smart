import joblib, numpy as np
import pandas as pd
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

_model = None
_model_loaded = False
_model_error = None

def get_model():
    global _model, _model_loaded, _model_error
    
    if _model_loaded:
        if _model_error:
            raise _model_error
        return _model
    
    try:
        _model = joblib.load(settings.ROUTE_AI["MODEL_PATH"])
        _model_loaded = True
        logger.info("ML model loaded successfully")
        return _model
    except Exception as e:
        _model_error = e
        _model_loaded = True
        logger.error(f"Failed to load ML model: {e}")
        raise e

def build_features_from_shipment(shipment, current_option):
    """
    Map your shipment fields → model features.
    Adapt to your REAL pipeline (order/encodings must match training).
    """
    # Calculate haversine distance from origin to destination if available
    haversine_km = 0.0
    if hasattr(shipment, 'origin') and hasattr(shipment, 'destination'):
        if shipment.origin and shipment.destination:
            # Simple distance calculation (you might want to use a proper geodetic calculation)
            lat_diff = abs(shipment.origin.lat - shipment.destination.lat)
            lng_diff = abs(shipment.origin.lng - shipment.destination.lng)
            haversine_km = ((lat_diff ** 2 + lng_diff ** 2) ** 0.5) * 111  # Rough km conversion
    
    # Get datetime features from scheduled_at
    planned_hour = 9  # Default
    planned_dow = 1   # Default Monday
    planned_month = 1 # Default January
    is_weekend = 0    # Default weekday
    lead_time_hours = 24  # Default 24 hours
    
    if hasattr(shipment, 'scheduled_at') and shipment.scheduled_at:
        planned_hour = shipment.scheduled_at.hour
        planned_dow = shipment.scheduled_at.weekday() + 1  # Monday=1, Sunday=7
        planned_month = shipment.scheduled_at.month
        is_weekend = 1 if planned_dow in [6, 7] else 0  # Saturday=6, Sunday=7
        
        # Calculate lead time (hours from now to scheduled departure)
        from django.utils import timezone
        now = timezone.now()
        lead_time_hours = max(0, (shipment.scheduled_at - now).total_seconds() / 3600)
    
    # Build features to match training data exactly
    # Numeric features (10 features)
    numeric_features = [
        float(getattr(shipment, "temp_c", 25.0)),        # temp_c
        float(getattr(shipment, "wind_speed", 10.0)),    # wind_speed  
        float(getattr(shipment, "humidity", 60.0)),      # humidity
        float(getattr(shipment, "precipitation", 0.0)),  # precipitation
        haversine_km,                                    # haversine_km
        planned_hour,                                    # planned_hour
        planned_dow,                                     # planned_dow
        planned_month,                                   # planned_month
        is_weekend,                                      # is_weekend
        lead_time_hours,                                 # lead_time_hours
    ]
    
    # Categorical features (3 features) - encoded as numbers for simplicity
    # In a real system, you'd use proper categorical encoding
    gps_provider = 0  # Default encoding for missing GpsProvider
    market_regular = 0  # Default encoding for missing Market/Regular
    condition_encoded = 0  # Default encoding for "Clear" condition
    
    if hasattr(shipment, "condition"):
        condition_map = {"Clear": 0, "Clouds": 1, "Rain": 2, "Snow": 3}
        condition_encoded = condition_map.get(shipment.condition, 0)
    
    categorical_features = [
        gps_provider,      # GpsProvider (encoded)
        market_regular,    # Market/Regular (encoded)
        condition_encoded, # condition (encoded)
    ]
    
    # Combine all features (13 total: 10 numeric + 3 categorical)
    all_features = numeric_features + categorical_features
    
    # Create feature snapshot for logging
    snap = {
        "temp_c": numeric_features[0],
        "wind_speed": numeric_features[1],
        "humidity": numeric_features[2],
        "precipitation": numeric_features[3],
        "haversine_km": numeric_features[4],
        "planned_hour": numeric_features[5],
        "planned_dow": numeric_features[6],
        "planned_month": numeric_features[7],
        "is_weekend": numeric_features[8],
        "lead_time_hours": numeric_features[9],
        "gps_provider": categorical_features[0],
        "market_regular": categorical_features[1],
        "condition": categorical_features[2],
    }
    
    # Create feature matrix as DataFrame (1 sample, 13 features)
    # Column names must match exactly what the model was trained with
    column_names = [
        "temp_c", "wind_speed", "humidity", "precipitation",
        "haversine_km", "planned_hour", "planned_dow", "planned_month",
        "is_weekend", "lead_time_hours", "GpsProvider", "Market/Regular", "condition"
    ]
    
    X = pd.DataFrame([all_features], columns=column_names)
    return snap, X

def predict_p_delay(shipment, current_option):
    try:
        model = get_model()
        snap, X = build_features_from_shipment(shipment, current_option)
        p = float(model.predict_proba(X)[0, 1]) if hasattr(model, "predict_proba") else float(model.predict(X)[0])
        return p, snap
    except Exception as e:
        logger.error(f"ML prediction failed: {e}")
        # Return a default probability based on simple heuristics
        snap, _ = build_features_from_shipment(shipment, current_option)
        
        # Enhanced heuristic: detect delays based on shipment status and timing
        base_prob = 0.1
        
        # Check if shipment is actually delayed based on our realistic data
        from django.utils import timezone
        now = timezone.now()
        
        # If shipment is PLANNED but scheduled time has passed, it's delayed
        if shipment.status == "PLANNED" and shipment.scheduled_at < now:
            base_prob += 0.4  # High delay probability for overdue planned shipments
            
        # If shipment is ENROUTE and taking too long, it's delayed
        elif shipment.status == "ENROUTE":
            # Check if it's been enroute for too long (more than 2 days)
            if shipment.scheduled_at < now - timezone.timedelta(days=2):
                base_prob += 0.3  # Medium delay probability for long enroute shipments
                
        # If shipment is DELIVERED but was delivered late, it was delayed
        elif shipment.status == "DELIVERED" and shipment.delivered_at:
            # Check if delivery was significantly late (more than 24 hours after scheduled)
            if shipment.delivered_at > shipment.scheduled_at + timezone.timedelta(hours=24):
                base_prob += 0.5  # High delay probability for late deliveries
        
        # Add weather and distance factors
        if snap.get("haversine_km", 0) > 500:
            base_prob += 0.2
        if snap.get("precipitation", 0) > 5:
            base_prob += 0.3
        if snap.get("condition", 0) > 1:  # Not clear weather
            base_prob += 0.1
            
        return min(base_prob, 0.9), snap
