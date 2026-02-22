# Installation & Setup Verification Checklist

## Pre-Installation

- [ ] Python 3.9+ installed: `python --version`
- [ ] uv package manager installed: `uv --version`
- [ ] Internet connection available (for API calls)
- [ ] 2GB+ RAM available
- [ ] ~200MB disk space for dependencies

## Step-by-Step Installation

### 1. Environment Setup (Windows PowerShell)
```powershell
# Open PowerShell in project directory
cd ~/projects/rag_model

# Run startup script
.\run.ps1

# Script will:
# ✓ Create virtual environment
# ✓ Install dependencies
# ✓ Setup project
# ✓ Verify .env file
# ✓ Start Streamlit app
```

### 2. Manual Setup (Alternative)

#### Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows
```
- [ ] Virtual environment created

#### Install Dependencies
```bash
uv pip install -e .
```
Or with pip:
```bash
pip install -r requirements.txt
```
- [ ] Dependencies installed (6 packages)

#### Configure API Key
```bash
# Copy template
cp .env.example .env

# Edit .env
# GOOGLE_API_KEY=your_key_from_https://makersuite.google.com/app/apikeys
```
- [ ] `.env` file created
- [ ] `GOOGLE_API_KEY` added

#### Initialize Project
```bash
python setup.py
```
- [ ] Directories created
- [ ] Vector store initialized
- [ ] Policies indexed

## Verification Checklist

### Dependencies
```bash
python -c "import streamlit; print('✓ Streamlit')"
python -c "import PyPDF2; print('✓ PyPDF')"
python -c "import faiss; print('✓ FAISS')"
python -c "import sentence_transformers; print('✓ Sentence-Transformers')"
python -c "import google.generativeai; print('✓ Google Generative AI')"
python -c "import dotenv; print('✓ python-dotenv')"
```

- [ ] All 6 dependencies imported successfully

### Project Files
```bash
# Check required files
test -f app.py && echo "✓ app.py"
test -f policies.py && echo "✓ policies.py"
test -f pdf_processor.py && echo "✓ pdf_processor.py"
test -f vector_store.py && echo "✓ vector_store.py"
test -f compliance_checker.py && echo "✓ compliance_checker.py"
test -f .env && echo "✓ .env"
```

- [ ] All core modules present
- [ ] `.env` file configured

### Directory Structure
```bash
mkdir -p data/policies data/uploads data/vector_store
ls -la data/
```

- [ ] `data/` directory exists
- [ ] Subdirectories created

### API Configuration
```bash
grep GOOGLE_API_KEY .env
# Should show non-empty value
```

- [ ] API key is set
- [ ] API key is not "your_key_here"

## Running the Application

### Start with Script
```bash
# Windows PowerShell
.\run.ps1

# Windows CMD
run.bat

# Linux/macOS
bash run.sh
```

### Start Manually
```bash
# Activate venv first
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows

# Run app
streamlit run app.py
```

### Expected Output
```
Streamlit version X.XX.X
  
  URL: http://localhost:8501
  Network URL: http://192.168.X.X:8501
```

- [ ] App starts without errors
- [ ] Browser opens to http://localhost:8501

## Feature Testing

### Test Compliance Check
1. [ ] Select "Compliance Check" mode
2. [ ] Upload a PDF file (or use sample)
3. [ ] Click "🔎 Analyze Compliance"
4. [ ] Verify results display (2-5 seconds)
5. [ ] Check compliance status shows (✅ or ❌)

### Test Summarization
1. [ ] Select "Summarization" mode
2. [ ] Upload a PDF file
3. [ ] Click "📝 Generate Summary"
4. [ ] Verify summary generates (3-7 seconds)
5. [ ] Check preview is displayed

### Test Policy Browser
1. [ ] Select "Policy Browser" mode
2. [ ] Verify 8 policies are listed
3. [ ] Filter by category
4. [ ] Expand policies to view details
5. [ ] All policies display correctly

## Troubleshooting

### Issue: "ModuleNotFoundError"
```bash
# Solution: Reinstall dependencies
uv pip install -e .
# or
pip install -r requirements.txt
```

### Issue: "GOOGLE_API_KEY not found"
```bash
# Solution: Create and configure .env
cp .env.example .env
# Edit .env file with your API key
```

### Issue: "Port 8501 already in use"
```bash
# Solution: Use different port
streamlit run app.py --server.port 8502
```

### Issue: "FAISS error"
```bash
# Solution: Reinstall FAISS
uv pip install --force-reinstall faiss-cpu
```

### Issue: Slow Performance
- [ ] Check internet connection (API calls)
- [ ] Check CPU/RAM usage (use system monitor)
- [ ] Try smaller PDFs first
- [ ] Increase system resources

## Performance Verification

After setup, test performance:

```bash
# Time compliance check
time python -c "
from compliance_checker import evaluate_compliance
from vector_store import create_policy_vector_store
from policies import POLICIES

store = create_policy_vector_store(POLICIES)
# Should complete in <5 seconds
"
```

- [ ] Compliance check: <5 seconds
- [ ] Vector search: <200ms
- [ ] Memory usage: <500MB

## Next Steps After Verification

1. [ ] Configure additional policies in `policies.py`
2. [ ] Test with your own PDFs
3. [ ] Customize Streamlit theme in `.streamlit/config.toml`
4. [ ] Deploy with Docker if needed:
   ```bash
   docker-compose up --build
   ```

## Additional Resources

- **Full Documentation**: See `README.md`
- **Quick Reference**: See `QUICKSTART.md`
- **Project Overview**: See `PROJECT_SUMMARY.md`
- **Code Examples**: See `EXAMPLES.py`
- **Streamlit Docs**: https://docs.streamlit.io/
- **FAISS Docs**: https://github.com/facebookresearch/faiss/wiki
- **Google AI**: https://ai.google.dev/

## Support

If you encounter issues:

1. Check this checklist for missing steps
2. Review README.md for detailed info
3. Look at EXAMPLES.py for code samples
4. Check Streamlit logs: `streamlit run app.py --logger.level=debug`
5. Verify API key is valid at https://makersuite.google.com/app/apikeys

---

**Last Updated**: February 22, 2026  
**Status**: Ready for Production ✅

All items checked? 🎉 Your installation is complete!
