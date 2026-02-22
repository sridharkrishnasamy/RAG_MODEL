"""Compliance checking and evaluation using RAG with LLM."""

import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from vector_store import FAISSVectorStore
from policies import POLICIES, get_policy_by_id


load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY", ""))


def evaluate_compliance(pdf_text: str, policy_vector_store: FAISSVectorStore) -> dict:
    """
    Evaluate compliance of document against policies.
    
    Args:
        pdf_text: Extracted text from PDF
        policy_vector_store: FAISS vector store with policies
        
    Returns:
        Compliance evaluation result
    """
    # Retrieve relevant policies
    relevant_results = policy_vector_store.search(pdf_text, k=4)
    relevant_policies = [r["metadata"]["policy_id"] for r in relevant_results]
    
    prompt = f"""You are a compliance expert. Analyze the following document against the compliance policies provided.

DOCUMENT TO EVALUATE:
{pdf_text[:5000]}...

RELEVANT COMPLIANCE POLICIES:
"""
    
    for policy_id in relevant_policies:
        policy = get_policy_by_id(policy_id)
        if policy:
            prompt += f"\n[{policy['id']}] {policy['title']}\n{policy['text']}\n"
    
    prompt += """
Please provide:
1. COMPLIANT: true/false - Is the document compliant with policies?
2. ISSUES: List any compliance issues found
3. REASONING: Explanation of your assessment
4. SUGGESTIONS: Specific changes needed for compliance

Format your response as JSON."""
    
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        
        # Parse response
        response_text = response.text
        
        # Try to extract JSON
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            json_str = response_text[json_start:json_end]
            result = json.loads(json_str)
        except:
            result = {
                "compliant": False,
                "issues": ["Unable to parse detailed assessment"],
                "reasoning": response_text,
                "suggestions": []
            }
        
        return {
            "compliant": result.get("compliant", False),
            "issues": result.get("issues", []),
            "reasoning": result.get("reasoning", ""),
            "suggestions": result.get("suggestions", []),
            "referenced_policies": relevant_policies
        }
        
    except Exception as e:
        return {
            "compliant": False,
            "issues": [f"Error during evaluation: {str(e)}"],
            "reasoning": "API call failed",
            "suggestions": [],
            "referenced_policies": relevant_policies
        }


def summarize_pdf(pdf_text: str) -> str:
    """
    Generate a concise summary of the PDF document.
    
    Args:
        pdf_text: Extracted text from PDF
        
    Returns:
        Summary text
    """
    prompt = f"""Please provide a concise 3-4 paragraph summary of the following document:

{pdf_text[:8000]}...

Focus on the key points and main obligations or requirements."""
    
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {str(e)}"


def get_compliance_recommendations(issue_text: str) -> list:
    """
    Get specific recommendations to fix a compliance issue.
    
    Args:
        issue_text: Description of the compliance issue
        
    Returns:
        List of recommendations
    """
    prompt = f"""Given this compliance issue:
"{issue_text}"

Provide 3-5 specific, actionable recommendations to address this issue. Format as a numbered list."""
    
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        
        # Parse recommendations
        lines = response.text.split('\n')
        recommendations = [line.strip() for line in lines if line.strip() and any(c.isdigit() for c in line.split()[0])]
        
        return recommendations if recommendations else [response.text]
    except Exception as e:
        return [f"Error getting recommendations: {str(e)}"]
