import streamlit as st
import requests
import pandas as pd

from utils.api import BASE_URL
from utils.auth import get_headers

st.title("💳 Transaction Simulator")

user_id = st.number_input(
    "User ID",
    min_value=1,
    value=1
)

wallet_id = st.number_input(
    "Wallet ID",
    min_value=1,
    value=1
)

amount = st.number_input(
    "Amount",
    min_value=1.0,
    value=5000.0
)

if st.button("Process Transaction"):

    payload = {

        "user_id": int(user_id),

        "wallet_id": int(wallet_id),

        "amount": amount
    }

    response = requests.post(

        f"{BASE_URL}/wallet/transfer",

        json=payload,

        headers=get_headers()
    )

    if response.status_code == 200:

        result = response.json()["data"]

        st.success("Transaction Processed")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "ML Score",
                round(
                    result["ml_risk_score"],
                    4
                )
            )

        with col2:

            st.metric(
                "Final Score",
                round(
                    result["final_risk_score"],
                    4
                )
            )

        with col3:

            st.metric(
                "Decision",
                result["decision"]
            )

        st.subheader("Triggered Rules")

        for rule in result[
            "triggered_rules"
        ]:

            st.write(f"• {rule}")

        st.subheader(
            "Fraud Explanations"
        )

        for explanation in result[
            "human_explanations"
        ]:

            st.write(
                f"• {explanation}"
            )

        st.subheader(
            "Top Risk Factors"
        )

        shap_df = pd.DataFrame(

            result["top_risk_factors"]
        )

        st.dataframe(
            shap_df,
            use_container_width=True
        )

    else:

        st.error(response.text)
