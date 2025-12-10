from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self):
        # Using a compact model for speed and decent semantic quality
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def encode(self, texts_list):
        # Expects a list of strings and returns numpy embeddings
        return self.model.encode(texts_list, convert_to_numpy=True)
