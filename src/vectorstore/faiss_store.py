import faiss
import numpy as np

class FAISSStore:
    def __init__(self, dim=384):
        self.index = faiss.IndexFlatL2(dim)
        self.documents = []

    def add(self, embeddings, docs):
        embeddings_np = np.array(embeddings).astype("float32")
        self.index.add(embeddings_np)
        self.documents.extend(docs)

    def search(self, query_embedding, top_k=3):
        q = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(q, top_k)
        results = []
        for idx in indices[0]:
            if idx < len(self.documents):
                results.append(self.documents[idx])
        return results
