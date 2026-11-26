"""NyayaLens API: PDF extraction and multilingual semantic evidence retrieval."""
import os
import uuid

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel, Field

from backend.app.ingestion.pdf_loader import extract_pdf_pages
from backend.app.nlp.chunker import split_into_chunks
from backend.app.nlp.semantic_search import (
    IndexedDocument,
    create_document_index,
    retrieve_evidence,
)

app = FastAPI(
    title="NyayaLens AI/ML API",
    description="Page-grounded legal document NLP and semantic retrieval prototype.",
    version="0.2.0",
)

MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_MB", "20")) * 1024 * 1024

# Prototype-only in-memory store. Documents disappear when the API process stops.
DOCUMENTS: dict[str, dict] = {}


class QuestionRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)
    top_k: int = Field(default=5, ge=1, le=10)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "project": "NyayaLens",
        "version": "0.2.0",
        "ai_ml": "multilingual sentence embeddings + semantic retrieval",
    }


@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    """Extract PDF text, chunk it, and create a semantic vector index."""
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")

    content = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="PDF exceeds the upload size limit.")

    try:
        pages = extract_pdf_pages(content)
        chunks = split_into_chunks(pages)
        index = create_document_index(chunks)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="The AI embedding model could not be loaded. Check installation and model download access.",
        ) from exc

    document_id = str(uuid.uuid4())
    DOCUMENTS[document_id] = {
        "filename": file.filename,
        "page_count": len(pages),
        "index": index,
    }

    return {
        "document_id": document_id,
        "filename": file.filename,
        "page_count": len(pages),
        "chunk_count": len(chunks),
        "message": "Document indexed. You can now ask questions about its contents.",
        "notice": "Selectable-text PDFs only. Scanned-page OCR is not implemented.",
    }


@app.post("/documents/{document_id}/ask")
def ask_document(document_id: str, request: QuestionRequest):
    """Retrieve relevant source passages; do not invent an unsupported answer."""
    document = DOCUMENTS.get(document_id)
    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found. Upload it again; this prototype stores indexes only in memory.",
        )

    try:
        evidence = retrieve_evidence(
            request.question,
            document["index"],
            top_k=request.top_k,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "question": request.question,
        "filename": document["filename"],
        "evidence": evidence,
        "answer_policy": (
            "These are semantically relevant source passages, not a legal conclusion. "
            "Read the cited page and consult an advocate for legal interpretation."
        ),
    }
