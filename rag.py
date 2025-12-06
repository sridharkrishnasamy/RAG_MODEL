# ...existing code...
import json
import google.generativeai as genai

from policies import POLICIES

genai.configure(api_key="AIzaSyDMT2yTbeuZ6khTwM0p8w2WKgBtz5luLWk")


def tokenize(text: str):
    text = text.lower()
    for ch in ",.;:-_()/\\": 
        text = text.replace(ch, " ")
    return [w for w in text.split() if w]

def simple_retrieve(query: str, top_k: int = 3):
    query_words = set(tokenize(query))
    scored = []

    for p in POLICIES:
        policy_words = set(tokenize(p["text"]))
        overlap = query_words.intersection(policy_words)
        score = len(overlap)
        scored.append((score, p))

    scored.sort(key=lambda x: x[0], reverse=True)
    top_policies = [p for score, p in scored if score > 0][:top_k]

    if not top_policies:
        top_policies = POLICIES[:top_k]

    return top_policies

def _contains_keywords(text: str, keywords: set):
    words = set(tokenize(text))
    return bool(words.intersection(keywords))

def evaluate_action(action_description: str):
    """
    Deterministic evaluator (no external API calls) that inspects the action text
    and referenced policies and returns a JSON-compatible decision dict plus the
    list of relevant policies.
    """
    relevant_policies = simple_retrieve(action_description, top_k=3)

    sharing_verbs = {"share", "sharing", "post", "publish", "upload", "disclose", "expose", "leak"}
    student_terms = {"student", "students", "pupil", "pupils", "learner", "learner's", "children", "child"}
    personal_terms = {"personal", "personaldetails", "personal_detail", "name", "email", "address", "phone", "dob", "ssn", "identif", "private"}

    text = action_description.lower()

    is_sharing = _contains_keywords(text, sharing_verbs)
    is_about_students = _contains_keywords(text, student_terms)
    mentions_personal = _contains_keywords(text, personal_terms)
    mentions_consent = "consent" in text or "parent" in text or "guardian" in text
    mentions_anonymize = "anonym" in text or "redact" in text or "remove" in text

    referenced_ids = [p["id"] for p in relevant_policies]

    if is_sharing and is_about_students and mentions_personal:
        decision = "NOT_ALLOWED"
        reasoning = (
            "Sharing students' personal details publicly risks privacy and confidentiality. "
            "Based on the provided policy clauses, this action is disallowed."
        )
        suggestions = [
            "Do not publish personal details of students.",
            "If information must be shared, obtain explicit written consent from the student or guardian and follow data-protection policies.",
            "Consider sharing anonymized or aggregated data instead."
        ]
    elif is_sharing and is_about_students and mentions_anonymize:
        decision = "ALLOWED_WITH_CONDITIONS"
        reasoning = (
            "Sharing limited, anonymized information may be allowed if it cannot be linked to an individual and policies permit it."
        )
        suggestions = [
            "Remove or redact any personally identifying fields (names, emails, phone numbers, IDs).",
            "Document consent and ensure compliance with institutional privacy rules."
        ]
    elif is_sharing and mentions_consent:
        decision = "ALLOWED_WITH_CONDITIONS"
        reasoning = (
            "Action mentions consent; sharing may be allowed only when explicit consent is documented and policies are followed."
        )
        suggestions = [
            "Obtain and record explicit consent from the student or guardian before sharing.",
            "Limit shared fields to those consented to and follow retention/access controls."
        ]
    else:
        decision = "ALLOWED_WITH_CONDITIONS"
        reasoning = (
            "Action is not clearly disallowed by the heuristics, but sharing personal data should be handled cautiously."
        )
        suggestions = [
            "Verify applicable policies and obtain consent where required.",
            "Anonymize data where possible and limit scope of sharing.",
            "If unsure, consult the compliance officer or legal team."
        ]

    result = {
        "decision": decision,
        "reasoning": reasoning,
        "suggestions": suggestions,
        "referenced_policies": referenced_ids
    }

    return result, relevant_policies
