from sentence_transformers import SentenceTransformer


class TextEmbedder:
    """
    Wrapper around a sentence-transformers embedding model.

    Responsibilities:
    - load the embedding model once
    - provide embedding methods for single text or batch text
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> list[float]:
        vector = self.model.encode(text, normalize_embeddings=True)
        return vector.tolist()

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        vectors = self.model.encode(texts, normalize_embeddings=True)
        return [vector.tolist() for vector in vectors]


embedder = TextEmbedder()