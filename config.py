import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Pinecone
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "rag-assistant")

# Chunking
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Models
EMBEDDING_MODEL = "multilingual-e5-large"
LLM_MODEL = "claude-sonnet-4-20250514"

# Retrieval
TOP_K = 4
