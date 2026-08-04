# ============================================================
# WALLET GUARD - DECISION ENGINE SERVICE
# ============================================================

import os

# ============================================================
# THRESHOLD PATH
# ============================================================

THRESHOLD_PATH = "models/threshold.txt"

# ============================================================
# LOAD THRESHOLD
# ============================================================

def load_threshold():

    if os.path.exists(THRESHOLD_PATH):

        with open(THRESHOLD_PATH, "r") as file:

            return float(file.read())

    # Default fallback

    return 0.75

# ============================================================
# APPLY RULE-BASED VALIDATION
# ============================================================

def apply_rules(features):

    triggered_rules = []

    rule_score = 0.0

    # --------------------------------------------------------
    # High Transaction Amount
    # --------------------------------------------------------

    amount = features.get("Amount", 0)
    
    if amount > 10000:
        triggered_rules.append("High transaction amount")
        rule_score += 0.10
    if amount > 25000:
        rule_score += 0.10
    if amount > 50000:
        rule_score += 0.15
    if amount > 100000:
        rule_score += 0.15
    # --------------------------------------------------------
    # Night Transaction
    # --------------------------------------------------------

    if features.get(
        "night_transaction",
        0
    ) == 1:

        triggered_rules.append(
            "Night-time transaction"
        )

        rule_score += 0.05

    # --------------------------------------------------------
    # New Device
    # --------------------------------------------------------

    if features.get(
        "device_new",
        0
    ) == 1:

        triggered_rules.append(
            "New device detected"
        )

        rule_score += 0.08

    # --------------------------------------------------------
    # Failed Login Attempts
    # --------------------------------------------------------

    if features.get(
        "failed_attempts",
        0
    ) >= 3:

        triggered_rules.append(
            "Multiple failed attempts"
        )

        rule_score += 0.10

    # --------------------------------------------------------
    # High Transaction Velocity
    # --------------------------------------------------------

    if features.get(
        "transaction_velocity",
        0
    ) > 15:

        triggered_rules.append(
            "High transaction velocity"
        )

        rule_score += 0.15

    # --------------------------------------------------------
    # High-Risk Merchant
    # --------------------------------------------------------

    if features.get(
        "merchant_risk",
        0
    ) > 0.8:

        triggered_rules.append(
            "High-risk merchant"
        )

        rule_score += 0.10

    # --------------------------------------------------------
    # Suspicious IP Risk
    # --------------------------------------------------------

    if features.get(
        "ip_risk_score",
        0
    ) > 0.8:

        triggered_rules.append(
            "Suspicious IP risk score"
        )

        rule_score += 0.10

    # --------------------------------------------------------
    # Geo-Distance Risk
    # --------------------------------------------------------

    if features.get(
        "geo_distance",
        0
    ) > 200:

        triggered_rules.append(
            "Abnormal geo-distance"
        )

        rule_score += 0.07

    # --------------------------------------------------------
    # Cap Rule Score
    # --------------------------------------------------------

    rule_score = min(
        rule_score,
        1.0
    )

    return {

        "rule_score": round(
            float(rule_score),
            4
        ),

        "triggered_rules": triggered_rules
    }

# ============================================================
# HYBRID RISK FUSION
# ============================================================

def combine_risk_scores(
    ml_risk_score,
    rule_score
):

    # --------------------------------------------------------
    # Hybrid Weighted Fusion
    # --------------------------------------------------------

    final_risk_score = (

    (0.70 * ml_risk_score)

    +

    (0.30 * rule_score)
)
    final_risk_score = min(
        final_risk_score,
        1.0
    )

    return round(
        float(final_risk_score),
        4
    )

# ============================================================
# 3-TIER DECISION ENGINE
# ============================================================

def make_decision(
    final_risk_score
):

    # --------------------------------------------------------
    # APPROVE
    # --------------------------------------------------------

    if final_risk_score < 0.40:

        return "APPROVE"

    # --------------------------------------------------------
    # REVIEW
    # --------------------------------------------------------

    elif final_risk_score < 0.70:

        return "REVIEW"

    # --------------------------------------------------------
    # REJECT
    # --------------------------------------------------------

    else:

        return "REJECT"

# ============================================================
# GENERATE DECISION RESPONSE
# ============================================================

def generate_decision_payload(
    ml_risk_score,
    features
):

    # --------------------------------------------------------
    # Apply Rules
    # --------------------------------------------------------

    rule_result = apply_rules(
        features
    )

    rule_score = rule_result[
        "rule_score"
    ]

    triggered_rules = rule_result[
        "triggered_rules"
    ]

    # --------------------------------------------------------
    # Hybrid Risk Fusion
    # --------------------------------------------------------

    final_risk_score = (
        combine_risk_scores(
            ml_risk_score,
            rule_score
        )
    )

    # --------------------------------------------------------
    # Final Decision
    # --------------------------------------------------------

    decision = make_decision(
        final_risk_score
    )

    return {

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

        "triggered_rules": triggered_rules,

        "threshold_used": load_threshold()
    }

# ============================================================
# AUDIT LOG FORMATTER
# ============================================================

def format_audit_log(
    transaction_id,
    payload
):

    return {

        "transaction_id": transaction_id,

        "decision": payload[
            "decision"
        ],

        "ml_risk_score": payload[
            "ml_risk_score"
        ],

        "rule_risk_score": payload[
            "rule_risk_score"
        ],

        "final_risk_score": payload[
            "final_risk_score"
        ],

        "triggered_rules": payload[
            "triggered_rules"
        ]
    }
