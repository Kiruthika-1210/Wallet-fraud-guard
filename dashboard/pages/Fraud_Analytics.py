import streamlit as st
import requests

from utils.api import BASE_URL
from utils.auth import get_headers

st.title("📊 Fraud Analytics")

response = requests.get(
    f"{BASE_URL}/fraud/analytics",
    headers=get_headers()
)

if response.status_code == 200:

    response_data = response.json()

    analytics = response_data["analytics"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Transactions",
            analytics["total_transactions"]
        )

    with col2:
        st.metric(
            "Rejected Transactions",
            analytics["rejected_transactions"]
        )

    with col3:
        st.metric(
            "Fraud Rate",
            f"{analytics['fraud_rate_percentage']}%"
        )

    st.divider()

    col4, col5 = st.columns(2)

    with col4:
        st.metric(
            "Approved",
            analytics["approved_transactions"]
        )

    with col5:
        st.metric(
            "Review",
            analytics["review_transactions"]
        )

else:

    st.error(response.text)