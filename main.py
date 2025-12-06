from rag import evaluate_action

def main():
    print("=== Simple Governance RAG Demo (No scikit, No bs4) ===\n")
    action = input("Describe your intended action:\n> ")

    result, policies = evaluate_action(action)

    print("\n--- Decision ---")
    print("Decision:", result["decision"])
    print("\nReasoning:")
    print(result["reasoning"])

    print("\nSuggestions:")
    for s in result["suggestions"]:
        print("-", s)

    # print("\nReferenced Policies:")
    # for p_id in result["referenced_policies"]:
    #     print("-", p_id)

    # print("\n--- Policies Considered ---")
    # for p in policies:
    #     print(f"\n[{p['id']}] {p['title']}")
    #     print(p["text"])

if __name__ == "__main__":
    main()
