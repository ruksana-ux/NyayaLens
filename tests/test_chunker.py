from backend.app.nlp.chunker import split_into_chunks
from backend.app.ingestion.pdf_loader import PageText


def test_chunker_preserves_source_page():
    pages = [PageText(page_number=4, text="The court directed the matter to be listed again. " * 30)]
    chunks = split_into_chunks(pages, chunk_size=100, overlap=20)
    assert len(chunks) > 1
    assert all(chunk.page_number == 4 for chunk in chunks)
    assert all(chunk.text for chunk in chunks)


def test_chunker_rejects_invalid_overlap():
    pages = [PageText(page_number=1, text="Sample text")]
    try:
        split_into_chunks(pages, chunk_size=10, overlap=10)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected invalid overlap to raise ValueError")
