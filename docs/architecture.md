# Architecture

## Current MVP pipeline

1. Upload one user-provided PDF.
2. Validate file type, parseability, and size.
3. Extract selectable text page by page with PyMuPDF.
4. Preserve page numbers with each text segment.
5. Later: add scanned-page OCR and measure OCR quality.
6. Later: extract dates, directions, actors, and procedural events.
7. Later: build chronology across multiple orders.
8. Later: verify every generated claim against source passages and abstain when evidence is missing or conflicting.
9. Later: add human-reviewed English and Kannada explanations.

## Current implementation

- FastAPI endpoints: /health and /documents/extract.
- PyMuPDF text extraction.
- Streamlit local upload interface.
- Uploaded PDF bytes are processed in memory and are not intentionally persisted.

## Core design rule

Never present an inferred event as an explicit court direction. Every factual output should identify its source page and supporting passage. If evidence is absent or conflicting, say so.
