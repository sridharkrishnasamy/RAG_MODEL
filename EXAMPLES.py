"""
Example usage and API reference for the RAG compliance checker project.
"""

# ============================================================================
# Example 1: Using Compliance Checker Standalone
# ============================================================================

from compliance_checker import evaluate_compliance, summarize_pdf
from vector_store import create_policy_vector_store
from pdf_processor import extract_text_from_pdf
from policies import POLICIES

# Initialize vector store with policies
vector_store = create_policy_vector_store(POLICIES)

# Extract text from a PDF
pdf_text = extract_text_from_pdf("path/to/document.pdf")

# Check compliance
compliance_result = evaluate_compliance(pdf_text, vector_store)

print("Compliance Status:", "✅ PASS" if compliance_result["compliant"] else "❌ FAIL")
print("Issues Found:", len(compliance_result["issues"]))
for issue in compliance_result["issues"]:
    print(f"  - {issue}")

print("\nRecommendations:")
for suggestion in compliance_result["suggestions"]:
    print(f"  - {suggestion}")

# ============================================================================
# Example 2: Document Summarization
# ============================================================================

from compliance_checker import summarize_pdf

summary = summarize_pdf(pdf_text)
print("Summary:\n", summary)

# ============================================================================
# Example 3: Vector Store Search
# ============================================================================

from vector_store import FAISSVectorStore

# Create and populate vector store
store = FAISSVectorStore()
documents = [
    {
        "text": "Customer data must not be shared with third parties.",
        "metadata": {"policy_id": "DP-1", "type": "data_protection"}
    },
    {
        "text": "All data must be encrypted with AES-256.",
        "metadata": {"policy_id": "DP-2", "type": "data_protection"}
    }
]
store.add_documents(documents)

# Search for relevant documents
query = "What are the encryption requirements?"
results = store.search(query, k=2)

for i, result in enumerate(results, 1):
    print(f"{i}. {result['text']}")
    print(f"   Score: {result['score']:.4f}")
    print(f"   Metadata: {result['metadata']}\n")

# ============================================================================
# Example 4: Adding Custom Policies
# ============================================================================

from policies import POLICIES, get_policy_by_id, get_policies_by_category

# Add to POLICIES list
new_policy = {
    "id": "SEC-1",
    "title": "Security Standards",
    "text": "All systems must implement multi-factor authentication.",
    "category": "security"
}
POLICIES.append(new_policy)

# Retrieve by ID
policy = get_policy_by_id("SEC-1")
print(f"Retrieved Policy: {policy['title']}")

# Get by category
security_policies = get_policies_by_category("security")
print(f"Security policies: {len(security_policies)}")

# ============================================================================
# Example 5: Batch Processing Multiple PDFs
# ============================================================================

from pathlib import Path
from pdf_processor import extract_text_from_pdf

pdf_dir = Path("./data/uploads")
results = []

for pdf_file in pdf_dir.glob("*.pdf"):
    try:
        # Extract text
        text = extract_text_from_pdf(str(pdf_file))
        
        # Check compliance
        compliance = evaluate_compliance(text, vector_store)
        
        results.append({
            "filename": pdf_file.name,
            "compliant": compliance["compliant"],
            "issues": len(compliance["issues"])
        })
    except Exception as e:
        print(f"Error processing {pdf_file.name}: {e}")

# Display results
for result in results:
    status = "✅" if result["compliant"] else "❌"
    print(f"{status} {result['filename']}: {result['issues']} issues")

# ============================================================================
# Example 6: Saving and Loading Vector Store
# ============================================================================

from vector_store import FAISSVectorStore

# Create and save
store = FAISSVectorStore()
store.add_documents([...])
store.save("my_policies.pkl")

# Load later
store_loaded = FAISSVectorStore()
store_loaded.load("my_policies.pkl")

# Use immediately
results = store_loaded.search("data privacy")

# ============================================================================
# Example 7: Programmatic Streamlit Integration
# ============================================================================

import streamlit as st
from compliance_checker import evaluate_compliance

st.title("Compliance Checker")

# File uploader
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    # Save and process
    from pdf_processor import save_uploaded_pdf, extract_text_from_pdf
    
    pdf_path = save_uploaded_pdf(uploaded_file)
    pdf_text = extract_text_from_pdf(pdf_path)
    
    # Check compliance
    result = evaluate_compliance(pdf_text, st.session_state.vector_store)
    
    # Display
    if result["compliant"]:
        st.success("✅ Document is compliant")
    else:
        st.error("❌ Compliance issues found:")
        for issue in result["issues"]:
            st.warning(issue)

# ============================================================================
# Example 8: Configuration and Environment
# ============================================================================

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not set in .env")

# Configure API
import google.generativeai as genai
genai.configure(api_key=api_key)

print("✓ Configured successfully")

# ============================================================================
# Example 9: Advanced Text Chunking
# ============================================================================

from pdf_processor import chunk_text, extract_text_from_pdf

# Extract and chunk
pdf_text = extract_text_from_pdf("large_document.pdf")

# Create chunks with custom parameters
chunks = chunk_text(
    pdf_text,
    chunk_size=1000,      # Larger chunks for context
    overlap=200           # More overlap for better retrieval
)

print(f"Created {len(chunks)} chunks")

# Index chunks
from vector_store import FAISSVectorStore
store = FAISSVectorStore()
store.add_documents(chunks)

# Search across chunks
results = store.search("specific compliance requirement", k=5)

# ============================================================================
# Example 10: Error Handling and Logging
# ============================================================================

import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Process PDF
    pdf_text = extract_text_from_pdf("document.pdf")
    logger.info("PDF extracted successfully")
    
    # Check compliance
    result = evaluate_compliance(pdf_text, vector_store)
    logger.info(f"Compliance check complete: {result['compliant']}")
    
except FileNotFoundError as e:
    logger.error(f"PDF not found: {e}")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise

print("\n✅ All examples completed successfully!")
