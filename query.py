from langchain_anthropic import ChatAnthropic
from langchain_core.documents import Document
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_core.retrievers import BaseRetriever
from pinecone import Pinecone

import config

PROMPT_TEMPLATE = """Use the following context to answer the question. If you cannot
answer the question based on the context, say so clearly. Do not make up information.

Context:
{context}

Question: {question}

Answer:"""


class PineconeRetriever(BaseRetriever):
    """Custom retriever that queries Pinecone using Pinecone inference embeddings."""

    index_name: str
    top_k: int = 4

    def _get_relevant_documents(self, query: str):
        pc = Pinecone(api_key=config.get_pinecone_key())
        index = pc.Index(self.index_name)

        # Embed the query using Pinecone inference
        result = pc.inference.embed(
            model=config.EMBEDDING_MODEL,
            inputs=[query],
            parameters={"input_type": "query"},
        )
        query_vector = result.data[0].values

        results = index.query(
            vector=query_vector,
            top_k=self.top_k,
            include_metadata=True,
        )

        docs = []
        for match in results.matches:
            metadata = match.metadata or {}
            text = metadata.pop("text", "")
            docs.append(Document(page_content=text, metadata=metadata))
        return docs


def build_chain():
    """Build the RetrievalQA chain with Pinecone retriever and Claude LLM."""
    retriever = PineconeRetriever(
        index_name=config.get_index_name(),
        top_k=config.TOP_K,
    )

    llm = ChatAnthropic(
        model=config.LLM_MODEL,
        anthropic_api_key=config.get_anthropic_key(),
    )

    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"],
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )

    return chain


def ask(question: str):
    """Ask a question and return the answer with source documents."""
    chain = build_chain()
    result = chain.invoke({"query": question})

    answer = result["result"]
    sources = result.get("source_documents", [])

    return answer, sources
