# ============================================================
# WALLET GUARD - NOTEBOOK 3
# MODEL TRAINING & FRAUD RISK SCORING
# ============================================================

# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    precision_recall_curve
)

# ============================================================
# 2. RANDOM SEED
# ============================================================

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

# ============================================================
# 3. PROJECT PATHS
# ============================================================

BASE_PATH = ".."

processed_folder = os.path.join(BASE_PATH, "processed")
models_folder = os.path.join(BASE_PATH, "models")
artifacts_folder = os.path.join(BASE_PATH, "artifacts")

os.makedirs(models_folder, exist_ok=True)
os.makedirs(artifacts_folder, exist_ok=True)

# ============================================================
# 4. LOAD PREPROCESSED DATA
# ============================================================

X_train_path = os.path.join(
    processed_folder,
    "X_train_resampled.csv"
)

y_train_path = os.path.join(
    processed_folder,
    "y_train_resampled.csv"
)

X_test_path = os.path.join(
    processed_folder,
    "X_test_scaled.csv"
)

y_test_path = os.path.join(
    processed_folder,
    "y_test.csv"
)

# Load files

X_train = pd.read_csv(X_train_path)

y_train = pd.read_csv(y_train_path).values.ravel()

X_test = pd.read_csv(X_test_path)

y_test = pd.read_csv(y_test_path).values.ravel()

print("\nPreprocessed Datasets Loaded Successfully")

print("X_train:", X_train.shape)
print("X_test :", X_test.shape)

# ============================================================
# 5. TRAIN XGBOOST MODEL
# ============================================================

print("\nTraining XGBoost Fraud Detection Model...")

xgb_model = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective='binary:logistic',
    eval_metric='logloss',
    random_state=RANDOM_STATE,
    n_jobs=-1
)

xgb_model.fit(
    X_train,
    y_train
)

print("Model Training Completed Successfully")

# ============================================================
# 6. PREDICTION PROBABILITIES
# ============================================================

y_scores = xgb_model.predict_proba(X_test)[:, 1]

print("\nPrediction Probabilities Generated")

# ============================================================
# 7. THRESHOLD TUNING
# REDUCING FALSE POSITIVES
# ============================================================

# Default threshold = 0.5
# Higher threshold helps reduce false-positive fraud alerts

CUSTOM_THRESHOLD = 0.75

y_pred = (
    y_scores >= CUSTOM_THRESHOLD
).astype(int)

print(f"\nCustom Threshold Applied: {CUSTOM_THRESHOLD}")

# ============================================================
# 8. MODEL EVALUATION
# ============================================================

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(y_test, y_pred)

recall = recall_score(y_test, y_pred)

f1 = f1_score(y_test, y_pred)

roc_auc = roc_auc_score(y_test, y_scores)

print("\n================ MODEL PERFORMANCE ================\n")

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")
print(f"ROC-AUC  : {roc_auc:.4f}")

# ============================================================
# 9. CLASSIFICATION REPORT
# ============================================================

print("\nClassification Report\n")

print(
    classification_report(
        y_test,
        y_pred
    )
)

# ============================================================
# 10. CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    y_test,
    y_pred
)

print("\nConfusion Matrix\n")

print(cm)

# Extract confusion matrix values

tn, fp, fn, tp = cm.ravel()

# Calculate False Positive Rate

false_positive_rate = fp / (fp + tn)

print(f"\nFalse Positive Rate: {false_positive_rate:.6f}")

# ============================================================
# 11. CONFUSION MATRIX VISUALIZATION
# ============================================================

plt.figure(figsize=(6, 5))

plt.imshow(cm, cmap='Blues')

plt.title("Confusion Matrix")

plt.colorbar()

plt.xlabel("Predicted")
plt.ylabel("Actual")

for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        plt.text(
            j,
            i,
            str(cm[i, j]),
            ha='center',
            va='center',
            color='black'
        )

conf_matrix_path = os.path.join(
    artifacts_folder,
    "confusion_matrix.png"
)

plt.savefig(conf_matrix_path)

plt.show()

print("\nConfusion Matrix Saved")

# ============================================================
# 12. PRECISION-RECALL ANALYSIS
# ============================================================

precision_vals, recall_vals, thresholds = precision_recall_curve(
    y_test,
    y_scores
)

plt.figure(figsize=(8, 5))

plt.plot(
    recall_vals,
    precision_vals
)

plt.title("Precision-Recall Curve")

plt.xlabel("Recall")
plt.ylabel("Precision")

pr_curve_path = os.path.join(
    artifacts_folder,
    "precision_recall_curve.png"
)

plt.savefig(pr_curve_path)

plt.show()

print("\nPrecision-Recall Curve Saved")

# ============================================================
# 13. FEATURE IMPORTANCE
# ============================================================

feature_importance = pd.DataFrame({
    "Feature": X_train.columns,
    "Importance": xgb_model.feature_importances_
})

feature_importance = feature_importance.sort_values(
    by="Importance",
    ascending=False
)

print("\nTop 10 Important Features\n")

print(feature_importance.head(10))

# ============================================================
# 14. FEATURE IMPORTANCE VISUALIZATION
# ============================================================

top_features = feature_importance.head(10)

plt.figure(figsize=(10, 6))

plt.barh(
    top_features["Feature"],
    top_features["Importance"]
)

plt.title("Top 10 Feature Importances")

plt.xlabel("Importance Score")

plt.gca().invert_yaxis()

feature_importance_path = os.path.join(
    artifacts_folder,
    "feature_importance.png"
)

plt.savefig(feature_importance_path)

plt.show()

print("\nFeature Importance Graph Saved")

# ============================================================
# 15. SAVE TRAINED MODEL
# ============================================================

model_path = os.path.join(
    models_folder,
    "xgboost_model.pkl"
)

joblib.dump(
    xgb_model,
    model_path
)

print("\nTrained Model Saved Successfully")
print(model_path)

# ============================================================
# 16. SAVE MODEL METRICS
# ============================================================

metrics_report = f"""
============================================================
WALLET GUARD - MODEL PERFORMANCE REPORT
============================================================

Accuracy  : {accuracy:.4f}
Precision : {precision:.4f}
Recall    : {recall:.4f}
F1 Score  : {f1:.4f}
ROC-AUC   : {roc_auc:.4f}

Threshold Used : {CUSTOM_THRESHOLD}

Objective:
Reduce false-positive fraud alerts using
threshold tuning and risk-based scoring.

============================================================
"""

metrics_path = os.path.join(
    artifacts_folder,
    "metrics_report.txt"
)

with open(metrics_path, "w") as file:
    file.write(metrics_report)

print("\nMetrics Report Saved Successfully")

# ============================================================
# 17. FRAUD DECISION ENGINE PREPARATION
# ============================================================

def transaction_decision(risk_score):

    if risk_score < 0.40:
        return "APPROVE"

    elif risk_score < 0.75:
        return "REVIEW"

    else:
        return "REJECT"

# Example

sample_score = 0.82

decision = transaction_decision(sample_score)

print("\nSample Fraud Decision Engine")

print(f"Risk Score : {sample_score}")
print(f"Decision   : {decision}")

threshold_path = os.path.join(
    models_folder,
    "threshold.txt"
)

with open(threshold_path, "w") as file:
    file.write(str(CUSTOM_THRESHOLD))

print("\nThreshold Saved Successfully")
print(threshold_path)