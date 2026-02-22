"""PDF processing module for extracting text and metadata from PDF files."""

import os
from pathlib import Path
import tempfile
from pypdf import PdfReader


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
