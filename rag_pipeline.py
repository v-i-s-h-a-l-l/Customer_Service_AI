from vector_store import search
from graph_layer import expand_graph
from llm import generate_answer
from config import DEFAULT_CUSTOMER_DOMAIN
from web_search import search_web
from routing.intent_router import detect_intent
from agents.booking_agent import run_booking_agent


# Good threshold for OpenAI embeddings
SIMILARITY_THRESHOLD = 0.20


def run_rag(user_id, query, customer_type: str | None = None):
    """
    Run the RAG pipeline.

    Steps:
    1. Intent detection
    2. Restaurant booking → Booking agent directly
    3. Otherwise → RAG pipeline
    """

    domain = customer_type or DEFAULT_CUSTOMER_DOMAIN

    # =====================================================
    # RESTAURANT MODE → SKIP RAG COMPLETELY
    # =====================================================

    if domain == "restaurant":
        print("🍽 Restaurant mode → Using booking agent (Skipping RAG + Tavily)")
        return run_booking_agent(user_id, query)

    # =====================================================
    # INTENT ROUTING
    # =====================================================

    intent = detect_intent(query)

    if intent == "booking":
        print("🚗 Booking intent detected → Using booking agent")
        return run_booking_agent(user_id, query)

    # =====================================================
    # NORMAL RAG PIPELINE
    # =====================================================

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

        best_score = max(best_score, score)

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
