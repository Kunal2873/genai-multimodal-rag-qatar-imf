from src.embeddings.embedder import Embedder
from src.vectorstore.faiss_store import FAISSStore

class Retriever:
    def __init__(self, store: FAISSStore):
        self.embedder = Embedder()
        self.store = store

    def fetch_context(self, query, top_k=10):
        expanded = query + " Pillar Two OECD global minimum tax 2025 corporate income tax"
        query_vec = self.embedder.encode([expanded])[0]

        docs = self.store.search(query_vec, top_k)

        context = ""
        citations = []

        for d in docs:
            context += d["content"] + "\n\n"
            citations.append(f"Page {d['page']}")

        return context.strip(), sorted(set(citations))
