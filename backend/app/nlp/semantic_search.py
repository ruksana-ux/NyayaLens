"""Multilingual semantic embeddings and evidence retrieval.

The model maps text and questions to vectors. Similarity search retrieves
relevant source passages; it does not generate legal advice.
"""
from dataclasses import dataclass
from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer

from backend.app.nlp.chunker import TextChunk


MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


@lru_cache(maxsize=1)
def load_embedding_model() -> SentenceTransformer:
    """Load the multilingual model once and reuse it."""
    return SentenceTransformer(MODEL_NAME)


@dataclass
class IndexedDocument:
    chunks: list[TextChunk]
    vectors: np.ndarray


def create_document_index(chunks: list[TextChunk]) -> IndexedDocument:
    if not chunks:
        raise ValueError("No readable text was found in this PDF.")

    model = load_embedding_model()
    vectors = model.encode(
        [chunk.text for chunk in chunks],
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    return IndexedDocument(chunks=chunks, vectors=np.asarray(vectors))


def retrieve_evidence(
    question: str,
    index: IndexedDocument,
    top_k: int = 5,
) -> list[dict]:
    """Return the most semantically similar passages with page references."""
    question = question.strip()
    if not question:
        raise ValueError("Please enter a question.")

    model = load_embedding_model()
    query_vector = model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )[0]

    # Because both vectors are normalised, dot product equals cosine similarity.
    scores = index.vectors @ query_vector
    best_indices = np.argsort(scores)[::-1][: max(1, min(top_k, len(scores)))]

    return [
        {
            "chunk_id": index.chunks[i].chunk_id,
            "page_number": index.chunks[i].page_number,
            "text": index.chunks[i].text,
            "similarity": round(float(scores[i]), 4),
        }
        for i in best_indices
    ]
