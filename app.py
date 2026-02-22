"""Streamlit application for PDF compliance checking and summarization."""

import streamlit as st
import os
from dotenv import load_dotenv
from pdf_processor import extract_text_from_pdf, extract_metadata_from_pdf, save_uploaded_pdf
from vector_store import create_policy_vector_store, get_policy_file_names
from compliance_checker import evaluate_compliance, summarize_pdf, API_KEY_AVAILABLE

# Load environment variables
load_dotenv()

# Streamlit page configuration
st.set_page_config(
    page_title="PDF Compliance Checker",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .header-text {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .compliance-pass { color: #28a745; font-weight: bold; }
    .compliance-fail { color: #dc3545; font-weight: bold; }
    .policy-box {
        background-color: #f0f2f6;
        padding: 0.8rem;
        border-radius: 0.5rem;
        margin: 0.3rem 0;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


def initialize_vector_store():
    """Initialize FAISS vector store from policy PDFs in data/policies/."""
    if 'vector_store' not in st.session_state:
        with st.spinner("Reading policy PDFs and building vector store..."):
            st.session_state.vector_store = create_policy_vector_store()


def main():
    st.markdown('<p class="header-text">📋 PDF Compliance & Summary Tool</p>', unsafe_allow_html=True)
    st.markdown("Upload a document to check compliance against regulations in `data/policies/`")

    if not API_KEY_AVAILABLE:
        st.warning("""
        ⚠️ **Groq API Key Not Configured**
        
        To enable compliance analysis and summarization:
        1. Get a free key from: https://console.groq.com/keys
        2. Add to `.env` file: `GROQ_API_KEY=your_key_here`
        3. Restart the app
        """)

    st.markdown("---")

    # Initialize vector store from policy PDFs
    initialize_vector_store()

    # Sidebar
    policy_files = get_policy_file_names()
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        mode = st.radio("Select Mode:", ["Compliance Check", "Summarization"])

        st.markdown("---")
        st.markdown("### 📚 Loaded Policy PDFs")
        if policy_files:
            for f in policy_files:
                st.markdown(f"- 📄 {f}")
            st.markdown(f"**{len(policy_files)} regulations loaded**")
            chunks = len(st.session_state.get("vector_store", {}).documents) if hasattr(st.session_state.get("vector_store"), "documents") else "?"
            st.caption(f"Vector store: {chunks} chunks indexed")
        else:
            st.warning("No PDFs found in `data/policies/`")

        st.markdown("---")
        st.markdown("### 🔑 API Status")
        if API_KEY_AVAILABLE:
            st.success("✅ Groq API Key Configured")
        else:
            st.error("❌ Groq API Key Not Set")

        # Button to rebuild vector store
        if st.button("🔄 Rebuild Vector Store"):
            # Delete cached index
            import shutil
            cache_dir = os.path.join("data", "vector_store")
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)
            if 'vector_store' in st.session_state:
                del st.session_state['vector_store']
            st.rerun()

    # --- Mode: Compliance Check ---
    if mode == "Compliance Check":
        st.markdown("### 🔍 Compliance Evaluation")

        if not API_KEY_AVAILABLE:
            st.error("❌ Groq API Key Required for Compliance Checking")
            st.info("Please configure your Groq API key in the .env file.")
        elif not policy_files:
            st.error("❌ No policy PDFs found. Place regulation PDFs in `data/policies/` and restart.")
        else:
            uploaded_file = st.file_uploader(
                "Upload a PDF to check against regulations",
                type="pdf",
                help="The document will be evaluated against all loaded policy PDFs",
                key="compliance_uploader"
            )

            if uploaded_file:
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.info(f"📄 File: {uploaded_file.name}")
                with col2:
                    analyze_btn = st.button("🔎 Analyze Compliance", use_container_width=True)

                if analyze_btn:
                    try:
                        pdf_path = save_uploaded_pdf(uploaded_file)
                        st.session_state.pdf_text = extract_text_from_pdf(pdf_path)
                        st.session_state.pdf_metadata = extract_metadata_from_pdf(pdf_path)
                        st.session_state.analysis_done = True
                    except Exception as e:
                        st.error(f"Error processing PDF: {str(e)}")

                # Show metadata
                if st.session_state.get("pdf_metadata"):
                    with st.expander("📋 Document Metadata"):
                        metadata = st.session_state.pdf_metadata
                        c1, c2, c3 = st.columns(3)
                        c1.metric("Pages", metadata.get("pages", "N/A"))
                        c2.metric("Title", str(metadata.get("title", "Unknown"))[:30])
                        c3.metric("Author", str(metadata.get("author", "Unknown"))[:30])

                # Show compliance results
                if st.session_state.get("analysis_done"):
                    st.markdown("---")
                    st.markdown("### 📊 Compliance Assessment")

                    with st.spinner("Evaluating compliance against loaded regulations..."):
                        result = evaluate_compliance(
                            st.session_state.pdf_text,
                            st.session_state.vector_store
                        )

                    # Status
                    if result["compliant"] is None:
                        st.warning("⚠️ Assessment Unavailable")
                    elif result["compliant"]:
                        st.markdown(
                            "<p style='font-size:1.5rem; color:#28a745; font-weight:bold'>✅ COMPLIANT</p>",
                            unsafe_allow_html=True)
                    else:
                        st.markdown(
                            "<p style='font-size:1.5rem; color:#dc3545; font-weight:bold'>❌ NON-COMPLIANT</p>",
                            unsafe_allow_html=True)

                    # Issues
                    if result["issues"]:
                        st.markdown("#### ⚠️ Issues Found:")
                        for i, issue in enumerate(result["issues"], 1):
                            st.warning(f"{i}. {issue}")

                    # Detailed reasoning
                    st.markdown("#### 📝 Assessment Details:")
                    st.info(result["reasoning"])

                    # Suggestions
                    if result["suggestions"]:
                        st.markdown("#### 💡 Recommendations:")
                        for i, s in enumerate(result["suggestions"], 1):
                            st.success(f"{i}. {s}")

                    # Referenced policy files
                    if result["referenced_policies"]:
                        st.markdown("#### 📚 Regulations Referenced:")
                        for src in result["referenced_policies"]:
                            st.markdown(f"<div class='policy-box'>📄 {src}</div>", unsafe_allow_html=True)

    # --- Mode: Summarization ---
    elif mode == "Summarization":
        st.markdown("### 📄 Document Summarization")

        if not API_KEY_AVAILABLE:
            st.error("❌ Groq API Key Required for Summarization")
            st.info("Please configure your Groq API key in the .env file.")
        else:
            uploaded_file = st.file_uploader(
                "Upload a PDF to summarize",
                type="pdf",
                help="Generate a concise summary of the document"
            )

            if uploaded_file:
                if st.button("📝 Generate Summary", use_container_width=True):
                    try:
                        pdf_path = save_uploaded_pdf(uploaded_file)
                        pdf_text = extract_text_from_pdf(pdf_path)

                        with st.spinner("Generating summary..."):
                            summary = summarize_pdf(pdf_text)

                        st.markdown("#### Summary:")
                        st.info(summary)

                        with st.expander("👀 Original Text Preview"):
                            st.text_area(
                                "Document excerpt:",
                                value=pdf_text[:2000] + "..." if len(pdf_text) > 2000 else pdf_text,
                                height=200,
                                disabled=True
                            )
                    except Exception as e:
                        st.error(f"Error processing PDF: {str(e)}")

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; color:#888; font-size:0.9rem;'>"
        "PDF Compliance Checker v2.0 | Powered by FAISS, Sentence-Transformers & Groq"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
