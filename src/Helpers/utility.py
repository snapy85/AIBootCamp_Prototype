# utility.py
import streamlit as st
import hmac

def check_password_multi():
    """Returns True if a correct username+password pair is entered."""
    def password_entered():
        users = st.secrets["users"]
        username = st.session_state["username"]
        password = st.session_state["password"]
        if username in users and hmac.compare_digest(password, users[username]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    # If already authenticated, return True
    if st.session_state.get("password_correct", False):
        return True

    # Show username & password input
    st.text_input("Username", key="username")
    st.text_input("Password", type="password", on_change=password_entered, key="password")
    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
        st.error("😕 Username or password incorrect")
    return False
