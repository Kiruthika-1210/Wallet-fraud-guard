# ============================================================
# WALLET GUARD - NOTEBOOK 1
# DATA COLLECTION & DATASET PREPARATION
# ============================================================

# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ============================================================
# 2. RANDOM SEED FOR REPRODUCIBILITY
# ============================================================

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

# ============================================================
# 3. CREATE PROJECT FOLDER STRUCTURE
# ============================================================

BASE_PATH = ".."

folders = [
    "processed",
    "models",
    "artifacts"
]

for folder in folders:
    os.makedirs(os.path.join(BASE_PATH, folder), exist_ok=True)

print("Project folders created successfully.")

# ============================================================
# 4. LOAD ORIGINAL DATASET
# ============================================================

# Folder Structure:
#
# Wallet Fraud Guard/
# │
# ├── data/
# │   └── creditcard.csv
# │
# ├── model/
# │   └── Data_Collection.py

dataset_path = os.path.join(BASE_PATH, "data", "creditcard.csv")

df = pd.read_csv(dataset_path)

print("\nDataset Loaded Successfully")
print(f"Dataset Shape: {df.shape}")

# ============================================================
# 5. BASIC DATA INSPECTION
# ============================================================

print("\nFirst 5 Rows")
print(df.head())

print("\nDataset Info")
print(df.info())

print("\nMissing Values")
print(df.isnull().sum())

print("\nDuplicate Rows")
print(df.duplicated().sum())

print("\nStatistical Summary")
print(df.describe())

# ============================================================
# 6. REMOVE DUPLICATES
# ============================================================

df = df.drop_duplicates()

print("\nShape After Removing Duplicates")
print(df.shape)

# ============================================================
# 7. FRAUD DISTRIBUTION ANALYSIS
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
# 8. FEATURE ENGINEERING
# ADD REALISTIC FRAUD-RELATED FEATURES
# ============================================================

print("\nAdding Realistic Fraud Features...")

n_rows = len(df)

# ------------------------------------------------------------
# Transaction Hour
# ------------------------------------------------------------

df["transaction_hour"] = np.random.randint(
    0,
    24,
    n_rows
)

# ------------------------------------------------------------
# Night Transaction Flag
# ------------------------------------------------------------

df["night_transaction"] = df["transaction_hour"].apply(
    lambda x: 1 if x <= 5 else 0
)

# ------------------------------------------------------------
# New Device Usage
# ------------------------------------------------------------

df["device_new"] = np.random.choice(
    [0, 1],
    size=n_rows,
    p=[0.92, 0.08]
)

# ------------------------------------------------------------
# Failed Login Attempts
# ------------------------------------------------------------

df["failed_attempts"] = np.random.poisson(
    lam=1,
    size=n_rows
)

# ------------------------------------------------------------
# Geographic Distance
# ------------------------------------------------------------

df["geo_distance"] = np.random.normal(
    loc=20,
    scale=15,
    size=n_rows
)

df["geo_distance"] = np.abs(df["geo_distance"])

# ------------------------------------------------------------
# Transaction Velocity
# ------------------------------------------------------------

df["transaction_velocity"] = np.random.randint(
    1,
    20,
    n_rows
)

# ------------------------------------------------------------
# Merchant Risk Score
# ------------------------------------------------------------

df["merchant_risk"] = np.random.uniform(
    0,
    1,
    n_rows
)

# ------------------------------------------------------------
# IP Risk Score
# ------------------------------------------------------------

df["ip_risk_score"] = np.random.uniform(
    0,
    1,
    n_rows
)

print("Additional fraud-related features added successfully.")

# ============================================================
# 9. FEATURE PREVIEW
# ============================================================

print("\nEngineered Feature Preview")

print(
    df[
        [
            "transaction_hour",
            "night_transaction",
            "device_new",
            "failed_attempts",
            "geo_distance",
            "transaction_velocity",
            "merchant_risk",
            "ip_risk_score"
        ]
    ].head()
)

# ============================================================
# 10. CORRELATION CHECK FOR NEW FEATURES
# ============================================================

new_features = [
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

correlation_matrix = df[new_features].corr()

print("\nCorrelation Matrix")
print(correlation_matrix)

# ============================================================
# 11. SAVE CLEANED & ENGINEERED DATASET
# ============================================================

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

processed_file = f"creditcard_processed_{timestamp}.csv"

processed_path = os.path.join(
    BASE_PATH,
    "processed",
    processed_file
)

df.to_csv(processed_path, index=False)

print("\nProcessed Dataset Saved Successfully")
print(processed_path)

# ============================================================
# 12. DATASET METADATA
# ============================================================

metadata = {
    "total_rows_after_cleaning": len(df),
    "total_columns": len(df.columns),
    "fraud_percentage": float(
    round(
        (fraud_counts[1] / fraud_counts.sum()) * 100,
        4
    )
    ),
    "timestamp": timestamp
}

print("\nDataset Metadata")
print(metadata)

