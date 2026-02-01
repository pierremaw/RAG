import os
import streamlit as st
from ingest import ingest
from query import ask

st.set_page_config(page_title="RAG Assistant", page_icon="📚", layout="wide")

# --- Sidebar: PDF Upload & Ingestion ---
with st.sidebar:
    st.header("📄 Document Ingestion")

    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        os.makedirs("docs", exist_ok=True)
        for uploaded_file in uploaded_files:
            path = os.path.join("docs", uploaded_file.name)
            with open(path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        st.success(f"Saved {len(uploaded_files)} file(s) to docs/")

    if st.button("Ingest Documents", use_container_width=True):
        with st.spinner("Ingesting PDFs..."):
            try:
                ingest()
                st.success("Ingestion complete!")
            except Exception as e:
                st.error(f"Ingestion failed: {e}")

    st.divider()
    st.caption("Upload PDFs and click Ingest to index them. Then ask questions in the main panel.")

# --- Main Area: Chat Q&A ---
st.title("📚 RAG Assistant")
st.caption("Ask questions about your ingested documents")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask a question about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer, sources = ask(prompt)

                st.markdown(answer)

                if sources:
                    seen = set()
                    source_lines = []
                    for doc in sources:
                        source = doc.metadata.get("source", "unknown")
                        page = doc.metadata.get("page", "?")
                        key = f"{source}:p{page}"
                        if key not in seen:
                            seen.add(key)
                            source_lines.append(f"- {source} (page {page})")
                    if source_lines:
                        st.divider()
                        st.caption("**Sources:**\n" + "\n".join(source_lines))

                # Build full response for history
                full_response = answer
                if sources:
                    full_response += "\n\n---\n**Sources:** " + ", ".join(
                        f"{doc.metadata.get('source', '?')} p{doc.metadata.get('page', '?')}"
                        for doc in sources
                    )

                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )
            except Exception as e:
                error_msg = f"Error: {e}"
                st.error(error_msg)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )
