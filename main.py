# from vector_store import create_policy_vector_store, get_policy_file_names
# from compliance_checker import evaluate_compliance, API_KEY_AVAILABLE
# from pdf_processor import extract_text_from_pdf


# def main():
#     print("=== PDF Compliance RAG Demo (CLI) ===")

#     if not API_KEY_AVAILABLE:
#         print("WARNING: GROQ_API_KEY not configured in .env file.")
#         print("Get a free key at: https://console.groq.com/keys\n")

#     # Show loaded policy PDFs
#     pdf_files = get_policy_file_names()
#     print(f"\n📚 Policy PDFs loaded ({len(pdf_files)}):")
#     for f in pdf_files:
#         print(f"  - {f}")

#     # Build vector store from policy PDFs
#     print("\nBuilding vector store from policy PDFs...")
#     vector_store = create_policy_vector_store()
#     print(f"✓ {len(vector_store.documents)} chunks indexed\n")

#     # Get document to evaluate
#     path = input("Enter path to PDF to check (or 'quit'):\n> ").strip()
#     if path.lower() == "quit":
#         return

#     text = extract_text_from_pdf(path)
#     print("\nEvaluating compliance...\n")
#     result = evaluate_compliance(text, vector_store)

#     # Display results
#     print("--- Results ---")
#     if result["compliant"] is None:
#         print("Status: UNAVAILABLE (check API key)")
#     elif result["compliant"]:
#         print("Status: ✅ COMPLIANT")
#     else:
#         print("Status: ❌ NON-COMPLIANT")

#     print(f"\nReasoning: {result['reasoning']}")

#     if result["issues"]:
#         print("\nIssues:")
#         for issue in result["issues"]:
#             print(f"  - {issue}")

#     if result["suggestions"]:
#         print("\nSuggestions:")
#         for s in result["suggestions"]:
#             print(f"  - {s}")

#     if result["referenced_policies"]:
#         print("\nRegulations Referenced:")
#         for src in result["referenced_policies"]:
#             print(f"  📄 {src}")


# if __name__ == "__main__":
#     main()
