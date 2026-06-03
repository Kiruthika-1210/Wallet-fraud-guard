# ============================================================
# WALLET GUARD - NOTEBOOK 2
# EDA & DATA PREPROCESSING
# ============================================================

# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from imblearn.over_sampling import SMOTE

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
# 4. LOAD PROCESSED DATASET
# ============================================================

# Replace filename if needed

dataset_path = os.path.join(
    processed_folder,
    "creditcard_processed_20260603_201310.csv"
)

df = pd.read_csv(dataset_path)

print("\nDataset Loaded Successfully")
print(f"Dataset Shape: {df.shape}")

# ============================================================
# 5. DATASET OVERVIEW
# ============================================================

print("\nFirst 5 Rows")
print(df.head())

print("\nDataset Info")
print(df.info())

print("\nMissing Values")
print(df.isnull().sum())

# ============================================================
# 6. FRAUD DISTRIBUTION
# ============================================================

fraud_counts = df["Class"].value_counts()

print("\nFraud Distribution")
print(fraud_counts)

plt.figure(figsize=(8, 5))

fraud_counts.plot(
    kind="bar",
    color=["skyblue", "red"]
)

plt.title("Fraud vs Non-Fraud Transactions")
plt.xlabel("Class")
plt.ylabel("Count")
plt.xticks(rotation=0)

for index, value in enumerate(fraud_counts):
    plt.text(index, value, str(value), ha='center')

plt.show()

# ============================================================
# 7. FEATURE ANALYSIS
# ============================================================

selected_features = [
    "Amount",
    "transaction_hour",
    "geo_distance",
    "transaction_velocity",
    "merchant_risk",
    "ip_risk_score"
]

print("\nFeature Statistics")
print(df[selected_features].describe())

# ============================================================
# 8. OUTLIER ANALYSIS
# ============================================================

plt.figure(figsize=(10, 6))

plt.boxplot(df["Amount"])

plt.title("Transaction Amount Outlier Analysis")

plt.show()

# ============================================================
# 9. CORRELATION ANALYSIS
# ============================================================

correlation_features = [
    "Amount",
    "transaction_hour",
    "night_transaction",
    "device_new",
    "failed_attempts",
    "geo_distance",
    "transaction_velocity",
    "merchant_risk",
    "ip_risk_score",
    "Class"
]

correlation_matrix = df[correlation_features].corr()

print("\nCorrelation Matrix")
print(correlation_matrix)

# ============================================================
# 10. FEATURE & TARGET SPLIT
# ============================================================

X = df.drop("Class", axis=1)

y = df["Class"]

print("\nFeature Matrix Shape:", X.shape)
print("Target Shape:", y.shape)

# ============================================================
# 11. TRAIN-TEST SPLIT
# ============================================================

# IMPORTANT:
# Split BEFORE SMOTE to avoid data leakage

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=RANDOM_STATE
)

print("\nTrain-Test Split Completed")

print("X_train:", X_train.shape)
print("X_test :", X_test.shape)

print("y_train:", y_train.shape)
print("y_test :", y_test.shape)

# ============================================================
# 12. FEATURE SCALING
# ============================================================

scaler = StandardScaler()

# Fit ONLY on training data

X_train_scaled = scaler.fit_transform(X_train)

# Transform test data

X_test_scaled = scaler.transform(X_test)

print("\nFeature Scaling Completed")

# ============================================================
# 13. APPLY SMOTE ONLY ON TRAINING DATA
# ============================================================

print("\nApplying SMOTE on Training Data...")

smote = SMOTE(
    random_state=RANDOM_STATE
)

X_train_resampled, y_train_resampled = smote.fit_resample(
    X_train_scaled,
    y_train
)

print("SMOTE Applied Successfully")

print("\nBefore SMOTE")
print(y_train.value_counts())

print("\nAfter SMOTE")
print(pd.Series(y_train_resampled).value_counts())

# ============================================================
# 14. SAVE SCALER
# ============================================================

scaler_path = os.path.join(
    models_folder,
    "scaler.pkl"
)

joblib.dump(
    scaler,
    scaler_path
)

print("\nScaler Saved Successfully")
print(scaler_path)

# ============================================================
# 15. SAVE PREPROCESSED DATA
# ============================================================

# Save training data

X_train_path = os.path.join(
    processed_folder,
    "X_train_resampled.csv"
)

y_train_path = os.path.join(
    processed_folder,
    "y_train_resampled.csv"
)

# Save test data

X_test_path = os.path.join(
    processed_folder,
    "X_test_scaled.csv"
)

y_test_path = os.path.join(
    processed_folder,
    "y_test.csv"
)

# Convert arrays to DataFrames

X_train_resampled_df = pd.DataFrame(
    X_train_resampled,
    columns=X.columns
)

X_test_scaled_df = pd.DataFrame(
    X_test_scaled,
    columns=X.columns
)

# Save files

X_train_resampled_df.to_csv(
    X_train_path,
    index=False
)

pd.DataFrame(y_train_resampled).to_csv(
    y_train_path,
    index=False
)

X_test_scaled_df.to_csv(
    X_test_path,
    index=False
)

pd.DataFrame(y_test).to_csv(
    y_test_path,
    index=False
)

print("\nPreprocessed Datasets Saved Successfully")

# ============================================================
# SAVE FEATURE ORDER
# ============================================================

feature_order = pd.DataFrame({
    "feature": X.columns
})

feature_order_path = os.path.join(
    models_folder,
    "feature_order.csv"
)

feature_order.to_csv(
    feature_order_path,
    index=False
)

print("\nFeature Order Saved Successfully")
print(feature_order_path)

# ============================================================
# 16. PREPROCESSING METADATA
# ============================================================

metadata = {
    "original_rows": len(df),
    "training_rows_after_smote": len(X_train_resampled_df),
    "test_rows": len(X_test_scaled_df),
    "total_features": X.shape[1],
    "fraud_class_percentage": float(
        round(
            (fraud_counts[1] / fraud_counts.sum()) * 100,
            4
        )
    )
}

print("\nPreprocessing Metadata")
print(metadata)
