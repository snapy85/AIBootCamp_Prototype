# src/main.py

import os
from dotenv import load_dotenv

import streamlit as st
from openai import OpenAI

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI

# ─────────────────────────────────────────────────────────────────────────────
# 1. Load secrets & configure Streamlit
# ─────────────────────────────────────────────────────────────────────────────
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY", "")
if not api_key:
    st.error("🔑 OPENAI_API_KEY not set. Please add it to your .env file.")
    st.stop()

st.set_page_config(page_title="MDWcare AI Assistant", layout="wide")
st.title("MDWcare AI Assistant")

client = OpenAI(api_key=api_key)

# ─────────────────────────────────────────────────────────────────────────────
# 2. Load the persisted vector store
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading vector store…")
def load_vectordb(path: str):
    return Chroma(
        persist_directory=path,
        embedding_function=OpenAIEmbeddings()
    )

vectordb = load_vectordb("data/chroma_db")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Build the retriever (cached)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_retriever(db):
    llm = ChatOpenAI(temperature=0)
    return MultiQueryRetriever.from_llm(
        retriever=db.as_retriever(), llm=llm
    )

retriever = get_retriever(vectordb)

# ─────────────────────────────────────────────────────────────────────────────
# 4. Streamlit query UI
# ─────────────────────────────────────────────────────────────────────────────
st.header("Ask about MDW Work-Permit Policy")
query = st.text_input("Enter your question here")
if st.button("Search") and query:
    with st.spinner("Retrieving answers…"):
        results = retriever.get_relevant_documents(query)
    if results:
        for i, doc in enumerate(results, start=1):
            st.subheader(f"Result {i}")
            st.write(doc.page_content)
    else:
        st.warning("No relevant information found.")
