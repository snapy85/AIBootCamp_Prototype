'''import os
from dotenv import load_dotenv
from openai import OpenAI
import tiktoken 

load_dotenv('.env')

# Pass the API Key to the OpenAI Client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

load_dotenv()  # loads .env into os.environ
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
'''


'''
# 1. Load exactly the file named ".env" in your working directory
load_dotenv('.env')

# 2. Read the key from the now-populated environment
api_key = os.getenv('OPENAI_API_KEY')

# 3. Pass it directly into the client
client = OpenAI(api_key=api_key)
'''

from dotenv import load_dotenv
import os
import streamlit as st
from openai import OpenAI

load_dotenv()  
st.set_page_config(page_title="AI Gov Assistant")
st.write("🔑 OPENAI key loaded:", bool(os.getenv("OPENAI_API_KEY")))

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
