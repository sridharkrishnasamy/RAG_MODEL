# Quick Start Guide

## Prerequisites
- Python 3.9+
- Internet connection (for API calls)
- ~2GB RAM

## Installation (First Time Only)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup project
python setup.py

# 3. Start the app
streamlit run app.py
```

The app will open at: **http://localhost:8501**

---

## Configure API Key (Optional but Recommended)

For compliance checking and summarization:

1. Get API key: https://makersuite.google.com/app/apikeys
2. Edit `.env` file:
   ```
   GOOGLE_API_KEY=your_key_here
   ```
3. Restart the app

---

## Features

### 1. Policy Browser (No API Key Needed)
- Browse 8 compliance policies
- Filter by category
- View full policy details

### 2. Compliance Check (Requires API Key)
- Upload T&C PDF
- Get compliance assessment
- View issues + recommendations

### 3. Summarization (Requires API Key)
- Upload any PDF
- Get AI-powered summary
- Preview original text

---

## Troubleshooting

**Error: ModuleNotFoundError**
```bash
pip install -r requirements.txt
```

**Error: API key not valid**
- Check `.env` file
- Verify key is from https://makersuite.google.com/app/apikeys
- Key should start with `sk-` or similar

**Port 8501 already in use**
```bash
streamlit run app.py --server.port 8502
```

**FAISS error**
```bash
pip install --force-reinstall faiss-cpu
```

---

## Running Again

```bash
streamlit run app.py
```

That's it!

