from vector_store import search
from graph_layer import expand_graph
from llm import generate_answer
from config import DEFAULT_CUSTOMER_DOMAIN
from web_search import search_web


# Good threshold for OpenAI embeddings
SIMILARITY_THRESHOLD = 0.35


def run_rag(user_id, query, customer_type: str | None = None):
    """
    Run the RAG pipeline.

    Steps:
    1. Vector search (Qdrant / Cache)
    2. Graph expansion
    3. If retrieval weak → Tavily web search
    4. LLM generates final answer
    """

    domain = customer_type or DEFAULT_CUSTOMER_DOMAIN

    print("\n🚀 Running RAG...")

    # ==========================================
    # VECTOR SEARCH
    # ==========================================

    results = search(query, domain=domain)

    docs = []
    best_score = 0.0

    # ==========================================
    # PROCESS VECTOR RESULTS
    # ==========================================

    for r in results:
        payload = r.get("payload", {})
        score = r.get("score", 0.0)

        # Track best similarity score
        best_score = max(best_score, score)

        # Extract main document text
        if "text" in payload:
            docs.append(payload["text"])

        # ======================================
        # GRAPH EXPANSION
        # ======================================

        if "product_id" in payload:
            neighbors = expand_graph(payload["product_id"])
            docs.extend(neighbors)

    print(f"🔎 Best similarity score: {best_score:.3f}")

    # ==========================================
    # TAVILY FALLBACK
    # ==========================================

    if len(results) == 0 or best_score < SIMILARITY_THRESHOLD:
        print("🌐 Weak or no RAG results → Using Tavily web search")

        try:
            web_results = search_web(query)

            for result in web_results:
                docs.append(result)

        except Exception as e:
            print("❌ Tavily search failed:", str(e))

    else:
        print("✅ Using RAG knowledge base")

    # ==========================================
    # GENERATE FINAL ANSWER
    # ==========================================

    return generate_answer(user_id, query, docs)
