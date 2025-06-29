# src/ingest.py

import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# 1. Read URLs (skipping comments)
with open("data/urls.txt") as f:
    urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]

# 2. Fetch pages
docs = []
for url in urls:
    docs.extend(WebBaseLoader(url).load())

# 3. Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
chunks = splitter.split_documents(docs)

# 4. Embed & persist to Chroma
embeddings = OpenAIEmbeddings()
vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="data/chroma_db"
)

# vectordb.persist()  <-- remove this line

print(f"Ingested {len(chunks)} chunks into data/chroma_db")
