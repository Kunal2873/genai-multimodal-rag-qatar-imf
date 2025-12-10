# Multi-Modal RAG Chatbot for Qatar IMF Report

## 🎯 Objective

This project implements a Retrieval-Augmented Generation (RAG) system over the IMF Article IV Consultation report for Qatar.  
The system can:

- Ingest **text sections** of the PDF  
- Ingest **tabular data** (government finance, monetary survey, etc.)  
- Answer questions **grounded strictly in the document**  
- Provide **page-level citations**  
- Generate a **brief macroeconomic summary** from the report (bonus feature)

---

## 🧱 Architecture Overview

**Pipeline:**

1. **Ingestion**
   - `pdf_loader.py`  
     - Uses `pdfplumber` to extract text page-by-page  
     - Cleans and chunks text (with page numbers + modality `"text"`)
   - `table_extractor.py`  
     - Uses `camelot-py` + Ghostscript to extract tables  
     - Converts tables to text and tags them with page and modality `"table"`

2. **Embeddings**
   - `Embedder` (in `embeddings/embedder.py`)  
   - Uses a Sentence-Transformers model to convert each chunk (text + table) into a dense vector

3. **Vector Store**
   - `FAISSStore` (in `vectorstore/faiss_store.py`)  
   - Stores embeddings in a FAISS index and keeps original chunk metadata

4. **Retriever**
   - `Retriever` (in `retriever/retriever.py`)  
   - Embeds the user query  
   - Performs similarity search in FAISS (top_k=10)  
   - Returns a combined context string + unique page citations

5. **LLM Answer Generator**
   - `AnswerLLM` (in `generator/answer_llm.py`)  
   - Uses a local `mistral` model via Ollama HTTP API  
   - `answer()` → question answering strictly from context  
   - `summarize()` → generates a concise economic summary

6. **User Interface**
   - `app.py` (in `ui/`)  
   - Streamlit app with:
     - Question input
     - Answer with page citations
     - Expandable “Retrieved Context Chunks”
     - **Bonus:** “Generate Summary” button

---

## 🗂 Project Structure

```text
.
├── data/
│   └── qatar_imf.pdf
├── src/
│   ├── ingestion/
│   │   ├── pdf_loader.py
│   │   └── table_extractor.py
│   ├── embeddings/
│   │   └── embedder.py
│   ├── vectorstore/
│   │   └── faiss_store.py
│   ├── retriever/
│   │   └── retriever.py
│   ├── generator/
│   │   └── answer_llm.py
│   └── ui/
│       └── app.py
├── requirements.txt
├── README.md
└── .gitignore
