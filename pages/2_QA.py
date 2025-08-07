# --- Must come before chromadb import ---
import sys
try:
    import pysqlite3
    sys.modules["sqlite3"] = pysqlite3
except ImportError:
    pass  # fallback to system sqlite3 if not found

import streamlit as st
import openai
import chromadb
from chromadb.utils import embedding_functions
import tiktoken
import hashlib
import time
import sys
import os
import re

# Add src folder to sys path to import helpers
sys.path.append(os.path.abspath("src"))
from Helpers.filters import is_question_relevant, is_question_safe
from Helpers.prompt_builder import build_prompt
#from Helpers.prompt_builder import build_prompt_from_context, build_fallback_prompt

# ------------------------------
# 🔧 Constants
# ------------------------------
MODEL_COMPLETION = "gpt-4o-mini"
MODEL_EMBEDDING = "text-embedding-3-small"
CHROMA_PATH = ".chroma"
CHUNK_COLLECTION_NAME = "doc_chunks"

QUICK_QUESTIONS = [
    "Show me how to apply for a domestic helper in Singapore.",
    "Provide the link to hire a helper for elderly care at home.",
    "Where can I apply for a nanny or confinement helper online?"
]

# ------------------------------
# 🧠 Utility Functions
# ------------------------------
def count_tokens(text, model=MODEL_COMPLETION):
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))

def get_completion(prompt, model=MODEL_COMPLETION):
    messages = [{"role": "user", "content": prompt}]
    response = st.session_state["openai_client"].chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content

def compute_chunks_hash(chunks):
    text_data = "".join([chunk["text"] for chunk in chunks])
    return hashlib.md5(text_data.encode("utf-8")).hexdigest()

# ------------------------------
# 📄 Document Embedding Processing
# ------------------------------
def process_uploaded_documents():
    all_chunks = []
    for doc in st.session_state["uploaded_docs"]:
        all_chunks.extend(doc["chunks"])
    st.session_state["all_chunks"] = all_chunks

    current_hash = compute_chunks_hash(all_chunks)
    previous_hash = st.session_state.get("doc_chunks_hash")

    if previous_hash == current_hash and st.session_state.get("embedding_built"):
        return

    with st.spinner("🔄 Building embeddings..."):
        chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
        embedder = embedding_functions.OpenAIEmbeddingFunction(
            api_key=st.session_state["openai_api_key"],
            model_name=MODEL_EMBEDDING
        )
        collection = chroma_client.get_or_create_collection(
            name=CHUNK_COLLECTION_NAME,
            embedding_function=embedder
        )
        texts = [c["text"] for c in all_chunks]
        metadatas = [{"chunk_id": c["chunk_id"]} for c in all_chunks]
        ids = [c["chunk_id"] for c in all_chunks]

        if len(collection.get(ids=ids)["ids"]) > 0:
            collection.delete(ids=ids)

        collection.add(documents=texts, metadatas=metadatas, ids=ids)
        st.session_state["collection"] = collection
        st.session_state["embedding_built"] = True
        st.session_state["doc_chunks_hash"] = current_hash

# ------------------------------
# 🔑 Handle Question
# ------------------------------
def handle_question(question):
    try:
        collection = st.session_state["collection"]
        all_chunks = st.session_state["all_chunks"]

        if (
            "question_relevance" not in st.session_state or
            st.session_state.get("last_checked_question") != question
        ):
            st.session_state["question_relevance"] = is_question_relevant(question)
            st.session_state["question_safe"] = is_question_safe(question)
            st.session_state["last_checked_question"] = question

        if not st.session_state["question_safe"]:
            st.error("❌ Question is unsafe or inappropriate.")
            return

        if not st.session_state["question_relevance"]:
            st.warning("⚠️ Your question is not related to MDW topics.")
            return

        with st.spinner("🔍 Searching uploaded documents..."):
            results = collection.query(query_texts=[question], n_results=10)
            retrieved_chunks = results["documents"][0] if results["documents"] else []
            context = "\n\n".join(retrieved_chunks).strip()
            token_count = count_tokens(context)

        urls_found = re.findall(r"https?://www\\.mom\\.gov\\.sg[\\w\\-\\./\\?#%&=]*", context)
        prompt = build_prompt(question, context if retrieved_chunks else None)
        answer = get_completion(prompt)

        st.session_state["last_answer"] = (question, answer, urls_found, token_count, retrieved_chunks)

    except Exception as e:
        st.error(f"⚠️ Error during question processing: {e}")

# ------------------------------
# 🚀 Start App
# ------------------------------
st.title("MDWcare Assistant — Q&A")
st.caption("Ask about Singapore MDW policies using uploaded documents with GenAI fallback.")

if not st.session_state.get("password_correct"):
    st.error("You must log in first.")
    st.stop()

if "openai_client" not in st.session_state:
    with st.spinner("🔐 Waiting for OpenAI API key..."):
        try:
            max_wait, interval, waited = 30, 0.2, 0
            while waited < max_wait:
                api_key = st.session_state.get("openai_api_key", "").strip()
                if api_key:
                    st.session_state["openai_client"] = openai.OpenAI(api_key=api_key)
                    break
                time.sleep(interval)
                waited += interval
            if "openai_client" not in st.session_state:
                st.warning("OpenAI API key missing. Please log in again.")
                st.stop()
        except Exception as e:
            st.error(f"OpenAI setup failed: {e}")
            st.stop()

if not st.session_state.get("uploaded_docs"):
    st.error("Please upload at least one document first.")
    st.stop()

try:
    process_uploaded_documents()
    st.success("✅ Assistant is ready — ask a question.")
except Exception as e:
    st.error(f"Failed to process uploaded documents: {e}")
    st.stop()

# ------------------------------
# 💡 Quick-start Buttons
# ------------------------------
st.markdown("#### 💡 Quick-start question:")
st.markdown("""
<style>
div[data-testid="stButton"] > button {
    width: 100%;
    height: 100px;
    white-space: normal;
    font-size: 0.88rem;
    line-height: 1.4;
    border-radius: 10px;
    border: 1px solid #ddd;
    padding: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

cols = st.columns(3)
for i, q in enumerate(QUICK_QUESTIONS):
    with cols[i % 3]:
        if st.button(f"🔎 {q}", key=f"quickbtn_{i}"):
            st.session_state["user_question"] = q
            
# ------------------------------
# 📝 Ask Your Question
# ------------------------------
submitted = False
with st.form("qa_form"):
    st.markdown("### 🔊 Ask Your Question")
    try:
        default_q = st.session_state.get("user_question")
        question = st.text_input("What would you like to ask?", value=str(default_q or ""), key="question_input")
        submitted = st.form_submit_button("🔍 Get Answer")
    except Exception:
        question = ""

if submitted and question.strip():
    st.session_state["user_question"] = question
    with st.spinner("🤖 Generating answer..."):
        handle_question(question)

# ------------------------------
# 🧠 Show Answer
# ------------------------------
last = st.session_state.get("last_answer")
if last and isinstance(last, tuple) and len(last) == 5:
    try:
        question, answer, urls, token_count, retrieved_chunks = last
        st.markdown(f"### 🖊️ Question\n{question}")
        st.markdown("### ✅ Answer")
        st.markdown(answer)
        st.caption(f"📎 Used {len(retrieved_chunks)} chunks • Approx. {token_count} tokens")

        if urls:
            st.markdown("#### 🔗 MOM Links Found in Document Context")
            for i, u in enumerate(sorted(set(urls))):
                st.markdown(f"{i+1}. {u}")

        with st.expander("📖 Sample Document Snippets", expanded=False):
            for i, chunk in enumerate(retrieved_chunks[:3]):
                st.markdown(f"**Chunk {i+1}**")
                st.code(chunk[:500])
    except Exception:
        pass
else:
    st.info("ℹ️ No question has been asked yet.")

# ------------------------------
# 📊 Upload Info + Disclaimer
# ------------------------------
with st.expander("ℹ️ Upload Details", expanded=False):
    try:
        st.metric("📃 Total Document Chunks", len(st.session_state["all_chunks"]))
        st.markdown("### 📃 All Uploaded Chunks")
        for chunk in st.session_state["all_chunks"]:
            st.markdown(f"**{chunk['source']}** — `{chunk['chunk_id']}`")
            st.code(chunk["text"][:1000] + ("..." if len(chunk["text"]) > 1000 else ""))
    except Exception:
        st.warning("⚠️ Unable to show chunk details.")

with st.expander("IMPORTANT NOTICE", expanded=False):
    st.markdown("""
**This web application is a prototype developed for _educational purposes only_.**  
The information provided here is **NOT intended for real-world usage** and should not be relied upon for making any decisions.

Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.

Always consult with qualified professionals for accurate and personalized advice.
""")
