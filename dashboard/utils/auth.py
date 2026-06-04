# ============================================================
# AUTH UTILITIES
# ============================================================

import streamlit as st

# ============================================================
# STORE TOKEN
# ============================================================

def save_token(token, email):

    st.session_state.token = token

    st.session_state.user_email = email

# ============================================================
# LOGOUT
# ============================================================

def logout():

    st.session_state.token = None

    st.session_state.user_email = None

# ============================================================
# AUTH HEADERS
# ============================================================

def get_headers():

    if st.session_state.get("token"):

        return {

            "Authorization": (
                f"Bearer {st.session_state.token}"
            )
        }

    return {}
