import os
from dotenv import load_dotenv

load_dotenv()


def _get_secret(key, default=None):
    """Get a secret from session state, Streamlit secrets, or environment variables."""
    try:
        import streamlit as st
        # User-provided key in session state takes priority
        if key in st.session_state and st.session_state[key]:
            return st.session_state[key]
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key, default)


def get_anthropic_key():
    return _get_secret("ANTHROPIC_API_KEY")


def get_pinecone_key():
    return _get_secret("PINECONE_API_KEY")


def get_index_name():
    return _get_secret("PINECONE_INDEX_NAME", "rag-assistant")

# Chunking
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Models
EMBEDDING_MODEL = "multilingual-e5-large"
LLM_MODEL = "claude-sonnet-4-20250514"

# Retrieval
TOP_K = 4
