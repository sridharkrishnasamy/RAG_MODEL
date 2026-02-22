"""FAISS-based vector store for semantic search and retrieval."""

import os
import pickle
import numpy as np
import faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer
from pdf_processor import extract_text_from_pdf, chunk_text


POLICIES_DIR = Path("./data/policies")


class FAISSVectorStore:
    """Simple FAISS vector store for document retrieval."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents = []
        self.store_path = Path("./data/vector_store")
        self.store_path.mkdir(parents=True, exist_ok=True)

    def add_documents(self, documents: list) -> None:
        """Add documents (list of dicts with 'text' and 'metadata') to the index."""
        processed_docs = []
        for doc in documents:
            if isinstance(doc, dict):
                processed_docs.append(doc)
            else:
                processed_docs.append({"text": doc, "metadata": {}})

        texts = [doc["text"] for doc in processed_docs]
        embeddings = self.model.encode(texts, show_progress_bar=False)

        dimension = embeddings.shape[1]
        if self.index is None:
            self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings, dtype=np.float32))
        self.documents.extend(processed_docs)

    def search(self, query: str, k: int = 5) -> list:
        """Return top-k most similar chunks."""
        if self.index is None or len(self.documents) == 0:
            return []

        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(query_embedding, min(k, len(self.documents)))

        results = []
        for distance, idx in zip(distances[0], indices[0]):
            if idx >= 0:
                results.append({
                    "text": self.documents[idx]["text"],
                    "metadata": self.documents[idx].get("metadata", {}),
                    "score": float(distance)
                })
        return results

    def save(self, filename: str = "vector_store.pkl") -> None:
        filepath = self.store_path / filename
        with open(filepath, "wb") as f:
            pickle.dump({"documents": self.documents}, f)
        faiss.write_index(self.index, str(self.store_path / "faiss.index"))

    def load(self, filename: str = "vector_store.pkl") -> bool:
        filepath = self.store_path / filename
        index_path = self.store_path / "faiss.index"
        if filepath.exists() and index_path.exists():
            with open(filepath, "rb") as f:
                data = pickle.load(f)
                self.documents = data["documents"]
            self.index = faiss.read_index(str(index_path))
            return True
        return False


def load_policy_pdfs() -> list:
    """
    Read every PDF in data/policies/, chunk the text, and return
    a list of document dicts ready for the vector store.
    """
    documents = []
    if not POLICIES_DIR.exists():
        return documents

    for pdf_file in sorted(POLICIES_DIR.glob("*.pdf")):
        try:
            full_text = extract_text_from_pdf(str(pdf_file))
            if not full_text.strip():
                continue
            chunks = chunk_text(full_text, chunk_size=800, overlap=100)
            for i, chunk in enumerate(chunks):
                documents.append({
                    "text": chunk,
                    "metadata": {
                        "source_file": pdf_file.name,
                        "chunk_index": i,
                        "total_chunks": len(chunks),
                    }
                })
        except Exception as e:
            print(f"[Warning] Could not process {pdf_file.name}: {e}")
    return documents


def get_policy_file_names() -> list:
    """Return list of PDF filenames in the policies directory."""
    if not POLICIES_DIR.exists():
        return []
    return sorted(f.name for f in POLICIES_DIR.glob("*.pdf"))


def create_policy_vector_store() -> FAISSVectorStore:
    """
    Build (or load cached) FAISS vector store from policy PDFs in data/policies/.
    """
    store = FAISSVectorStore()

    # Try loading cached index first
    if store.load():
        print(f"✓ Loaded cached vector store ({len(store.documents)} chunks)")
        return store

    # Build fresh from PDFs
    documents = load_policy_pdfs()
    if documents:
        store.add_documents(documents)
        store.save()
        print(f"✓ Indexed {len(documents)} chunks from {len(get_policy_file_names())} policy PDFs")
    else:
        print("⚠ No policy PDFs found in data/policies/")
    return store
