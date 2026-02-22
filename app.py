"""Streamlit application for PDF compliance checking and summarization."""

import streamlit as st
import os
from dotenv import load_dotenv
from pdf_processor import extract_text_from_pdf, extract_metadata_from_pdf, save_uploaded_pdf
from vector_store import create_policy_vector_store
from compliance_checker import evaluate_compliance, summarize_pdf, get_compliance_recommendations
from policies import POLICIES, get_policies_by_category

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
    .compliance-pass {
        color: #28a745;
        font-weight: bold;
    }
    .compliance-fail {
        color: #dc3545;
        font-weight: bold;
    }
    .policy-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_vector_store():
    """Initialize FAISS vector store with policies."""
    if 'vector_store' not in st.session_state:
        with st.spinner("Initializing vector store with policies..."):
            st.session_state.vector_store = create_policy_vector_store(POLICIES)


def main():
    st.markdown('<p class="header-text">📋 PDF Compliance & Summary Tool</p>', unsafe_allow_html=True)
    st.markdown("Evaluate PDF documents for regulatory compliance and generate summaries")
    st.markdown("---")
    
    # Initialize vector store
    initialize_vector_store()
    
    # Sidebar for settings and instructions
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        mode = st.radio(
            "Select Mode:",
            ["Compliance Check", "Summarization", "Policy Browser"]
        )
        
        st.markdown("---")
        st.markdown("### 📚 Policies Overview")
        st.markdown(f"**Total Policies:** {len(POLICIES)}")
        categories = set(p.get("category", "general") for p in POLICIES)
        for cat in sorted(categories):
            count = len(get_policies_by_category(cat))
            st.markdown(f"- {cat.title()}: {count}")
    
    # Mode: Compliance Check
    if mode == "Compliance Check":
        st.markdown("### 🔍 Compliance Evaluation")
        
        uploaded_file = st.file_uploader(
            "Upload a PDF file to check compliance",
            type="pdf",
            help="Select a Terms & Conditions or Policy PDF"
        )
        
        if uploaded_file:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.info(f"📄 File: {uploaded_file.name}")
            
            with col2:
                if st.button("🔎 Analyze Compliance", use_container_width=True):
                    try:
                        # Save and process PDF
                        pdf_path = save_uploaded_pdf(uploaded_file)
                        st.session_state.pdf_text = extract_text_from_pdf(pdf_path)
                        st.session_state.pdf_metadata = extract_metadata_from_pdf(pdf_path)
                        st.session_state.analysis_done = True
                        
                    except Exception as e:
                        st.error(f"Error processing PDF: {str(e)}")
            
            # Display metadata
            if st.session_state.get("pdf_metadata"):
                with st.expander("📋 Document Metadata"):
                    metadata = st.session_state.pdf_metadata
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Pages", metadata.get("pages", "N/A"))
                    col2.metric("Title", metadata.get("title", "Unknown")[:30])
                    col3.metric("Author", metadata.get("author", "Unknown")[:30])
            
            # Display compliance evaluation
            if st.session_state.get("analysis_done"):
                st.markdown("---")
                st.markdown("### 📊 Compliance Assessment")
                
                with st.spinner("Evaluating compliance..."):
                    result = evaluate_compliance(
                        st.session_state.pdf_text,
                        st.session_state.vector_store
                    )
                
                # Compliance status
                compliance_status = "✅ COMPLIANT" if result["compliant"] else "❌ NON-COMPLIANT"
                st.markdown(
                    f"<p style='font-size:1.5rem; color:{'#28a745' if result['compliant'] else '#dc3545'}; "
                    f"font-weight:bold'>{compliance_status}</p>",
                    unsafe_allow_html=True
                )
                
                # Issues
                if result["issues"]:
                    st.markdown("#### ⚠️ Issues Found:")
                    for i, issue in enumerate(result["issues"], 1):
                        st.warning(f"{i}. {issue}")
                
                # Reasoning
                st.markdown("#### 📝 Assessment Details:")
                st.info(result["reasoning"])
                
                # Suggestions
                if result["suggestions"]:
                    st.markdown("#### 💡 Recommendations:")
                    for i, suggestion in enumerate(result["suggestions"], 1):
                        st.success(f"{i}. {suggestion}")
                
                # Referenced policies
                if result["referenced_policies"]:
                    st.markdown("#### 📚 Relevant Policies:")
                    cols = st.columns(min(3, len(result["referenced_policies"])))
                    for idx, policy_id in enumerate(result["referenced_policies"]):
                        from policies import get_policy_by_id
                        policy = get_policy_by_id(policy_id)
                        if policy:
                            with cols[idx % 3]:
                                st.markdown(f"<div class='policy-box'><b>{policy['id']}</b><br>{policy['title']}</div>", 
                                           unsafe_allow_html=True)
    
    # Mode: Summarization
    elif mode == "Summarization":
        st.markdown("### 📄 Document Summarization")
        
        uploaded_file = st.file_uploader(
            "Upload a PDF file to summarize",
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
                    
                    # Preview of original text
                    with st.expander("👀 Original Text Preview"):
                        st.text_area(
                            "Document excerpt:",
                            value=pdf_text[:2000] + "..." if len(pdf_text) > 2000 else pdf_text,
                            height=200,
                            disabled=True
                        )
                    
                except Exception as e:
                    st.error(f"Error processing PDF: {str(e)}")
    
    # Mode: Policy Browser
    elif mode == "Policy Browser":
        st.markdown("### 📚 Browse Compliance Policies")
        
        # Filter by category
        categories = sorted(set(p.get("category", "general") for p in POLICIES))
        selected_category = st.selectbox("Filter by Category:", ["All"] + categories)
        
        # Get policies to display
        if selected_category == "All":
            policies_to_show = POLICIES
        else:
            policies_to_show = get_policies_by_category(selected_category)
        
        # Display policies
        for policy in policies_to_show:
            with st.expander(f"**{policy['id']}** - {policy['title']}"):
                st.markdown(f"**Category:** {policy.get('category', 'general').title()}")
                st.markdown(f"**Content:**\n\n{policy['text']}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #888; font-size: 0.9rem;'>
            <p>PDF Compliance Checker v1.0 | Powered by FAISS & Google Generative AI</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
