import os
from dotenv import load_dotenv

load_dotenv()


def _get_secret(key, default=None):
    """Get a secret from Streamlit secrets or environment variables."""
    try:
        import streamlit as st
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key, default)


# API Keys
ANTHROPIC_API_KEY = _get_secret("ANTHROPIC_API_KEY")
PINECONE_API_KEY = _get_secret("PINECONE_API_KEY")

# Pinecone
PINECONE_INDEX_NAME = _get_secret("PINECONE_INDEX_NAME", "rag-assistant")

# Chunking
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Models
EMBEDDING_MODEL = "multilingual-e5-large"
LLM_MODEL = "claude-sonnet-4-20250514"

# Retrieval
TOP_K = 4
