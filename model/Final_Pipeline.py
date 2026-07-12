# ============================================================
# WALLET GUARD - NOTEBOOK 5
# FINAL FRAUD DETECTION PIPELINE
# ============================================================

# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import os
import json
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
# 3. LOAD TRAINED ARTIFACTS
# ============================================================

print("\nLoading Trained Artifacts...")

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

print("Artifacts Loaded Successfully")

# ============================================================
# 4. INITIALIZE SHAP EXPLAINER
# ============================================================

explainer = shap.TreeExplainer(xgb_model)

print("\nSHAP Explainer Initialized")

# ============================================================
# 5. SAMPLE TRANSACTION INPUT
# ============================================================

# Simulated transaction

transaction = {
    "Time": 50000,
    "V1": -2.3,
    "V2": 1.5,
    "V3": -3.2,
    "V4": 2.1,
    "V5": -1.8,
    "V6": 0.5,
    "V7": -2.4,
    "V8": 1.2,
    "V9": -1.9,
    "V10": -3.5,
    "V11": 2.4,
    "V12": -2.8,
    "V13": 0.1,
    "V14": -4.1,
    "V15": 0.3,
    "V16": -1.2,
    "V17": -2.7,
    "V18": -0.8,
    "V19": 1.1,
    "V20": 0.6,
    "V21": 0.7,
    "V22": -0.5,
    "V23": 0.4,
    "V24": 0.2,
    "V25": 0.1,
    "V26": 0.5,
    "V27": -0.3,
    "V28": 0.2,
    "Amount": 8500,

    # Engineered Fraud Features

    "transaction_hour": 2,
    "night_transaction": 1,
    "device_new": 1,
    "failed_attempts": 5,
    "geo_distance": 120,
    "transaction_velocity": 18,
    "merchant_risk": 0.92,
    "ip_risk_score": 0.88
}

print("\nTransaction Received")

# ============================================================
# 6. CONVERT TRANSACTION TO DATAFRAME
# ============================================================

transaction_df = pd.DataFrame([transaction])

print("\nTransaction Converted to DataFrame")

# ============================================================
# 7. FEATURE SCALING
# ============================================================

scaled_transaction = scaler.transform(transaction_df)

scaled_transaction_df = pd.DataFrame(
    scaled_transaction,
    columns=transaction_df.columns
)

print("\nFeature Scaling Completed")

# ============================================================
# 8. XGBOOST FRAUD RISK SCORING
# ============================================================

ml_risk_score = xgb_model.predict_proba(
    scaled_transaction_df
)[0][1]

print(f"\nML Fraud Risk Score: {ml_risk_score:.4f}")

# ============================================================
# 9. RULE-BASED ANOMALY VALIDATION
# ============================================================

rule_score = 0

rule_triggers = []

# ------------------------------------------------------------
# High Amount Rule
# ------------------------------------------------------------

if transaction["Amount"] > 5000:
    rule_score += 0.10
    rule_triggers.append("High transaction amount")

# ------------------------------------------------------------
# Night Transaction Rule
# ------------------------------------------------------------

if transaction["night_transaction"] == 1:
    rule_score += 0.10
    rule_triggers.append("Night-time transaction")

# ------------------------------------------------------------
# New Device Rule
# ------------------------------------------------------------

if transaction["device_new"] == 1:
    rule_score += 0.15
    rule_triggers.append("New device detected")

# ------------------------------------------------------------
# Failed Login Attempts Rule
# ------------------------------------------------------------

if transaction["failed_attempts"] >= 3:
    rule_score += 0.15
    rule_triggers.append("Multiple failed attempts")

# ------------------------------------------------------------
# High Transaction Velocity Rule
# ------------------------------------------------------------

if transaction["transaction_velocity"] > 15:
    rule_score += 0.15
    rule_triggers.append("High transaction velocity")

# ------------------------------------------------------------
# Merchant Risk Rule
# ------------------------------------------------------------

if transaction["merchant_risk"] > 0.8:
    rule_score += 0.10
    rule_triggers.append("High-risk merchant")

# ------------------------------------------------------------
# IP Risk Rule
# ------------------------------------------------------------

if transaction["ip_risk_score"] > 0.8:
    rule_score += 0.10
    rule_triggers.append("Suspicious IP risk score")

print(f"\nRule-Based Risk Score: {rule_score:.4f}")

print("\nTriggered Rules")

for rule in rule_triggers:
    print(f"- {rule}")

# ============================================================
# 10. HYBRID RISK FUSION
# ============================================================

# Combine ML score + rule score

final_risk_score = (
    (0.55 * ml_risk_score) +
    (0.45 * rule_score)
)

# Ensure score remains between 0 and 1

final_risk_score = min(final_risk_score, 1.0)

print(f"\nFinal Hybrid Risk Score: {final_risk_score:.4f}")

# ============================================================
# 11. 3-TIER DECISION ENGINE
# ============================================================

def transaction_decision(score):

    if score < 0.30:
        return "APPROVE"
    
    elif score < 0.50:
        return "REVIEW"
    
    else:
        return "REJECT"

decision = transaction_decision(final_risk_score)

print(f"\nTransaction Decision: {decision}")

# ============================================================
# 12. SHAP EXPLAINABILITY
# ============================================================

print("\nGenerating SHAP Explanations...")

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

feature_contributions = feature_contributions.sort_values(
    by="Impact",
    ascending=False
)

top_risk_factors = feature_contributions[
    feature_contributions["SHAP_Value"] > 0
].head(5)

print("\nTop Fraud Risk Contributors\n")

print(top_risk_factors)

# ============================================================
# 13. HUMAN-READABLE FRAUD EXPLANATION
# ============================================================

human_explanations = []

print("\nHuman-Readable Fraud Explanations\n")

for _, row in top_risk_factors.iterrows():

    feature = row["Feature"]

    impact = row["SHAP_Value"]

    if impact > 0:

        explanation = (
            f"{feature} increased fraud risk "
            f"by {abs(impact):.4f}"
        )

    else:

        explanation = (
            f"{feature} reduced fraud risk "
            f"by {abs(impact):.4f}"
        )

    human_explanations.append(explanation)

    print(explanation)

# ============================================================
# 14. BACKEND-READY RESPONSE PAYLOAD
# ============================================================

response_payload = {
    "timestamp": datetime.now().isoformat(),

    "ml_risk_score": round(float(ml_risk_score), 4),

    "rule_risk_score": round(float(rule_score), 4),

    "final_risk_score": round(float(final_risk_score), 4),

    "threshold_used": CUSTOM_THRESHOLD,

    "decision": decision,

    "triggered_rules": rule_triggers,

    "top_risk_factors": [
        {
            "feature": row["Feature"],
            "impact_score": round(
                float(row["SHAP_Value"]),
                4
            )
        }
        for _, row in top_risk_factors.iterrows()
    ],

    "human_explanations": human_explanations
}

print("\nBackend-Ready Fraud Response\n")

print(
    json.dumps(
        response_payload,
        indent=4
    )
)

# ============================================================
# 15. AUDIT LOGGING STRUCTURE
# ============================================================

audit_log = {
    "transaction_id": "TXN_1001",

    "decision": decision,

    "risk_score": round(
        float(final_risk_score),
        4
    ),

    "timestamp": datetime.now().isoformat(),

    "rules_triggered": rule_triggers,

    "top_explanations": human_explanations
}

audit_log_path = os.path.join(
    artifacts_folder,
    "fraud_audit_log.json"
)

with open(audit_log_path, "w") as file:
    json.dump(
        audit_log,
        file,
        indent=4
    )

print("\nAudit Log Saved Successfully")

