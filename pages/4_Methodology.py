import streamlit as st

st.title("MDWcare Assistant — Methodology")
# ---------------------------------------------------------
# Security: check login (app-level control, not part of RAG/LLM)
# ---------------------------------------------------------
if not st.session_state.get("password_correct"):
    st.error("You must log in first.")
    st.stop()

st.markdown("""
**Industry-Standard Development Methodologies**

---

**Agile Development:**  
The project is managed using agile sprints (Sprint 0: setup and ingestion; Sprint 1: feature build; Sprint 2: testing and submission). Tasks are broken down into short, manageable iterations, allowing for incremental progress, regular feedback, and quick adaptation to any changes or lessons learned.

---

**User-Centric Design:**  
All requirements, UI/UX flows, and acceptance criteria are designed from the perspective of the end user (employer or parent). Features such as simple login, document upload, and intuitive Q&A interface are prioritized to maximize usability and demonstrate best practices in user-focused product development.

---

**Lifecycle Structure:**  
The project lifecycle covers planning (problem definition, architecture), requirements gathering (proposal/user stories), iterative development (agile sprints), testing (end-to-end and user acceptance), and deployment (Streamlit prototype ready for demo/review).

---

**Best Practices in RAG Prototyping:**  
Follows best practices for Retrieval-Augmented Generation: after document upload, content is chunked and embedded into ChromaDB, and all Q&A relies strictly on the ingested content to ensure explainability and traceability.

---

**Security and Compliance:**  
No user registration or sensitive data is processed; all authentication and secrets are hardcoded for demo purposes. If deployed for external review (e.g., Streamlit Cloud), password protection is enabled to ensure secure demo access.

---

**MVP Focus:**  
Single-user, static files, no dynamic web crawling, no multi-user features. All workflows, design, and testing are explicitly mapped to agile and user-centric principles.

---

**MVP User Stories**

- As an employer or parent in Singapore, I want to securely log in to the assistant, so that I can access and use official MOM policy documents for hiring a Migrant Domestic Worker.
- As an employer, I want to upload and manage a single MOM policy document, so that I can retrieve accurate, up-to-date answers without searching across multiple government web pages.
- As an employer, I want to ask questions in a simple chat interface, so that I can quickly clarify the MDW hiring process, policies, and requirements.

---

**System Architecture**

The prototype consists of a modular Streamlit frontend, document upload/ingest logic, a chunker/cleaner, vector embedding with ChromaDB, and an OpenAI-powered RAG backend.  
All passwords/secrets are handled in `secrets.toml`, and the session state manages all active user and document info.
```
+---------------------+ +-------------------+ +----------------+ +---------------+
| Streamlit Frontend | ---> | Document Processor| ---> | Vector Store | ---> | LLM Q&A |
|     (UI & Auth)      | |      (Chunk/Clean)      | |   (ChromaDB)     | |  (OpenAI GPT) |
+---------------------+ +-------------------+ +----------------+ +---------------+
```
            
""")
