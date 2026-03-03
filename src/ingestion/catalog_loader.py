# src/ingestion/catalog_loader.py
import json
import os


class PaperCatalog:
    """
    Loads paper_catalog.json and provides fast lookup by filename.
    Used by the ingestion pipeline to enrich chunk metadata with
    clean titles, authors, topics, and abstracts from the catalog.
    """

    def __init__(self, catalog_path: str):
        with open(catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Primary index: filename → paper entry
        self._by_filename = {
            entry["filename"]: entry
            for entry in data["papers"]
        }

        # Secondary index: paper_id → paper entry
        self._by_id = {
            entry["id"]: entry
            for entry in data["papers"]
        }

        self.papers = data["papers"]

    def get_by_filename(self, filename: str) -> dict | None:
        """Look up a paper by its PDF filename."""
        return self._by_filename.get(filename)

    def get_by_id(self, paper_id: str) -> dict | None:
        """Look up a paper by its catalog id (e.g. 'paper_006')."""
        return self._by_id.get(paper_id)

    def get_chunk_metadata(self, filename: str) -> dict:
        """
        Return a metadata dict ready to attach to every chunk of a paper.
        Falls back to filename-derived values if the paper is not in the catalog.
        """
        entry = self.get_by_filename(filename)

        if entry:
            return {
                "paper_id":    entry["id"],
                "paper_title": entry["title"],
                "authors":     "; ".join(entry["authors"]),
                "year":        entry["year"],
                "venue":       entry.get("venue", ""),
                "doi":         entry.get("doi") or "",
                "topics":      "; ".join(entry.get("topics", [])),
                "source_file": filename,
            }

        # Fallback for PDFs not yet in the catalog
        stem = os.path.splitext(filename)[0]
        return {
            "paper_id":    stem.lower().replace(" ", "_"),
            "paper_title": stem,
            "authors":     "Unknown",
            "year":        None,
            "venue":       "",
            "doi":         "",
            "topics":      "",
            "source_file": filename,
        }

    def all_filenames(self) -> list[str]:
        """Return all PDF filenames registered in the catalog."""
        return list(self._by_filename.keys())

    def __len__(self) -> int:
        return len(self.papers)
