# ============================================================
# WALLET GUARD - FRAUD MODEL SERVICE
# ============================================================

import os
import joblib
import pandas as pd

# ============================================================
# MODEL PATHS
# ============================================================

MODEL_PATH = "models/xgboost_model.pkl"

SCALER_PATH = "models/scaler.pkl"

THRESHOLD_PATH = "models/threshold.txt"

FEATURE_ORDER_PATH = "models/feature_order.csv"

# ============================================================
# GLOBAL ARTIFACTS
# ============================================================

model = None

scaler = None

threshold = 0.75

feature_order = []

# ============================================================
# LOAD ARTIFACTS
# ============================================================

def initialize_artifacts():

    global model
    global scaler
    global threshold
    global feature_order

    print("\nLoading ML Artifacts...")

    # --------------------------------------------------------
    # Load XGBoost Model
    # --------------------------------------------------------

    if os.path.exists(MODEL_PATH):

        model = joblib.load(MODEL_PATH)

        print("XGBoost Model Loaded")

    else:

        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    # --------------------------------------------------------
    # Load Scaler
    # --------------------------------------------------------

    if os.path.exists(SCALER_PATH):

        scaler = joblib.load(SCALER_PATH)

        print("Scaler Loaded")

    else:

        raise FileNotFoundError(
            f"Scaler file not found: {SCALER_PATH}"
        )

    # --------------------------------------------------------
    # Load Threshold
    # --------------------------------------------------------

    if os.path.exists(THRESHOLD_PATH):

        with open(THRESHOLD_PATH, "r") as file:

            threshold = float(file.read())

        print("Threshold Loaded")

    else:

        print("Threshold file missing.")
        print("Using default threshold = 0.75")

    # --------------------------------------------------------
    # Load Feature Order
    # --------------------------------------------------------

    if os.path.exists(FEATURE_ORDER_PATH):

        feature_df = pd.read_csv(
            FEATURE_ORDER_PATH
        )

        feature_order = (
            feature_df["feature"]
            .tolist()
        )

        print("Feature Order Loaded")

    else:

        raise FileNotFoundError(
            f"Feature order file missing: "
            f"{FEATURE_ORDER_PATH}"
        )

    print("\nAll ML Artifacts Loaded Successfully")

# ============================================================
# GET FEATURE ORDER
# ============================================================

def get_feature_order():

    return feature_order

# ============================================================
# GET THRESHOLD
# ============================================================

def get_threshold():

    return threshold

# ============================================================
# PREPARE INPUT FEATURES
# ============================================================

def prepare_features(features: dict):

    # --------------------------------------------------------
    # Fill Missing Features
    # --------------------------------------------------------

    prepared_data = {}

    for feature in feature_order:

        prepared_data[feature] = (
            features.get(feature, 0)
        )

    # --------------------------------------------------------
    # Convert to DataFrame
    # --------------------------------------------------------

    feature_df = pd.DataFrame(
        [prepared_data]
    )

    return feature_df

# ============================================================
# SCALE FEATURES
# ============================================================

def scale_features(feature_df):

    scaled_array = scaler.transform(
        feature_df
    )

    scaled_df = pd.DataFrame(
        scaled_array,
        columns=feature_df.columns
    )

    return scaled_df

# ============================================================
# PREDICT FRAUD RISK SCORE
# ============================================================

def predict(features: dict):

    # --------------------------------------------------------
    # Prepare Features
    # --------------------------------------------------------

    feature_df = prepare_features(
        features
    )

    # --------------------------------------------------------
    # Scale Features
    # --------------------------------------------------------

    scaled_df = scale_features(
        feature_df
    )

    # --------------------------------------------------------
    # Predict Probability
    # --------------------------------------------------------

    risk_score = (
        model.predict_proba(scaled_df)[0][1]
    )

    return float(risk_score)

# ============================================================
# PREDICT FRAUD CLASS
# ============================================================

def predict_class(features: dict):

    risk_score = predict(features)

    if risk_score >= threshold:

        return 1

    return 0

# ============================================================
# FULL FRAUD ANALYSIS
# ============================================================

def analyze_transaction(features: dict):

    risk_score = predict(features)

    fraud_class = predict_class(features)

    return {
        "risk_score": round(
            float(risk_score),
            4
        ),

        "fraud_prediction": fraud_class,

        "threshold_used": threshold
    }

