# src/chunking/chunker.py
import re
import tiktoken

class TokenChunker:
    def __init__(
        self,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        model: str = "gpt-4"
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoder = tiktoken.encoding_for_model(model)

    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        return len(self.encoder.encode(text))

    def chunk_text(self, text: str, metadata: dict = None) -> list[dict]:
        """
        Split text into overlapping chunks.

        Returns:
            List of chunk dictionaries with text and metadata
        """
        tokens = self.encoder.encode(text)
        chunks = []

        start = 0
        chunk_id = 0

        paper_id = (metadata or {}).get("paper_id", "paper")

        while start < len(tokens):
            end = start + self.chunk_size
            chunk_tokens = tokens[start:end]
            chunk_text = self.encoder.decode(chunk_tokens)

            # Detect page number from [PAGE N] markers present in the chunk text
            page_matches = re.findall(r'\[PAGE (\d+)\]', chunk_text)
            page_number = int(page_matches[0]) if page_matches else None

            chunks.append({
                "chunk_id": f"{paper_id}_chunk_{chunk_id:03d}",
                "text": chunk_text,
                "token_count": len(chunk_tokens),
                "start_token": start,
                "end_token": end,
                "metadata": {
                    **(metadata or {}),
                    "page_number": page_number,
                    "section": None,   # reserved for future heading detection
                }
            })

            start += self.chunk_size - self.chunk_overlap
            chunk_id += 1

        return chunks
