# ==========================================================
# 🔥 CROSS-ENCODER RERANKER
# ==========================================================

from sentence_transformers import CrossEncoder

# ==========================================================
# 🚀 LOAD RERANK MODEL
# ==========================================================
# Excellent multilingual reranker
# Small + fast + strong accuracy

RERANK_MODEL_NAME = "BAAI/bge-reranker-base"

print("Loading reranker model...")

reranker = CrossEncoder(RERANK_MODEL_NAME)

print("✅ Reranker Loaded")


# ==========================================================
# 🔄 RERANK FUNCTION
# ==========================================================


def rerank_documents(query: str, documents: list, top_k: int = 5):
    """
    Reranks retrieved documents using cross-encoder.

    Args:
        query (str): user query
        documents (list): retrieved texts
        top_k (int): number of final docs

    Returns:
        list: reranked top documents
    """

    if not documents:
        return []

    # Create query-document pairs
    pairs = [(query, doc) for doc in documents]

    # Compute relevance scores
    scores = reranker.predict(pairs)

    # Combine doc + score
    scored_docs = list(zip(documents, scores))

    # Sort by relevance
    scored_docs.sort(key=lambda x: x[1], reverse=True)

    # Select top-k
    reranked_docs = [doc for doc, _ in scored_docs[:top_k]]

    return reranked_docs


# ==========================================================
# OPTIONAL DEBUG FUNCTION
# ==========================================================


def rerank_with_scores(query: str, documents: list):
    """
    Returns documents with scores (debugging)
    """

    pairs = [(query, doc) for doc in documents]
    scores = reranker.predict(pairs)

    scored_docs = list(zip(documents, scores))
    scored_docs.sort(key=lambda x: x[1], reverse=True)

    return scored_docs
