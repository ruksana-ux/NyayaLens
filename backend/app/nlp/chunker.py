"""Split extracted legal text into overlapping, page-linked chunks."""
from dataclasses import dataclass
import re

from backend.app.ingestion.pdf_loader import PageText


@dataclass
class TextChunk:
    chunk_id: int
    page_number: int
    text: str


def split_into_chunks(
    pages: list[PageText],
    chunk_size: int = 900,
    overlap: int = 150,
) -> list[TextChunk]:
    """Create chunks without losing the source page number."""
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("Use chunk_size > overlap >= 0.")

    chunks: list[TextChunk] = []
    for page in pages:
        # Collapse excess whitespace but retain the text content.
        text = re.sub(r"\s+", " ", page.text).strip()
        if not text:
            continue

        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))

            # Prefer ending at a word boundary when possible.
            if end < len(text):
                boundary = text.rfind(" ", start, end)
                if boundary > start + chunk_size // 2:
                    end = boundary

            piece = text[start:end].strip()
            if piece:
                chunks.append(
                    TextChunk(
                        chunk_id=len(chunks) + 1,
                        page_number=page.page_number,
                        text=piece,
                    )
                )

            if end >= len(text):
                break
            start = max(end - overlap, start + 1)

    return chunks
