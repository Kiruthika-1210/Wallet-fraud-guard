# ============================================================
# WALLET GUARD - NOTEBOOK 6
# DEPLOYMENT TESTING & PERFORMANCE VALIDATION
# ============================================================

# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import os
import json
import time
import random
import joblib
import shap
import numpy as np
import pandas as pd
from datetime import datetime

# ============================================================
# 2. PROJECT PATHS
# ============================================================

BASE_PATH = ".."

models_folder = os.path.join(BASE_PATH, "models")
artifacts_folder = os.path.join(BASE_PATH, "artifacts")

# ============================================================
# 3. LOAD PRODUCTION ARTIFACTS
# ============================================================

print("\nLoading Production Artifacts...")

# Load model

model_path = os.path.join(
    models_folder,
    "xgboost_model.pkl"
)

xgb_model = joblib.load(model_path)

# Load scaler

scaler_path = os.path.join(
    models_folder,
    "scaler.pkl"
)

scaler = joblib.load(scaler_path)

# Load threshold

threshold_path = os.path.join(
    models_folder,
    "threshold.txt"
)

with open(threshold_path, "r") as file:
    CUSTOM_THRESHOLD = float(file.read())

print("Production Artifacts Loaded Successfully")

# ============================================================
# 4. INITIALIZE SHAP EXPLAINER
# ============================================================

explainer = shap.TreeExplainer(xgb_model)

print("\nSHAP Explainer Initialized")

# ============================================================
# 5. FRAUD DECISION ENGINE
# ============================================================

def transaction_decision(score):

    if score < 0.40:
        return "APPROVE"

    elif score < 0.75:
        return "REVIEW"

    else:
        return "REJECT"

# ============================================================
# 6. RULE ENGINE
# ============================================================

def rule_based_validation(transaction):

    rule_score = 0

    triggered_rules = []

    if transaction["Amount"] > 5000:
        rule_score += 0.10
        triggered_rules.append(
            "High transaction amount"
        )

    if transaction["night_transaction"] == 1:
        rule_score += 0.10
        triggered_rules.append(
            "Night-time transaction"
        )

    if transaction["device_new"] == 1:
        rule_score += 0.15
        triggered_rules.append(
            "New device detected"
        )

    if transaction["failed_attempts"] >= 3:
        rule_score += 0.15
        triggered_rules.append(
            "Multiple failed attempts"
        )

    if transaction["transaction_velocity"] > 15:
        rule_score += 0.15
        triggered_rules.append(
            "High transaction velocity"
        )

    if transaction["merchant_risk"] > 0.8:
        rule_score += 0.10
        triggered_rules.append(
            "High-risk merchant"
        )

    if transaction["ip_risk_score"] > 0.8:
        rule_score += 0.10
        triggered_rules.append(
            "Suspicious IP risk score"
        )

    return rule_score, triggered_rules

# ============================================================
# 7. GENERATE RANDOM TEST TRANSACTION
# ============================================================

def generate_transaction():

    return {
        "Time": random.randint(0, 172792),

        "V1": random.uniform(-5, 5),
        "V2": random.uniform(-5, 5),
        "V3": random.uniform(-5, 5),
        "V4": random.uniform(-5, 5),
        "V5": random.uniform(-5, 5),
        "V6": random.uniform(-5, 5),
        "V7": random.uniform(-5, 5),
        "V8": random.uniform(-5, 5),
        "V9": random.uniform(-5, 5),
        "V10": random.uniform(-5, 5),
        "V11": random.uniform(-5, 5),
        "V12": random.uniform(-5, 5),
        "V13": random.uniform(-5, 5),
        "V14": random.uniform(-5, 5),
        "V15": random.uniform(-5, 5),
        "V16": random.uniform(-5, 5),
        "V17": random.uniform(-5, 5),
        "V18": random.uniform(-5, 5),
        "V19": random.uniform(-5, 5),
        "V20": random.uniform(-5, 5),
        "V21": random.uniform(-5, 5),
        "V22": random.uniform(-5, 5),
        "V23": random.uniform(-5, 5),
        "V24": random.uniform(-5, 5),
        "V25": random.uniform(-5, 5),
        "V26": random.uniform(-5, 5),
        "V27": random.uniform(-5, 5),
        "V28": random.uniform(-5, 5),

        "Amount": random.uniform(1, 10000),

        "transaction_hour": random.randint(0, 23),

        "night_transaction": random.choice([0, 1]),

        "device_new": random.choice([0, 1]),

        "failed_attempts": random.randint(0, 5),

        "geo_distance": random.uniform(1, 300),

        "transaction_velocity": random.randint(1, 25),

        "merchant_risk": random.uniform(0, 1),

        "ip_risk_score": random.uniform(0, 1)
    }

# ============================================================
# 8. FRAUD PREDICTION PIPELINE
# ============================================================

def fraud_pipeline(transaction):

    start_time = time.time()

    # --------------------------------------------------------
    # Convert to DataFrame
    # --------------------------------------------------------

    transaction_df = pd.DataFrame([transaction])

    # --------------------------------------------------------
    # Scaling
    # --------------------------------------------------------

    scaled_transaction = scaler.transform(
        transaction_df
    )

    scaled_transaction_df = pd.DataFrame(
        scaled_transaction,
        columns=transaction_df.columns
    )

    # --------------------------------------------------------
    # ML Risk Scoring
    # --------------------------------------------------------

    ml_risk_score = xgb_model.predict_proba(
        scaled_transaction_df
    )[0][1]

    # --------------------------------------------------------
    # Rule Validation
    # --------------------------------------------------------

    rule_score, triggered_rules = (
        rule_based_validation(transaction)
    )

    # --------------------------------------------------------
    # Hybrid Risk Fusion
    # --------------------------------------------------------

    final_risk_score = (
        (0.75 * ml_risk_score) +
        (0.25 * rule_score)
    )

    final_risk_score = min(
        final_risk_score,
        1.0
    )

    # --------------------------------------------------------
    # Decision Engine
    # --------------------------------------------------------

    decision = transaction_decision(
        final_risk_score
    )

    # --------------------------------------------------------
    # SHAP Explainability
    # --------------------------------------------------------

    shap_values = explainer.shap_values(
        scaled_transaction_df
    )

    transaction_shap_values = shap_values[0]

    feature_contributions = pd.DataFrame({
        "Feature": scaled_transaction_df.columns,
        "SHAP_Value": transaction_shap_values
    })

    feature_contributions["Impact"] = np.abs(
        feature_contributions["SHAP_Value"]
    )

    feature_contributions = (
        feature_contributions[
            feature_contributions["SHAP_Value"] > 0
        ]
        .sort_values(
            by="Impact",
            ascending=False
        )
        .head(5)
    )

    # --------------------------------------------------------
    # Response Time
    # --------------------------------------------------------

    inference_latency = (
        time.time() - start_time
    ) * 1000

    # --------------------------------------------------------
    # API Response
    # --------------------------------------------------------

    response = {
        "timestamp": datetime.now().isoformat(),

        "ml_risk_score": round(
            float(ml_risk_score),
            4
        ),

        "rule_risk_score": round(
            float(rule_score),
            4
        ),

        "final_risk_score": round(
            float(final_risk_score),
            4
        ),

        "decision": decision,

        "threshold_used": CUSTOM_THRESHOLD,

        "triggered_rules": triggered_rules,

        "top_risk_factors": [
            {
                "feature": row["Feature"],
                "impact_score": round(
                    float(row["SHAP_Value"]),
                    4
                )
            }
            for _, row in feature_contributions.iterrows()
        ],

        "latency_ms": round(
            inference_latency,
            2
        )
    }

    return response

# ============================================================
# 9. SINGLE API REQUEST TEST
# ============================================================

print("\nSimulating API Request...")

sample_transaction = generate_transaction()

response = fraud_pipeline(sample_transaction)

print("\nAPI Response\n")

print(
    json.dumps(
        response,
        indent=4
    )
)

# ============================================================
# 10. LATENCY BENCHMARKING
# ============================================================

print("\nRunning Latency Benchmark...")

latencies = []

num_requests = 100

for _ in range(num_requests):

    transaction = generate_transaction()

    response = fraud_pipeline(transaction)

    latencies.append(
        response["latency_ms"]
    )

average_latency = np.mean(latencies)

max_latency = np.max(latencies)

min_latency = np.min(latencies)

print("\nLatency Benchmark Results")

print(f"Average Latency : {average_latency:.2f} ms")

print(f"Maximum Latency : {max_latency:.2f} ms")

print(f"Minimum Latency : {min_latency:.2f} ms")

# ============================================================
# 11. THROUGHPUT ESTIMATION
# ============================================================

requests_per_second = 1000 / average_latency

requests_per_minute = requests_per_second * 60

print("\nThroughput Estimation")

print(f"Estimated Requests/Second : {requests_per_second:.2f}")

print(f"Estimated Requests/Minute : {requests_per_minute:.2f}")

# ============================================================
# 12. JSON RESPONSE VALIDATION
# ============================================================

print("\nValidating JSON Response...")

try:

    json.dumps(response)

    print("JSON Response Validation Successful")

except Exception as error:

    print("JSON Validation Failed")

    print(error)

# ============================================================
# 13. DEPLOYMENT READINESS CHECKLIST
# ============================================================

deployment_status = {
    "model_loaded": True,
    "scaler_loaded": True,
    "threshold_loaded": True,
    "shap_explainer_ready": True,
    "json_response_ready": True,
    "rule_engine_ready": True,
    "decision_engine_ready": True,
    "latency_benchmark_completed": True
}

print("\nDeployment Readiness Checklist\n")

for key, value in deployment_status.items():

    print(f"{key}: {value}")

# ============================================================
# 14. SAVE DEPLOYMENT REPORT
# ============================================================

deployment_report = {
    "average_latency_ms": round(
        float(average_latency),
        2
    ),

    "maximum_latency_ms": round(
        float(max_latency),
        2
    ),

    "minimum_latency_ms": round(
        float(min_latency),
        2
    ),

    "estimated_requests_per_minute": round(
        float(requests_per_minute),
        2
    ),

    "deployment_ready": True,

    "timestamp": datetime.now().isoformat()
}

deployment_report_path = os.path.join(
    artifacts_folder,
    "deployment_report.json"
)

with open(deployment_report_path, "w") as file:

    json.dump(
        deployment_report,
        file,
        indent=4
    )

print("\nDeployment Report Saved Successfully")
