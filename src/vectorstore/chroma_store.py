# src/vectorstore/chroma_store.py
# NOTE: Uses LanceDB instead of ChromaDB — ChromaDB is not compatible with Python 3.14.
# The public interface (create_collection, add_documents, query) is identical
# so the rest of the codebase does not need to change.
import json
import pyarrow as pa
import lancedb


class ChromaVectorStore:
    """
    Vector store backed by LanceDB.
    Maintains the same interface as the original ChromaDB version.
    """

    EMBEDDING_DIM = 1024  # Default for voyage-3-large

    def __init__(self, persist_directory: str = "./lance_db"):
        self.db = lancedb.connect(persist_directory)
        self.table = None

    def create_collection(self, name: str, embedding_dim: int = 1024):
        """Create or open a table (equivalent to a ChromaDB collection)."""
        self.EMBEDDING_DIM = embedding_dim
        schema = pa.schema([
            pa.field("id", pa.string()),
            pa.field("document", pa.string()),
            pa.field("vector", pa.list_(pa.float32(), embedding_dim)),
            pa.field("metadata_json", pa.string()),
        ])
        if name in self.db.table_names():
            self.table = self.db.open_table(name)
        else:
            self.table = self.db.create_table(name, schema=schema)

    def add_documents(
        self,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict]
    ):
        """Add documents with embeddings and metadata."""
        data = [
            {
                "id": id_,
                "document": doc,
                "vector": emb,
                "metadata_json": json.dumps(meta),
            }
            for id_, doc, emb, meta in zip(ids, documents, embeddings, metadatas)
        ]
        self.table.add(data)

    def query(
        self,
        query_embedding: list[float],
        n_results: int = 5,
        where: dict = None
    ) -> dict:
        """
        Query similar documents.
        Returns dict with keys: documents, metadatas, distances
        (same format as ChromaDB results).
        """
        search = self.table.search(query_embedding).limit(n_results)

        if where:
            filter_expr = " AND ".join(
                f"{k} = '{v}'" for k, v in where.items()
            )
            search = search.where(filter_expr)

        results = search.to_list()

        return {
            "ids":              [[r["id"] for r in results]],
            "documents":        [[r["document"] for r in results]],
            "metadatas":        [[json.loads(r["metadata_json"]) for r in results]],
            "distances":        [[r["_distance"] for r in results]],
            "similarity_scores": [[round(1 - r["_distance"], 4) for r in results]],
        }
