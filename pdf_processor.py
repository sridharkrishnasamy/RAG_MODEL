"""PDF processing module for extracting text and metadata from PDF files."""

import os
from pathlib import Path
import tempfile
from pypdf import PdfReader


def validate_document_type(text: str) -> tuple[bool, str]:
    """
    Validate if the document is a recognized valid document type.
    
    Checks for: Sale Deed, IT Terms & Conditions, Legal/Policy documents.
    
    Args:
        text: Extracted text from the PDF
        
    Returns:
        Tuple of (is_valid, document_type)
    """
    text_lower = text.lower()
    
    # Keywords for different valid document types
    sale_deed_keywords = ["sale deed", "property", "seller", "buyer", "conveyance", "registered", "immovable property"]
    it_terms_keywords = ["terms and conditions", "terms of service", "software", "license", "intellectual property", "it services", "software services"]
    legal_keywords = ["agreement", "policy", "compliance", "regulation", "governing", "effective date", "hereby"]
    
    # Count keyword matches
    sale_deed_count = sum(1 for kw in sale_deed_keywords if kw in text_lower)
    it_terms_count = sum(1 for kw in it_terms_keywords if kw in text_lower)
    legal_count = sum(1 for kw in legal_keywords if kw in text_lower)
    
    # Document is valid if it has reasonable keyword matches
    if sale_deed_count >= 3:
        return True, "Sale Deed"
    elif it_terms_count >= 3:
        return True, "IT Terms & Conditions"
    elif legal_count >= 3:
        return True, "Legal/Policy Document"
    
    return False, "Unknown"


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract all text from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text content
    """
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text.strip()
    except Exception as e:
        raise ValueError(f"Error reading PDF: {str(e)}")


def extract_metadata_from_pdf(pdf_path: str) -> dict:
    """
    Extract metadata from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary with metadata
    """
    try:
        reader = PdfReader(pdf_path)
        metadata = reader.metadata or {}
        return {
            "title": metadata.get("/Title", "Unknown"),
            "author": metadata.get("/Author", "Unknown"),
            "pages": len(reader.pages),
            "producer": metadata.get("/Producer", "Unknown"),
        }
    except Exception as e:
        return {"error": str(e)}


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    """
    Split text into overlapping chunks for better retrieval.
    
    Args:
        text: The text to chunk
        chunk_size: Size of each chunk in characters
        overlap: Number of overlapping characters between chunks
        
    Returns:
        List of text chunks
    """
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i : i + chunk_size]
        if chunk.strip():
            chunks.append(chunk)
    return chunks


def save_uploaded_pdf(uploaded_file) -> str:
    """
    Save uploaded PDF to temporary location and return path.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        Path to the saved file
    """
    temp_dir = Path("./data/uploads")
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = temp_dir / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return str(file_path)
