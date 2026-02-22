"""
Setup script to initialize the RAG project.
Run this once before starting the app.
"""

import os
from pathlib import Path
from vector_store import create_policy_vector_store, get_policy_file_names


def setup_project():
    """Initialize project directories and vector store."""

    # Create directories
    dirs = [
        "./data/policies",
        "./data/uploads",
        "./data/vector_store",
    ]
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created {dir_path}")

    # Show policy PDFs
    pdf_files = get_policy_file_names()
    print(f"\n📚 Found {len(pdf_files)} policy PDFs in data/policies/:")
    for f in pdf_files:
        print(f"   - {f}")

    # Build vector store from policy PDFs
    print("\n🔧 Building FAISS vector store from policy PDFs...")
    vector_store = create_policy_vector_store()
    print(f"✓ Indexed {len(vector_store.documents)} chunks")

    # Check for API key
    env_file = Path(".env")
    if not env_file.exists():
        print("\n⚠️  Missing .env file!")
        print("   Create .env with: GROQ_API_KEY=your_key_here")
    else:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY", "").strip()
        if not api_key or api_key == "your_api_key_here":
            print("\n⚠️  GROQ_API_KEY is not configured")
            print("   Get free key from: https://console.groq.com/keys")
            print("   Set in .env: GROQ_API_KEY=your_key_here")
        else:
            print("✓ GROQ_API_KEY configured")

    print("\n✅ Project setup complete!")
    print("Run: streamlit run app.py")


if __name__ == "__main__":
    setup_project()
