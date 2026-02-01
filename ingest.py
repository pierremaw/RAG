import time
import uuid

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
from pinecone.exceptions import PineconeApiException

import config


def load_pdfs(directory: str):
    """Load all PDF files from a directory."""
    loader = PyPDFDirectoryLoader(directory)
    documents = loader.load()
    print(f"Loaded {len(documents)} pages from PDFs in '{directory}'")
    return documents


def chunk_documents(documents):
    """Split documents into chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")
    return chunks


def ensure_index_exists():
    """Create the Pinecone index if it doesn't exist."""
    pc = Pinecone(api_key=config.get_pinecone_key())
    existing = [idx.name for idx in pc.list_indexes()]
    if config.get_index_name() not in existing:
        print(f"Creating Pinecone index '{config.get_index_name()}'...")
        pc.create_index(
            name=config.get_index_name(),
            dimension=1024,  # multilingual-e5-large dimension
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        print("Index created.")
    else:
        print(f"Pinecone index '{config.get_index_name()}' already exists.")


def embed_texts(pc, texts):
    """Embed texts using Pinecone's inference API."""
    result = pc.inference.embed(
        model=config.EMBEDDING_MODEL,
        inputs=texts,
        parameters={"input_type": "passage"},
    )
    return [e.values for e in result.data]


def embed_and_store(chunks):
    """Embed chunks and upsert them into Pinecone."""
    pc = Pinecone(api_key=config.get_pinecone_key())
    ensure_index_exists()
    index = pc.Index(config.get_index_name())

    # Batch embed and upsert with rate limit handling
    batch_size = 50
    total_batches = (len(chunks) + batch_size - 1) // batch_size
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        texts = [chunk.page_content for chunk in batch]
        metadatas = [
            {**chunk.metadata, "text": chunk.page_content} for chunk in batch
        ]
        batch_num = i // batch_size + 1

        for attempt in range(5):
            try:
                vectors = embed_texts(pc, texts)
                break
            except PineconeApiException as e:
                if e.status == 429:
                    wait = 60 * (attempt + 1)
                    print(f"  Rate limited, waiting {wait}s...")
                    time.sleep(wait)
                else:
                    raise

        ids = [str(uuid.uuid4()) for _ in batch]
        upserts = [
            {"id": id_, "values": vec, "metadata": meta}
            for id_, vec, meta in zip(ids, vectors, metadatas)
        ]
        index.upsert(vectors=upserts)
        print(f"  Upserted batch {batch_num}/{total_batches} ({len(batch)} chunks)")

    print(f"Stored {len(chunks)} chunks in Pinecone.")


def ingest(directory: str = "docs"):
    """Full ingestion pipeline: load PDFs, chunk, embed, and store."""
    documents = load_pdfs(directory)
    if not documents:
        print("No PDF documents found. Add PDFs to the directory and try again.")
        return
    chunks = chunk_documents(documents)
    embed_and_store(chunks)
    print("Ingestion complete.")
