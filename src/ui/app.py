import sys
import os

# ensure root directory is in python path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)



import streamlit as st
from src.ingestion.pdf_loader import load_pdf_chunks
from src.embeddings.embedder import Embedder
from src.vectorstore.faiss_store import FAISSStore
from src.retriever.retriever import Retriever
from src.generator.answer_llm import AnswerLLM

st.set_page_config(page_title="Qatar IMF RAG System")

@st.cache_resource(show_spinner="Initializing system... This may take a few minutes the first time.")
def init_system():
    import os
    from src.ingestion.table_extractor import extract_tables

    # Ensures the  Ghostscript visibility for Camelot
    os.environ["PATH"] += os.pathsep + r"C:\Program Files\gs\gs10.06.0\bin"
    os.environ["PATH"] += os.pathsep + r"C:\Program Files\gs\gs10.06.0\lib"

    # Load text chunks
    text_chunks = load_pdf_chunks("data/qatar_imf.pdf")

    # Load table chunks (this is slow takes some time usually)
    table_chunks = extract_tables("data/qatar_imf.pdf")

    # Combine multimodal chunks
    chunks = text_chunks + table_chunks

    # Embed once and cache
    embedder = Embedder()
    vectors = embedder.encode([c["content"] for c in chunks])

    # Store embeddings in FAISS DB once
    store = FAISSStore()
    store.add(vectors, chunks)

    # Build retriever + llm wrapper once
    retriever = Retriever(store)
    llm = AnswerLLM(model_name="mistral")

    return retriever, llm



st.title("Multi-Modal RAG Chatbot for Qatar IMF Report")
st.write("Ask questions based on the IMF Article IV Consultation document.")

retriever, llm = init_system()

query = st.text_input("Enter your question:")

if query:
    context, citations = retriever.fetch_context(query)
    answer = llm.answer(query, context, citations)

    st.subheader("Answer")
    st.write(answer)

    with st.expander("Retrieved Context Chunks"):
        st.write(context)

if st.button("Generate Summary"):
    st.info("Generating summary from retrieved context...")
    context, citations = retriever.fetch_context("Qatar economic overview")
    summary = llm.summarize(context, citations)
    st.subheader("Summary")
    st.write(summary)



