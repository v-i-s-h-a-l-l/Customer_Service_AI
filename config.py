QDRANT_URL = (
    "https://34174987-f2f0-4dc3-ad57-b5dad19a0f38.eu-west-2-0.aws.cloud.qdrant.io"
)
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwiZXhwIjoxNzczNzM3MTU3fQ.o2j9i4M7TWyqFCtokDOKosiYw3_V2y2ISudwSckrJFE"
OPENAI_API_KEY = "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"
TAVILY_API_KEY = "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"
# Logical domains to Qdrant collection names.
# Add new domains here and reuse them across the codebase.
COLLECTIONS = {
    "ecommerce": "ecommerce",
    "car_booking": "car_booking",
}

# Default customer domain if none is explicitly provided.
DEFAULT_CUSTOMER_DOMAIN = "car_booking"

EMBEDDING_MODEL = "text-embedding-3-large"
LLM_MODEL = "gpt-4.1-nano"


def normalize_domain(domain: str) -> str:
    """
    Normalize a user-provided domain/customer_type into a safe collection key.
    Keeps it simple: lowercase + spaces to underscores.
    """
    return domain.strip().lower().replace(" ", "_")


def resolve_collection_name(domain: str | None) -> str:
    """
    Map a logical domain (e.g. 'ecommerce', 'car_booking') to a Qdrant collection.
    Falls back to DEFAULT_CUSTOMER_DOMAIN when domain is missing or unknown.
    """
    if not domain:
        domain = DEFAULT_CUSTOMER_DOMAIN

    domain = normalize_domain(domain)

    # If the domain isn't in the static mapping, treat the domain itself as the
    # collection name so runtime-created collections work without code changes.
    return COLLECTIONS.get(domain, domain)
