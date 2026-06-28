# src/llm/llm_client.py

import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

def load_llm():
    """Load the Groq LLM client."""
    
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.7
    )
    return llm