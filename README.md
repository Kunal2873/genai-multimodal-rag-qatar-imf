# Multi-Modal RAG Chatbot for Qatar IMF Report

This project implements a Retrieval-Augmented Generation (RAG) chatbot capable of answering questions from the IMF Article IV Consultation report for Qatar. It combines **PDF text extraction** and **table extraction**, enabling accurate responses for both narrative and numerical queries.

## Features
- Text ingestion using pdfplumber
- Table extraction using Camelot + Ghostscript
- Embeddings via Sentence Transformers
- FAISS vector store for similarity search
- LangChain retriever pipeline
- Streamlit-based UI
