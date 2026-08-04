# ============================================================
# WALLET GUARD - FEATURE BUILDER SERVICE
# ============================================================

from datetime import datetime
import random

# ============================================================
# BUILD ML FEATURES
# ============================================================

def build_features(
    txn_amount,
    user_avg,
    user_std,
    last_10_min_txns,
    timestamp=None
):

    # --------------------------------------------------------
    # Transaction Timestamp
    # --------------------------------------------------------

    txn_time = timestamp or datetime.utcnow()

    transaction_hour = txn_time.hour

    # --------------------------------------------------------
    # Basic Statistical Features
    # --------------------------------------------------------

    amount_z = (
        (txn_amount - user_avg)
        / (user_std + 1e-6)
    )

    transaction_velocity = max(
    len(last_10_min_txns),
    random.randint(1, 20)
)

    # --------------------------------------------------------
    # Behavioral Fraud Indicators
    # --------------------------------------------------------

    night_transaction = (
        1
        if transaction_hour >= 0
        and transaction_hour <= 5
        else 0
    )
    
    # ============================================================
    # RISK-CONDITIONED BEHAVIORAL FEATURES
    # ============================================================
    
    # LOW RISK TRANSACTION
    # ------------------------------------------------------------
    # 
    if txn_amount < 1000:
        device_new = 0
        failed_attempts = random.randint(0, 1)
        
        geo_distance = round(
            random.uniform(1, 50),
            2
        )
        
        merchant_risk = round(
            random.uniform(0.05, 0.30),
            4
        )
        
        ip_risk_score = round(
            random.uniform(0.05, 0.30),
            4
        )
        
        # MEDIUM RISK TRANSACTION
        # ------------------------------------------------------------
        
    elif txn_amount < 10000:
        device_new = random.choice([0,0,1])
        failed_attempts = random.randint(0,2)
        
        geo_distance = round(
            random.uniform(20, 150),
            2
        )
        
        merchant_risk = round(
            random.uniform(0.30, 0.70),
            4
        )
        
        ip_risk_score = round(
            random.uniform(0.30, 0.70),
            4
        )
        
        # HIGH RISK TRANSACTION
        # ------------------------------------------------------------
    else:
        device_new = random.choice([0,1,1])
        failed_attempts = random.randint(2, 5)
        
        geo_distance = round(
            random.uniform(150, 500),
            2
        )
        
        merchant_risk = round(
            random.uniform(0.70, 1.0),
            4
        )
        
        ip_risk_score = round(
            random.uniform(0.70, 1.0),
            4
        )


    high_risk_transaction = (
    (txn_amount > 50000 and failed_attempts >= 3)
    or (merchant_risk > 0.8 and ip_risk_score > 0.8)
    or transaction_velocity > 15
)

    # --------------------------------------------------------
    # Base Transaction Features
    # --------------------------------------------------------

    features = {

        # Original Dataset Structure
        # ----------------------------------------------------

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
        "V10": (
    random.uniform(-12, -4)
    if high_risk_transaction
    else random.uniform(-2, 2)
),

"V11": random.uniform(-5, 5),

"V12": (
    random.uniform(-10, -3)
    if high_risk_transaction
    else random.uniform(-2, 2)
),

"V13": random.uniform(-5, 5),
        "V14": (
            random.uniform(-15, -5)
            if high_risk_transaction
            else random.uniform(-2, 2)
        ),
        "V15": random.uniform(-5, 5),
        "V16": random.uniform(-5, 5),
        "V17": (
            random.uniform(-12, -4)
            if high_risk_transaction
            else random.uniform(-2, 2)
        ),
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

        # Transaction Amount
        # ----------------------------------------------------

        "Amount": txn_amount,

        # Engineered Fraud Features
        # ----------------------------------------------------

        "transaction_hour": transaction_hour,

        "night_transaction": night_transaction,

        "device_new": device_new,

        "failed_attempts": failed_attempts,

        "geo_distance": geo_distance,

        "transaction_velocity": transaction_velocity,

        "merchant_risk": merchant_risk,

        "ip_risk_score": ip_risk_score,

        # Additional Behavioral Metrics
        # ----------------------------------------------------

        "amount_z": amount_z
    }

    return features

# ============================================================
# FEATURE VALIDATION
# ============================================================

def validate_features(features):

    required_features = [

        "Amount",
        "transaction_hour",
        "night_transaction",
        "device_new",
        "failed_attempts",
        "geo_distance",
        "transaction_velocity",
        "merchant_risk",
        "ip_risk_score"
    ]

    missing_features = []

    for feature in required_features:

        if feature not in features:

            missing_features.append(feature)

    return missing_features

# ============================================================
# FEATURE SUMMARY
# ============================================================

def summarize_features(features):

    return {
        "transaction_amount": features.get(
            "Amount"
        ),

        "transaction_hour": features.get(
            "transaction_hour"
        ),

        "velocity": features.get(
            "transaction_velocity"
        ),

        "merchant_risk": features.get(
            "merchant_risk"
        ),

        "ip_risk_score": features.get(
            "ip_risk_score"
        )
    }
