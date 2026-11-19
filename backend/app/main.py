"""NyayaLens API: initial PDF text extraction prototype."""
import os
from fastapi import FastAPI, File, HTTPException, UploadFile
from backend.app.ingestion.pdf_loader import extract_pdf_pages

app = FastAPI(
    title="NyayaLens API",
    description="Evidence-oriented court-document processing prototype.",
    version="0.1.0",
)
MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_MB", "20")) * 1024 * 1024


@app.get("/health")
def health():
    return {"status": "ok", "project": "NyayaLens", "version": "0.1.0"}


@app.post("/documents/extract")
async def extract_document(file: UploadFile = File(...)):
    """Extract selectable text without retaining the uploaded PDF."""
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")
    content = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="PDF exceeds the upload size limit.")
    try:
        pages = extract_pdf_pages(content)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    total_chars = sum(len(page.text) for page in pages)
    return {
        "filename": file.filename,
        "page_count": len(pages),
        "total_characters": total_chars,
        "ocr_required": total_chars == 0,
        "pages": [{"page_number": p.page_number, "text": p.text} for p in pages],
        "notice": "Text extraction only. Scanned-page OCR and legal interpretation are not implemented.",
    }
