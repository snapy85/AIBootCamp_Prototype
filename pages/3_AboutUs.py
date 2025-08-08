import streamlit as st

st.title("MDWHire Assistant — About Us")
# ---------------------------------------------------------
# Security: check login (app-level control, not part of RAG/LLM)
# ---------------------------------------------------------
if not st.session_state.get("password_correct"):
    st.error("You must log in first.")
    st.stop()
    
st.markdown("""
**Subject Title**
[1233624B] AI-Powered Assistant for MOM Helper Information

**Project Summary**

The MDWHire Assistant is a prototype AI-powered web assistant, developed as part of the [AI Bootcamp/Capstone], to help streamline access to government policy information—showcasing how Retrieval-Augmented Generation and modern LLMs can improve clarity and efficiency.

---

**1. Problem Statement**

Working adults in Singapore, especially new parents, struggle to quickly find clear, up-to-date information about hiring a Migrant Domestic Worker (MDW). The current MOM website requires users to search across multiple pages and filter information themselves, leading to confusion and inefficiency.

---

**2. Proposed Solution**

A single-user, password-protected web prototype, the MDWHire Assistant enables the MOM Advisor Agent to securely log in, upload a MOM policy document, and interact with an AI-powered Q&A interface. This interface only answers based on the uploaded content, ensuring answers are always sourced from the official document (Retrieval-Augmented Generation).

---

**3. Target User (MVP)**

- MOM Advisor Agent (single user for demo)
- Future expansion: general employers/families in Singapore hiring an MDW

---

**4. Key Features & MVP Scope**

- Secure login (password-protected)
- Upload and manage a MOM policy document (PDF or HTML)
- Automated chunking and text cleaning
- All Q&A answers use only the uploaded document
- Streamlit-based, multi-page prototype for demo/educational use

---

**5. Project Objectives**

- Demonstrate the feasibility of using RAG and LLMs for policy discovery in a government context.
- Lay the groundwork for a scalable, user-focused solution that could expand to multiple users, automatic data refresh, and analytics.

---

**6. Team/Group**

- Name: Ong Wan Chin
- Group ID: 1233624B
- GovTech AI Bootcamp Capstone Project

---

*For methodology, architecture, and technical approach, see the Methodology page.*
""")
