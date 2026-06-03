# ============================================================
# WALLET GUARD - NOTEBOOK 4
# SHAP EXPLAINABILITY & FRAUD RISK ATTRIBUTION
# ============================================================

# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import os
import joblib
import shap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# 2. PROJECT PATHS
# ============================================================

BASE_PATH = ".."

processed_folder = os.path.join(BASE_PATH, "processed")
models_folder = os.path.join(BASE_PATH, "models")
artifacts_folder = os.path.join(BASE_PATH, "artifacts")

os.makedirs(artifacts_folder, exist_ok=True)

# ============================================================
# 3. LOAD TRAINED MODEL
# ============================================================

model_path = os.path.join(
    models_folder,
    "xgboost_model.pkl"
)

xgb_model = joblib.load(model_path)

print("\nTrained XGBoost Model Loaded Successfully")

# ============================================================
# 4. LOAD TEST DATA
# ============================================================

X_test_path = os.path.join(
    processed_folder,
    "X_test_scaled.csv"
)

y_test_path = os.path.join(
    processed_folder,
    "y_test.csv"
)

X_test = pd.read_csv(X_test_path)

y_test = pd.read_csv(y_test_path).values.ravel()

print("\nTest Dataset Loaded Successfully")

print("X_test Shape:", X_test.shape)

# ============================================================
# 5. INITIALIZE SHAP EXPLAINER
# ============================================================

print("\nInitializing SHAP Explainer...")

explainer = shap.TreeExplainer(xgb_model)

print("SHAP Explainer Initialized Successfully")

# ============================================================
# 6. GENERATE SHAP VALUES
# ============================================================

print("\nGenerating SHAP Values...")

# Use subset for faster explainability

# Use subset for faster explainability

fraud_indices = np.where(y_test == 1)[0]

# Select fraud samples only

sample_size = 100

selected_indices = fraud_indices[:sample_size]

X_sample = X_test.iloc[selected_indices]

shap_values = explainer.shap_values(X_sample)

print("SHAP Values Generated Successfully")

# ============================================================
# 7. GLOBAL FEATURE IMPORTANCE
# ============================================================

print("\nGenerating Global Feature Importance...")

plt.figure()

shap.summary_plot(
    shap_values,
    X_sample,
    show=False
)

summary_plot_path = os.path.join(
    artifacts_folder,
    "shap_summary_plot.png"
)

plt.savefig(
    summary_plot_path,
    bbox_inches='tight'
)

plt.close()

print("SHAP Summary Plot Saved")

# ============================================================
# 8. LOCAL FRAUD TRANSACTION EXPLANATION
# ============================================================

# Select a suspicious transaction

transaction_index = 0

transaction_data = X_sample.iloc[transaction_index]

transaction_shap_values = shap_values[transaction_index]

print("\nTransaction Selected for Explainability")

print(f"Transaction Index: {transaction_index}")

# ============================================================
# 9. GENERATE FRAUD REASONS
# ============================================================

feature_contributions = pd.DataFrame({
    "Feature": X_sample.columns,
    "SHAP_Value": transaction_shap_values
})

feature_contributions["Impact"] = np.abs(
    feature_contributions["SHAP_Value"]
)

feature_contributions = feature_contributions.sort_values(
    by="Impact",
    ascending=False
)

top_reasons = feature_contributions.head(5)

print("\nTop Fraud Risk Contributors\n")

print(top_reasons)

# ============================================================
# 10. HUMAN-READABLE FRAUD EXPLANATIONS
# ============================================================

print("\nHuman-Readable Fraud Explanation\n")

for _, row in top_reasons.iterrows():

    feature = row["Feature"]

    impact = row["SHAP_Value"]

    direction = (
        "increased"
        if impact > 0
        else "reduced"
    )

    print(
        f"{feature} {direction} fraud risk "
        f"by {abs(impact):.4f}"
    )

# ============================================================
# 11. SHAP WATERFALL VISUALIZATION
# ============================================================

print("\nGenerating SHAP Waterfall Plot...")

waterfall_plot_path = os.path.join(
    artifacts_folder,
    "shap_waterfall_plot.png"
)

plt.figure()

shap.plots._waterfall.waterfall_legacy(
    explainer.expected_value,
    transaction_shap_values,
    feature_names=X_sample.columns,
    show=False
)

plt.savefig(
    waterfall_plot_path,
    bbox_inches='tight'
)

plt.close()

print("SHAP Waterfall Plot Saved")

# ============================================================
# 12. SHAP FORCE PLOT
# ============================================================

print("\nGenerating SHAP Force Plot...")

force_plot = shap.force_plot(
    explainer.expected_value,
    transaction_shap_values,
    transaction_data,
    matplotlib=False
)

force_plot_path = os.path.join(
    artifacts_folder,
    "shap_force_plot.html"
)

shap.save_html(
    force_plot_path,
    force_plot
)

print("SHAP Force Plot Saved")

# ============================================================
# 13. FRAUD EXPLANATION REPORT
# ============================================================

fraud_report = f"""
============================================================
WALLET GUARD - FRAUD EXPLANATION REPORT
============================================================

Transaction Index: {transaction_index}

Top Fraud Risk Contributors:

"""

for _, row in top_reasons.iterrows():

    fraud_report += (
        f"\n- {row['Feature']} "
        f"(Impact Score: {row['SHAP_Value']:.4f})"
    )

fraud_report += """

============================================================

This report was generated using SHAP explainability
for audit-ready fraud attribution.

============================================================
"""

report_path = os.path.join(
    artifacts_folder,
    "fraud_explanation_report.txt"
)

with open(report_path, "w") as file:
    file.write(fraud_report)

print("\nFraud Explanation Report Saved")

# ============================================================
# 14. BACKEND-READY EXPLANATION JSON
# ============================================================

explanation_payload = {
    "transaction_index": int(transaction_index),
    "top_risk_factors": [
        {
            "feature": row["Feature"],
            "impact_score": float(row["SHAP_Value"])
        }
        for _, row in top_reasons.iterrows()
    ]
}

print("\nBackend-Ready Explanation Payload\n")

print(explanation_payload)

