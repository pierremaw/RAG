# RAG Assistant

**[Live Demo](https://pautybqphujebmetcxuihx.streamlit.app/)**

PDF question-answering system using Retrieval-Augmented Generation with a Streamlit web interface.

Upload PDFs, ingest them into a vector database, and ask questions answered by Claude using relevant context from your documents.

## Stack

- **LangChain** - orchestration framework
- **Pinecone** - vector database + embeddings (multilingual-e5-large)
- **Anthropic Claude** - LLM for answer generation
- **Streamlit** - web interface
- **PyPDF** - PDF parsing

## Architecture

```
PDF files → PyPDF loader → Text chunks → Pinecone Inference embeddings → Pinecone index
                                                                              ↓
User question → Pinecone Inference embed → Pinecone similarity search → Top-k chunks → Claude → Answer
```

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Copy .env.example to .env and add your API keys
cp .env.example .env
```

### Required API Keys

| Variable | Description | Get it from |
|---|---|---|
| `ANTHROPIC_API_KEY` | Claude (generation) | https://console.anthropic.com/settings/keys |
| `PINECONE_API_KEY` | Embeddings + vector storage | https://app.pinecone.io |
| `PINECONE_INDEX_NAME` | Your Pinecone index name | https://app.pinecone.io |

## Usage

### Web App
```bash
python -m streamlit run app.py
```
- Upload PDFs via the sidebar
- Click "Ingest Documents" to index them
- Ask questions in the chat interface

### CLI
```bash
# Ingest PDFs from docs/ directory
python main.py ingest

# Ask a question
python main.py query "What is this document about?"

# Interactive mode
python main.py query
```

## Live Demo

The app is deployed on Streamlit Community Cloud:

https://pautybqphujebmetcxuihx.streamlit.app/
