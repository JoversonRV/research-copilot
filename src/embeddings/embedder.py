# src/embeddings/embedder.py
import voyageai
from typing import List


class VoyageEmbedder:
    """
    Embedder using Voyage AI - Anthropic's recommended embedding provider
    for use with Claude in RAG pipelines.

    Models:
        - voyage-3-large : Best quality (1024 dims) - recommended for academic papers
        - voyage-3        : Balanced quality/cost (1024 dims)
        - voyage-3-lite   : Fastest/cheapest (512 dims)
    """

    def __init__(self, model: str = "voyage-3-large"):
        self.client = voyageai.Client()  # reads VOYAGE_API_KEY from env
        self.model = model

    def embed_texts(self, texts: List[str], input_type: str = "document") -> List[List[float]]:
        """
        Generate embeddings for a list of texts.

        Args:
            texts:      List of strings to embed
            input_type: "document" for indexing, "query" for search queries
        """
        result = self.client.embed(
            texts=texts,
            model=self.model,
            input_type=input_type
        )
        return result.embeddings

    def embed_query(self, query: str) -> List[float]:
        """Generate embedding for a single search query."""
        return self.embed_texts([query], input_type="query")[0]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for documents to be indexed."""
        return self.embed_texts(texts, input_type="document")
