# RAG Assistant Demo

PDF question-answering system using Retrieval-Augmented Generation with a Streamlit web interface.

## Stack
- **Framework**: Python + LangChain
- **Vector DB**: Pinecone (cloud, serverless)
- **LLM**: Anthropic Claude (claude-sonnet-4-20250514)
- **Embeddings**: Pinecone Inference (multilingual-e5-large)
- **Frontend**: Streamlit
- **Document type**: PDF

## Architecture

```
PDF files → PyPDF loader → Text chunks → Pinecone Inference embeddings → Pinecone index
                                                                              ↓
User question → Pinecone Inference embed → Pinecone similarity search → Top-k chunks → Claude → Answer
```

## Project Structure

```
RAG Assistant Demo/
├── app.py              # Streamlit web interface
├── main.py             # CLI entry point
├── config.py           # Configuration (env vars, constants)
├── ingest.py           # PDF ingestion pipeline
├── query.py            # RAG query engine
├── requirements.txt    # Python dependencies
├── .env                # API keys (not committed)
├── .env.example        # API key template
├── design.md           # This file
└── docs/               # PDF files to ingest
```

## Usage

### Web App (Streamlit)
```bash
python -m streamlit run app.py
```
- Upload PDFs via the sidebar
- Click "Ingest Documents" to index them
- Ask questions in the chat interface

### CLI
```bash
# Ingest documents
python main.py ingest

# Ask a single question
python main.py query "What is this document about?"

# Interactive mode
python main.py query
```

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy .env.example to .env and fill in your API keys
cp .env.example .env

# 3. Place PDF files in the docs/ directory
```

## Configuration

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude (generation) |
| `PINECONE_API_KEY` | Pinecone API key (embeddings + vector storage) |
| `PINECONE_INDEX_NAME` | Pinecone index name (default: `rag-assistant`) |

Only two API providers are needed: Anthropic and Pinecone.
