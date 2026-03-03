from vector_store import search
from graph_layer import expand_graph
from llm import generate_answer


def run_rag(user_id, query):
    results = search(query)

    docs = []

    for r in results:
        payload = r.payload
        docs.append(payload["text"])

        if "product_id" in payload:
            neighbors = expand_graph(payload["product_id"])
            docs.extend(neighbors)

    return generate_answer(user_id, query, docs)
