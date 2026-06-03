# ============================================================
# WALLET GUARD - SHAP EXPLAINER SERVICE
# ============================================================

import shap
import pandas as pd
import numpy as np

from api.services import fraud_model

# ============================================================
# GLOBAL SHAP EXPLAINER
# ============================================================

explainer = None

# ============================================================
# INITIALIZE SHAP EXPLAINER
# ============================================================

def initialize_explainer():

    global explainer

    if fraud_model.model is None:

        raise Exception(
            "Fraud model not initialized."
        )

    explainer = shap.TreeExplainer(
        fraud_model.model
    )

    print("\nSHAP Explainer Initialized")

# ============================================================
# GENERATE SHAP VALUES
# ============================================================

def generate_shap_values(
    scaled_df
):

    if explainer is None:

        raise Exception(
            "SHAP explainer not initialized."
        )

    shap_values = explainer.shap_values(
        scaled_df
    )

    return shap_values

# ============================================================
# GET TOP RISK FACTORS
# ============================================================

def get_top_risk_factors(
    scaled_df,
    top_n=5
):

    # --------------------------------------------------------
    # Generate SHAP Values
    # --------------------------------------------------------

    shap_values = generate_shap_values(
        scaled_df
    )

    transaction_shap_values = (
        shap_values[0]
    )

    # --------------------------------------------------------
    # Create Feature Contribution DataFrame
    # --------------------------------------------------------

    feature_contributions = pd.DataFrame({

        "Feature": scaled_df.columns,

        "SHAP_Value": transaction_shap_values
    })

    # --------------------------------------------------------
    # Calculate Impact
    # --------------------------------------------------------

    feature_contributions["Impact"] = (
        np.abs(
            feature_contributions[
                "SHAP_Value"
            ]
        )
    )

    # --------------------------------------------------------
    # Keep Positive Fraud Contributors
    # --------------------------------------------------------

    feature_contributions = (

        feature_contributions[
            feature_contributions[
                "SHAP_Value"
            ] > 0
        ]

        .sort_values(
            by="Impact",
            ascending=False
        )

        .head(top_n)
    )

    return feature_contributions

# ============================================================
# GENERATE HUMAN EXPLANATIONS
# ============================================================

def generate_human_explanations(
    top_risk_factors
):

    explanations = []

    for _, row in (
        top_risk_factors.iterrows()
    ):

        feature = row["Feature"]

        impact = row["SHAP_Value"]

        explanation = (
            f"{feature} increased fraud "
            f"risk by {abs(impact):.4f}"
        )

        explanations.append(
            explanation
        )

    return explanations

# ============================================================
# GENERATE EXPLANATION PAYLOAD
# ============================================================

def generate_explanation_payload(
    scaled_df
):

    # --------------------------------------------------------
    # Get Top Risk Factors
    # --------------------------------------------------------

    top_risk_factors = (
        get_top_risk_factors(
            scaled_df
        )
    )

    # --------------------------------------------------------
    # Human Explanations
    # --------------------------------------------------------

    human_explanations = (
        generate_human_explanations(
            top_risk_factors
        )
    )

    # --------------------------------------------------------
    # Backend Payload
    # --------------------------------------------------------

    payload = {

        "top_risk_factors": [

            {
                "feature": row["Feature"],

                "impact_score": round(
                    float(row["SHAP_Value"]),
                    4
                )
            }

            for _, row in (
                top_risk_factors.iterrows()
            )
        ],

        "human_explanations": (
            human_explanations
        )
    }

    return payload

# ============================================================
# FULL SHAP ANALYSIS
# ============================================================

def analyze_transaction(
    features
):

    # --------------------------------------------------------
    # Prepare Features
    # --------------------------------------------------------

    feature_df = (
        fraud_model.prepare_features(
            features
        )
    )

    # --------------------------------------------------------
    # Scale Features
    # --------------------------------------------------------

    scaled_df = (
        fraud_model.scale_features(
            feature_df
        )
    )

    # --------------------------------------------------------
    # Generate Payload
    # --------------------------------------------------------

    payload = (
        generate_explanation_payload(
            scaled_df
        )
    )

    return payload

