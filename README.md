# PDF Compliance Checker & Summarizer

A RAG-based tool for evaluating PDF compliance against policies and generating document summaries using FAISS vector store and Streamlit UI.

## Features

✅ **Compliance Evaluation** - Check if PDFs comply with your policies  
📝 **Compliance Suggestions** - Get specific recommendations to fix issues  
📄 **Document Summarization** - Generate concise summaries of any PDF  
🔍 **Policy Browser** - Browse and manage compliance policies  
⚡ **FAISS Vector Store** - Fast semantic search using embeddings  
🎨 **Streamlit UI** - Beautiful web interface on localhost  

## Architecture

- **PDF Processing**: Extract text and metadata from PDFs
- **Vector Store**: FAISS-based semantic search using sentence-transformers
- **LLM**: Google Generative AI (Gemini Pro) for compliance analysis
- **UI**: Streamlit for interactive web interface
- **Package Manager**: uv for fast dependency management

## Setup & Installation

### 1. Prerequisites
- Python 3.9+ installed
- `uv` package manager ([install here](https://github.com/astral-sh/uv))
- Google API key from [Google AI Studio](https://makersuite.google.com/app/apikeys)

### 2. Install Dependencies

Using `uv`:
```bash
uv pip install -e .
```

Or with pip:
```bash
pip install -e .
```

### 3. Configure API Key

Copy `.env.example` to `.env` and add your Google API key:
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### 4. Run the Application

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## Project Structure

```
rag_model/
├── app.py                    # Main Streamlit application
├── policies.py               # Compliance policies database
├── pdf_processor.py          # PDF extraction & processing
├── vector_store.py           # FAISS vector store implementation
├── compliance_checker.py     # Compliance evaluation logic
├── pyproject.toml            # Project dependencies (uv)
├── .env.example              # Environment variables template
├── data/
│   ├── policies/             # Policy PDF files
│   ├── uploads/              # Uploaded PDFs
│   └── vector_store/         # FAISS indices
└── README.md                 # This file
```

## Usage

### Compliance Check
1. Select "Compliance Check" mode
2. Upload a Terms & Conditions or Policy PDF
3. Click "🔎 Analyze Compliance"
4. Review:
   - Compliance status (✅ or ❌)
   - Issues found
   - Improvement recommendations
   - Referenced policies

### Summarization
1. Select "Summarization" mode
2. Upload a PDF
3. Click "📝 Generate Summary"
4. View the generated summary

### Policy Browser
1. Select "Policy Browser" mode
2. Browse all compliance policies
3. Filter by category
4. View policy details

## API & Modules

### `pdf_processor.py`
- `extract_text_from_pdf()` - Extract text from PDF files
- `extract_metadata_from_pdf()` - Get PDF metadata (pages, title, author)
- `chunk_text()` - Split text into overlapping chunks
- `save_uploaded_pdf()` - Save uploaded files to disk

### `vector_store.py`
- `FAISSVectorStore` - Main vector store class
  - `add_documents()` - Index documents
  - `search()` - Semantic search
  - `save() / load()` - Persist indices

### `compliance_checker.py`
- `evaluate_compliance()` - Check compliance of document
- `summarize_pdf()` - Generate document summary
- `get_compliance_recommendations()` - Get fix recommendations

### `policies.py`
- `POLICIES` - List of all policies
- `get_policy_by_id()` - Retrieve specific policy
- `get_policies_by_category()` - Filter by category

## Configuration

### Policies
Edit `policies.py` to add/modify compliance policies:
```python
{
    "id": "DP-1",
    "title": "Policy Title",
    "text": "Policy description and requirements...",
    "category": "data_protection"  # e.g., data_protection, marketing, accessibility
}
```

### Models
Change the embedding model in `vector_store.py`:
```python
FAISSVectorStore(model_name="all-mpnet-base-v2")  # For better quality but slower
```

## Performance

- FAISS indexes handle 1000s of policies efficiently
- Vector embeddings cached in memory
- All processing local (no vendor lock-in)
- Typical compliance check: 2-5 seconds

## Requirements

### Core Dependencies
- `streamlit` - Interactive web UI
- `pypdf` - PDF text extraction
- `faiss-cpu` - Vector similarity search
- `sentence-transformers` - Text embeddings
- `google-generativeai` - LLM for analysis
- `python-dotenv` - Environment config

### System Requirements
- ~2GB RAM for FAISS indices
- ~1GB disk for vector store
- Internet connection (for API calls)

## Troubleshooting

**"ModuleNotFoundError: No module named 'faiss'"**
```bash
uv pip install faiss-cpu
```

**"GOOGLE_API_KEY not found"**
- Check `.env` file exists
- Verify API key is set correctly
- Get key from [Google AI Studio](https://makersuite.google.com/app/apikeys)

**"streamlit not found"**
```bash
uv pip install streamlit
```

**FAISS initialization fails**
- Clear `./data/vector_store/` directory
- Restart the application

## Development

Add new features by extending:
- **New policies**: Add to `policies.py`
- **New analysis**: Add functions to `compliance_checker.py`
- **UI changes**: Modify `app.py`

## License

[Your License Here]

## Support

For issues or questions, refer to:
- [Streamlit Documentation](https://docs.streamlit.io/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [Google Generative AI](https://ai.google.dev/)
