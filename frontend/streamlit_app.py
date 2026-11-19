"""Local Streamlit interface for NyayaLens."""
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"
st.set_page_config(page_title="NyayaLens", page_icon="⚖️", layout="wide")
st.title("NyayaLens")
st.caption("Court-document understanding prototype")

st.warning(
    "Research prototype only; not legal advice. Do not upload confidential, "
    "sealed, or sensitive documents. Scanned-document OCR is not implemented."
)
uploaded = st.file_uploader("Choose a court-order PDF", type=["pdf"])

if uploaded and st.button("Extract document text"):
    try:
        response = requests.post(
            f"{API_URL}/documents/extract",
            files={"file": (uploaded.name, uploaded.getvalue(), "application/pdf")},
            timeout=90,
        )
        response.raise_for_status()
        result = response.json()
        st.write(f"Pages: {result['page_count']}")
        st.write(f"Characters extracted: {result['total_characters']}")
        if result["ocr_required"]:
            st.info("No selectable text found. OCR is not included yet.")
        for page in result["pages"]:
            with st.expander(f"Page {page['page_number']}"):
                st.text(page["text"] or "[No selectable text on this page]")
        st.caption(result["notice"])
    except requests.RequestException as exc:
        st.error("Could not reach the API. Start it with: uvicorn backend.app.main:app --reload")
        st.code(str(exc))
