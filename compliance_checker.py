"""Compliance checking and evaluation using RAG with Groq LLM."""

import os
import json
import time
from groq import Groq
from dotenv import load_dotenv
from vector_store import FAISSVectorStore


load_dotenv()

# Configure Groq API key
api_key = os.getenv("GROQ_API_KEY", "").strip()
if not api_key:
    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
if api_key and api_key != "your_api_key_here":
    groq_client = Groq(api_key=api_key)
    API_KEY_AVAILABLE = True
else:
    groq_client = None
    API_KEY_AVAILABLE = False

# Free Groq models to try in order of preference
FREE_MODELS = [
    "llama-3.1-8b-instant",
    "llama3-8b-8192",
    "gemma2-9b-it",
    "mixtral-8x7b-32768",
]


def _call_groq(prompt: str, max_retries: int = 2, retry_delay: int = 30):
    """Call Groq API with automatic model fallback and retry on rate limits."""
    last_error = None
    for model_name in FREE_MODELS:
        for attempt in range(max_retries + 1):
            try:
                response = groq_client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=2048,
                )
                return response.choices[0].message.content
            except Exception as e:
                last_error = e
                error_str = str(e)
                if "429" in error_str or "rate" in error_str.lower() or "limit" in error_str.lower():
                    if attempt < max_retries:
                        time.sleep(retry_delay)
                        continue
                    else:
                        break
                else:
                    break
    raise last_error


def evaluate_compliance(pdf_text: str, policy_vector_store: FAISSVectorStore) -> dict:
    """
    Evaluate uploaded document text against policy PDFs stored in FAISS.
    Retrieves the most relevant policy chunks and asks the LLM to assess compliance.
    """
    if not API_KEY_AVAILABLE:
        return {
            "compliant": None,
            "issues": ["API Key not configured. Please set GROQ_API_KEY in .env file"],
            "reasoning": "Please configure your Groq API key to enable compliance analysis",
            "suggestions": ["1. Get free key from https://console.groq.com/keys",
                            "2. Add GROQ_API_KEY=your_key to .env file",
                            "3. Restart the app"],
            "referenced_policies": []
        }

    # Retrieve the most relevant policy chunks for this document
    relevant_results = policy_vector_store.search(pdf_text[:3000], k=8)
    referenced_sources = list({r["metadata"].get("source_file", "unknown") for r in relevant_results})

    # Build context from retrieved chunks
    policy_context = ""
    for i, r in enumerate(relevant_results, 1):
        source = r["metadata"].get("source_file", "unknown")
        policy_context += f"\n--- Policy Chunk {i} (from: {source}) ---\n{r['text']}\n"

    prompt = f"""You are a legal and regulatory compliance expert. You have been given a document 
and several relevant excerpts from official regulations, acts, and policies.

Your task:
1. Carefully compare the DOCUMENT against the REGULATION EXCERPTS below.
2. Identify any areas where the document violates or fails to comply with the regulations.
3. Be specific — quote the regulation text that is violated and explain why.

DOCUMENT TO EVALUATE:
{pdf_text[:5000]}

REGULATION / POLICY EXCERPTS (retrieved from official policy PDFs):
{policy_context}

Respond ONLY with valid JSON in this exact format:
{{
  "compliant": true or false,
  "issues": ["list of specific compliance issues found"],
  "reasoning": "detailed explanation of the assessment, referencing specific regulations",
  "suggestions": ["specific actionable fixes to achieve compliance"]
}}
"""

    try:
        response_text = _call_groq(prompt)

        # Extract JSON from response
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                result = json.loads(response_text[json_start:json_end])
            else:
                result = {
                    "compliant": False,
                    "issues": ["Could not parse structured assessment"],
                    "reasoning": response_text,
                    "suggestions": []
                }
        except json.JSONDecodeError:
            result = {
                "compliant": False,
                "issues": ["Could not parse structured assessment"],
                "reasoning": response_text,
                "suggestions": []
            }

        return {
            "compliant": result.get("compliant", False),
            "issues": result.get("issues", []),
            "reasoning": result.get("reasoning", ""),
            "suggestions": result.get("suggestions", []),
            "referenced_policies": referenced_sources
        }

    except Exception as e:
        return {
            "compliant": None,
            "issues": [f"Error during evaluation: {str(e)}"],
            "reasoning": "All Groq models hit rate limits. Please wait a minute and try again.",
            "suggestions": ["Wait 60 seconds and retry"],
            "referenced_policies": referenced_sources if 'referenced_sources' in dir() else []
        }


def summarize_pdf(pdf_text: str) -> str:
    """Generate a concise summary of the PDF document."""
    if not API_KEY_AVAILABLE:
        return "Error: API Key not configured. Please set GROQ_API_KEY in .env file."

    prompt = f"""Please provide a concise 3-4 paragraph summary of the following document.
Focus on the key points, obligations, and requirements.

{pdf_text[:8000]}"""

    try:
        return _call_groq(prompt)
    except Exception as e:
        return f"Error generating summary: {str(e)}"
