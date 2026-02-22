# PDF Compliance Checker & Summarizer

A RAG-based tool for evaluating PDF documents for regulatory compliance and generating summaries using FAISS semantic search and Streamlit web interface.

## Features

✅ **Compliance Evaluation** - Check if PDFs comply with your policies  
📝 **Compliance Suggestions** - Get specific recommendations to fix issues  
📄 **Document Summarization** - Generate concise AI-powered summaries  
🔍 **Policy Browser** - Browse and manage compliance policies (works without API key)  
⚡ **FAISS Vector Store** - Fast semantic search using embeddings  
🎨 **Streamlit UI** - Beautiful web interface on localhost  

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Project
```bash
python setup.py
```

### 3. Run the App
```bash
streamlit run app.py
```

**Access**: http://localhost:8501

---

## Configuration

### API Key (Optional for Compliance & Summarization)

1. Get free API key: https://makersuite.google.com/app/apikeys
2. Add to `.env` file:
   ```
   GOOGLE_API_KEY=your_key_here
   ```

**Note**: You can still browse policies without an API key.

---

## Project Structure

```
rag_model/
├── app.py                    # Main Streamlit UI
├── policies.py               # 8 compliance policies
├── pdf_processor.py          # PDF extraction & metadata
├── vector_store.py           # FAISS semantic search
├── compliance_checker.py     # LLM-based analysis
├── setup.py                  # Project initialization
├── requirements.txt          # Dependencies
├── .env.example              # API key template
├── README.md                 # Documentation
└── data/
    ├── policies/             # Policy PDFs
    ├── uploads/              # User uploads
    └── vector_store/         # FAISS indices
```

---

## Features Overview

### 1. Policy Browser
- Browse all 8 compliance policies
- Filter by category (Data Protection, Marketing, Accessibility, Terms, Privacy)
- View full policy details
- **Works without API key ✅**

### 2. Compliance Evaluation
- Upload T&C or Policy PDFs
- Automated compliance checking
- Identifies issues with explanations
- Suggests specific remediation steps
- Shows relevant policies
- **Requires API key**

### 3. Document Summarization
- Upload any PDF
- AI-powered 3-4 paragraph summary
- Original text preview
- **Requires API key**

---

## Policies Included

| ID | Title | Category |
|----|-------|----------|
| DP-1 | Data Sharing Policy | Data Protection |
| DP-2 | Data Encryption Policy | Data Protection |
| DP-3 | Data Retention Policy | Data Protection |
| MK-1 | Marketing Consent | Marketing |
| MK-2 | Advertising Standards | Marketing |
| ACC-1 | Accessibility Compliance | Accessibility |
| T&C-1 | Terms & Conditions | Terms |
| GDPR-1 | GDPR Compliance | Privacy |

---

## Technology Stack

| Component | Package | Purpose |
|-----------|---------|---------|
| Web UI | Streamlit | Interactive interface |
| PDF Processing | PyPDF | Extract text & metadata |
| Vector Store | FAISS | Semantic search |
| Embeddings | Sentence-Transformers | Text vectorization |
| LLM | Google Generative AI | Analysis & summarization |
| Config | python-dotenv | Environment management |

---

## Troubleshooting

### ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### API Key Error
- Check `.env` file exists
- Verify key is from https://makersuite.google.com/app/apikeys
- Restart app after updating key

### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

### FAISS Error
```bash
pip install --force-reinstall faiss-cpu
```

---

## Adding Custom Policies

Edit `policies.py`:

```python
{
    "id": "CUSTOM-1",
    "title": "Your Policy Title",
    "text": "Your policy description...",
    "category": "your_category"
}
```

Available categories: `data_protection`, `marketing`, `accessibility`, `terms`, `privacy`, `general`

---

## Performance

- Compliance check: 2-5 seconds
- Summarization: 3-7 seconds
- Vector search: <100ms
- Memory: ~500MB

---

## Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [FAISS GitHub](https://github.com/facebookresearch/faiss)
- [Sentence Transformers](https://www.sbert.net/)
- [Google Generative AI](https://ai.google.dev/)
- [PyPDF](https://github.com/py-pdf/PyPDF)

---

## License

MIT

---

**Version**: 1.0  
**Last Updated**: February 2026
