POLICIES = [
    {
        "id": "DP-1",
        "title": "Data Sharing Policy",
        "text": "Customer personal data must not be shared with third parties without explicit consent. Data includes names, email addresses, phone numbers, and identifiable information. Violations result in immediate data protection compliance issues.",
        "category": "data_protection"
    },
    {
        "id": "DP-2",
        "title": "Data Encryption Policy",
        "text": "All sensitive customer data must be stored in encrypted form using AES-256 or equivalent. Encryption keys must be securely managed. Unencrypted storage of personal data is prohibited.",
        "category": "data_protection"
    },
    {
        "id": "DP-3",
        "title": "Data Retention Policy",
        "text": "Customer data must be deleted within 30 days of account termination or after 12 months of inactivity. Backup retention follows the same rules. Archival requires explicit regulatory exceptions.",
        "category": "data_protection"
    },
    {
        "id": "MK-1",
        "title": "Marketing Consent Policy",
        "text": "Marketing emails can only be sent to customers who have explicitly opted in. Opt-out requests must be honored within 24 hours. Marketing communications must include unsubscribe links.",
        "category": "marketing"
    },
    {
        "id": "MK-2",
        "title": "Advertising Standards",
        "text": "All advertisements must be truthful and not misleading. Claims must be substantiated by evidence. Prohibited content includes hate speech, discrimination, and false health claims.",
        "category": "marketing"
    },
    {
        "id": "ACC-1",
        "title": "Accessibility Compliance",
        "text": "All digital content must comply with WCAG 2.1 Level AA standards. Images require alt text, videos require captions, and color contrast ratios must meet minimum standards.",
        "category": "accessibility"
    },
    {
        "id": "T&C-1",
        "title": "Terms and Conditions Requirements",
        "text": "T&C must clearly disclose terms, limitations, and conditions. No hidden fees allowed. Cancellation policies must be transparent. Payment terms must be clearly stated.",
        "category": "terms"
    },
    {
        "id": "GDPR-1",
        "title": "GDPR Compliance",
        "text": "Customer data processing must have lawful basis. Users have rights to access, rectify, and delete their data. Privacy policies must be transparent and accessible.",
        "category": "privacy"
    }
]

def get_policy_by_id(policy_id: str):
    """Retrieve a specific policy by ID."""
    for policy in POLICIES:
        if policy["id"] == policy_id:
            return policy
    return None

def get_policies_by_category(category: str):
    """Retrieve all policies in a category."""
    return [p for p in POLICIES if p.get("category") == category]

