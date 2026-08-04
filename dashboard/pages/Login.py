import streamlit as st
import requests

from utils.api import BASE_URL
from utils.auth import save_token

st.title("🔐 Authentication")

tab1, tab2 = st.tabs(["Login", "Register"])

# ============================================================
# LOGIN
# ============================================================

with tab1:

    with st.form("login_form"):

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        submit = st.form_submit_button(
            "Login"
        )

        if submit:

            response = requests.post(

                f"{BASE_URL}/auth/login",

                json={

                    "email": email,

                    "password": password
                }
            )

            if response.status_code == 200:

                token = response.json()[
                    "access_token"
                ]

                save_token(token, email)

                st.success(
                    "Login successful"
                )

            else:

                st.error(
                    "Invalid credentials"
                )

# ============================================================
# REGISTER
# ============================================================

with tab2:

    with st.form("register_form"):

        register_name = st.text_input(
    "Full Name"
)

        email = st.text_input(
            "Register Email"
        )

        password = st.text_input(

            "Register Password",

            type="password"
        )

        submit = st.form_submit_button(
            "Register"
        )

        if submit:

            response = requests.post(

                f"{BASE_URL}/auth/register",

                json={
                    "name": register_name,

                    "email": email,

                    "password": password
                }
            )

            if response.status_code == 200:

                st.success(
                    "Registration successful"
                )

            else:

                st.error(response.text)

