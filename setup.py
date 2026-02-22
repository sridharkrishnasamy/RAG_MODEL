"""
Setup script to initialize the RAG project.
Run this once before starting the app.
"""

import os
from pathlib import Path
from vector_store import create_policy_vector_store
from policies import POLICIES


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
    
    # Initialize FAISS vector store with policies
    print("\n📚 Initializing vector store with policies...")
    vector_store = create_policy_vector_store(POLICIES)
    vector_store.save("policies_index.pkl")
    print(f"✓ Indexed {len(POLICIES)} policies")
    
    # Check for API key
    env_file = Path(".env")
    if not env_file.exists():
        print("\n⚠️  Missing .env file!")
        print("   Copy .env.example to .env and add your GOOGLE_API_KEY")
    else:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        if os.getenv("GOOGLE_API_KEY"):
            print("✓ GOOGLE_API_KEY configured")
        else:
            print("⚠️  GOOGLE_API_KEY not set in .env")
    
    print("\n✅ Project setup complete!")
    print("Run: streamlit run app.py")


if __name__ == "__main__":
    setup_project()
