"""Page-aware extraction for user-supplied PDFs."""
from dataclasses import dataclass
import fitz


@dataclass
class PageText:
    page_number: int
    text: str


def extract_pdf_pages(pdf_bytes: bytes) -> list[PageText]:
    """Extract selectable text while preserving 1-based page numbers."""
    if not pdf_bytes:
        raise ValueError("The uploaded file is empty.")
    try:
        document = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception as exc:
        raise ValueError("The file could not be opened as a valid PDF.") from exc

    try:
        if document.is_encrypted:
            raise ValueError("Password-protected PDFs are not supported yet.")
        return [
            PageText(page_number=i + 1, text=page.get_text("text").strip())
            for i, page in enumerate(document)
        ]
    finally:
        document.close()
