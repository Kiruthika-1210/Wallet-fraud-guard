# ============================================================
# WALLET GUARD - MAIN DASHBOARD
# ============================================================

import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(

    page_title="Wallet Guard",

    page_icon="🛡️",

    layout="wide"
)

# ============================================================
# SESSION STATE
# ============================================================

if "token" not in st.session_state:

    st.session_state.token = None

if "user_email" not in st.session_state:

    st.session_state.user_email = None

# ============================================================
# MAIN PAGE
# ============================================================

st.title("🛡️ Wallet Guard")

st.markdown(
    """
    ### AI-Powered Hybrid Fraud Detection Platform
    
    Use the sidebar to navigate between:
    
    - Authentication
    - Transaction Simulation
    - Fraud Analytics
    - Audit Logs
    """
)

# ============================================================
# SIDEBAR STATUS
# ============================================================

with st.sidebar:

    st.header("Wallet Guard")

    if st.session_state.token:

        st.success("Authenticated")

        st.write(
            f"User: {st.session_state.user_email}"
        )

    else:

        st.warning("Not Logged In")
