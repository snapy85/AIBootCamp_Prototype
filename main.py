import streamlit as st
import hmac
import openai
import os

st.set_page_config(page_title="MDWcare Login", page_icon="🧾", layout="centered")
st.title("MDWcare Assistant")

# -----------------------------------
# 🔐 Login Authentication
# -----------------------------------
def check_password_form():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Login")

            if login_btn:
                try:
                    users = st.secrets["users"]
                except KeyError:
                    st.error("Internal error: No `[users]` section found in secrets.toml.")
                    return False

                if username in users and hmac.compare_digest(password, users[username]):
                    st.session_state["password_correct"] = True
                    st.session_state["username"] = username

                    # Load OpenAI API key after successful login
                    if load_openai_api_key():
                        st.success("✅ Login successful. Redirecting...")
                        st.switch_page("pages/1_Upload.py")
                    else:
                        st.error("Login successful, but API key missing.")
                else:
                    st.session_state["password_correct"] = False
                    st.error("❌ Invalid username or password. Please try again.")
        return False
    return True

# -----------------------------------
# 🔑 Load OpenAI API Key into Session
# -----------------------------------
def load_openai_api_key():
    api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", "")).strip()
    if api_key:
        st.session_state["openai_api_key"] = api_key

        # ✅ DEBUGGING ONLY — Your custom debug line
        st.write("All secrets loaded:", dict(st.secrets))

        # ✅ Additional debug info (safe)
        st.write("🔍 DEBUG: API key loaded:", bool(api_key))  # Do not print the key itself

        return True
    return False

# -----------------------------------
# 🙋 Greeting + Instructions (after login)
# -----------------------------------
def show_greeting_and_instruction():
    st.success(f"👋 Welcome, **{st.session_state['username']}**!")
    st.markdown("**Welcome to MDWcare Assistant. Follow the steps below to get started:**")

    st.info(
        """
        **How to use this app:**

        1. **Upload**  
           Upload MOM policy documents or related PDFs in the next step.

        2. **Q&A**  
           Ask questions about Singapore's MDW process — answers come from your uploaded documents or OpenAI.

        3. **About Us**  
           Learn who built this assistant and what challenges we're solving.

        4. **Methodology**  
           Explore our design and how RAG (Retrieval-Augmented Generation) powers the answers.
        """,
        icon="ℹ️"
    )

# -----------------------------------
# 🧠 Main App Flow
# -----------------------------------
if not check_password_form():
    pass  # login form was shown or failed
else:
    show_greeting_and_instruction()

# -----------------------------------
# ⚠️ Always-On Disclaimer
# -----------------------------------
with st.expander("IMPORTANT NOTICE", expanded=True):
    st.markdown("""
**This web application is a prototype developed for _educational purposes only_.**  
The information provided here is **NOT intended for real-world usage** and should not be relied upon for making any decisions.

Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.

Always consult with qualified professionals for accurate and personalized advice.
""")
