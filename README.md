# NyayaLens

AI/ML-powered court-document intelligence prototype for Karnataka District and Subordinate Courts.

## What this version does

1. Accepts a user-uploaded PDF containing selectable text.
2. Extracts text page by page with PyMuPDF.
3. Splits text into overlapping chunks while preserving page numbers.
4. Uses a multilingual Sentence Transformer to convert passages and questions into embeddings.
5. Uses cosine similarity to retrieve relevant passages from the uploaded document.
6. Shows the retrieved passages and their original page numbers in a Streamlit interface.

**Important:** this version performs semantic retrieval. It does not generate legal conclusions, provide legal advice, or claim that a retrieved passage is the complete answer. The model is a general multilingual embedding model, not a legal model trained by this project. Kannada quality must be tested before claiming reliable Kannada support.

## Project structure

```text
backend/
  app/
    ingestion/pdf_loader.py
    nlp/chunker.py
    nlp/semantic_search.py
    main.py
frontend/
  streamlit_app.py
research/
  problem_statement.md
docs/
  architecture.md
  privacy.md
  limitations.md
tests/
requirements.txt
```

## Setup on Windows PowerShell

Use Python 3.11 or 3.12.

```powershell
python --version
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks environment activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

## Run the backend

From the repository root, with the virtual environment active:

```powershell
uvicorn backend.app.main:app --reload
```

Open http://127.0.0.1:8000/docs to inspect the API.

## Run the frontend

Open a second terminal in the repository root, activate the same virtual environment, then run:

```powershell
streamlit run frontend/streamlit_app.py
```

## First run note

The first upload loads the Sentence Transformer model. It may download model files from the model hub and can take longer than later requests. A working internet connection is normally needed for the first download. Model inference runs locally after the model is available.

## AI/ML concepts used

- NLP text chunking
- Sentence embeddings
- Multilingual semantic representation
- Cosine similarity
- Top-k information retrieval

The current retrieval output is evidence, not a generated legal answer. The next research stages are OCR for scanned PDFs, legal event extraction, multi-order chronology, Kannada evaluation, and claim-to-source verification.

## Safety and privacy

This is a research prototype, not a legal service. Do not upload confidential, sealed, privileged, or sensitive documents. The current API stores document indexes in process memory only; they disappear when the backend restarts. Do not deploy publicly without authentication, privacy review, retention controls, and security testing. Never commit real case documents to this public repository.

Read the [problem statement](research/problem_statement.md), [architecture](docs/architecture.md), [privacy notes](docs/privacy.md), and [limitations](docs/limitations.md).
