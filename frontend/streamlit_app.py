"""NyayaLens frontend: upload a court order and retrieve evidence with NLP."""
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="NyayaLens AI", page_icon="⚖️", layout="wide")
st.title("NyayaLens")
st.subheader("AI/ML-powered court document intelligence")
st.write(
    "Upload a court-order PDF, then ask a question. The multilingual NLP model "
    "searches for semantically relevant passages and shows their source pages."
)

st.warning(
    "Research prototype only — not legal advice. Do not upload confidential, "
    "sealed, privileged, or sensitive documents. Scanned PDFs are not supported yet."
)

if "document_id" not in st.session_state:
    st.session_state.document_id = None
if "filename" not in st.session_state:
    st.session_state.filename = None

uploaded_file = st.file_uploader("1. Upload a court-order PDF", type=["pdf"])

if uploaded_file and st.button("Process PDF with AI/ML", type="primary"):
    with st.spinner("Extracting text and creating multilingual embeddings. First run may download the model..."):
        try:
            response = requests.post(
                f"{API_URL}/documents/upload",
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "application/pdf",
                    )
                },
                timeout=300,
            )
            response.raise_for_status()
            result = response.json()
            st.session_state.document_id = result["document_id"]
            st.session_state.filename = result["filename"]
            st.success(result["message"])
            st.write(f"Pages processed: **{result['page_count']}**")
            st.write(f"Text chunks indexed: **{result['chunk_count']}**")
            st.caption(result["notice"])
        except requests.RequestException as exc:
            st.error("Could not process the PDF. Confirm that the FastAPI backend is running.")
            if getattr(exc, "response", None) is not None:
                st.code(exc.response.text)
            else:
                st.code(str(exc))

if st.session_state.document_id:
    st.divider()
    st.markdown(f"**Loaded document:** {st.session_state.filename}")
    st.markdown("### 2. Ask a question about this document")
    question = st.text_input(
        "Your question",
        placeholder="Example: What date is mentioned for the next hearing?",
    )
    top_k = st.slider("Number of evidence passages", min_value=1, max_value=10, value=5)

    if st.button("Find supporting passages"):
        if not question.strip():
            st.warning("Please type a question first.")
        else:
            with st.spinner("Finding relevant passages using semantic similarity..."):
                try:
                    response = requests.post(
                        f"{API_URL}/documents/{st.session_state.document_id}/ask",
                        json={"question": question, "top_k": top_k},
                        timeout=120,
                    )
                    response.raise_for_status()
                    result = response.json()

                    st.markdown("### Evidence found in the document")
                    st.info(result["answer_policy"])
                    for number, item in enumerate(result["evidence"], start=1):
                        with st.expander(
                            f"Evidence {number} · Page {item['page_number']} · "
                            f"Similarity {item['similarity']:.3f}",
                            expanded=(number == 1),
                        ):
                            st.write(item["text"])
                except requests.RequestException as exc:
                    st.error("Could not retrieve evidence. The document index may have expired if the backend restarted.")
                    if getattr(exc, "response", None) is not None:
                        st.code(exc.response.text)
                    else:
                        st.code(str(exc))

st.caption(
    "AI method: multilingual sentence embeddings + cosine-similarity retrieval. "
    "The current version retrieves evidence; it does not generate legal advice."
)
