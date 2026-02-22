"""FAISS-based vector store for semantic search and retrieval."""

import os
import pickle
import numpy as np
import faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer


class FAISSVectorStore:
    """Simple FAISS vector store for document retrieval."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the vector store with a sentence transformer model.
        
        Args:
            model_name: Name of the sentence-transformers model to use
        """
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents = []
        self.store_path = Path("./data/vector_store")
        self.store_path.mkdir(parents=True, exist_ok=True)
    
    def add_documents(self, documents: list) -> None:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of document strings or dicts with 'text' and optional 'metadata'
        """
        processed_docs = []
        for doc in documents:
            if isinstance(doc, dict):
                processed_docs.append(doc)
            else:
                processed_docs.append({"text": doc, "metadata": {}})
        
        # Generate embeddings
        texts = [doc["text"] for doc in processed_docs]
        embeddings = self.model.encode(texts)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings, dtype=np.float32))
        
        self.documents = processed_docs
    
    def search(self, query: str, k: int = 3) -> list:
        """
        Search for similar documents.
        
        Args:
            query: Query string
            k: Number of results to return
            
        Returns:
            List of tuples (document, score)
        """
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
        """Save the vector store and index to disk."""
        filepath = self.store_path / filename
        with open(filepath, "wb") as f:
            pickle.dump({
                "documents": self.documents,
                "index": self.index,
                "model_name": "all-MiniLM-L6-v2",
            }, f)
    
    def load(self, filename: str = "vector_store.pkl") -> None:
        """Load a vector store from disk."""
        filepath = self.store_path / filename
        if filepath.exists():
            with open(filepath, "rb") as f:
                data = pickle.load(f)
                self.documents = data["documents"]
                self.index = data["index"]


def create_policy_vector_store(policies: list) -> FAISSVectorStore:
    """
    Create a vector store from policy documents.
    
    Args:
        policies: List of policy dictionaries with 'id', 'title', 'text'
        
    Returns:
        FAISSVectorStore instance with policies indexed
    """
    store = FAISSVectorStore()
    
    documents = []
    for policy in policies:
        doc = {
            "text": f"{policy['title']}\n\n{policy['text']}",
            "metadata": {
                "policy_id": policy["id"],
                "title": policy["title"],
                "category": policy.get("category", "general")
            }
        }
        documents.append(doc)
    
    store.add_documents(documents)
    return store
