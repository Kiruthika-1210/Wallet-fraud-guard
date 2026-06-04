import streamlit as st
import requests
import pandas as pd
import json

from utils.api import BASE_URL
from utils.auth import get_headers

st.title("📁 Fraud Audit Logs")

response = requests.get(

    f"{BASE_URL}/fraud/logs",

    headers=get_headers()
)

if response.status_code == 200:

    logs = response.json()

    logs_df = pd.DataFrame(logs)

    for column in logs_df.columns:
        logs_df[column] = logs_df[column].apply(
            lambda x: json.dumps(x, indent=2)
            if isinstance(x, (dict, list))
            else str(x)
        )
        
    st.dataframe(
        logs_df,
        width="stretch"
    )

else:

    st.error(response.text)
