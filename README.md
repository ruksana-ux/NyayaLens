# NyayaLens

AI-powered court-document intelligence for Karnataka District and Subordinate Courts.

## MVP status

This is an early prototype. It currently accepts a user-uploaded PDF and extracts selectable text page by page. Scanned-document OCR, Kannada processing, multi-order chronology, evidence verification, and legal-language explanations are planned, not yet implemented.

## Intended direction

- Extract dates, directions, and procedural events from court orders.
- Reconstruct a chronology across multiple orders.
- Attach page-level evidence to every factual statement.
- Distinguish explicit facts, inferences, and unknowns.
- Begin with English and Kannada, adding other languages only after human-reviewed evaluation.

## Boundaries

NyayaLens is not a lawyer and does not provide legal advice, predict case outcomes, recommend litigation strategy, or calculate legal deadlines. Users must verify important information with their advocate and original court record.

## Run locally

Use Python 3.11 or newer.

PowerShell:
1. python --version
2. python -m venv .venv
3. .venv\Scripts\Activate.ps1
4. python -m pip install -r requirements.txt
5. uvicorn backend.app.main:app --reload

Open http://127.0.0.1:8000/docs. In a second terminal, activate the environment and run: streamlit run frontend/streamlit_app.py

If Python is not recognised, install it from https://www.python.org/downloads/, select Add python.exe to PATH, and reopen the terminal.

See docs/ for architecture, privacy, and limitations.