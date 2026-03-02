import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from config import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME
from embeddings import embed_text


# ==============================
# 🚀 QDRANT CLIENT INIT
# ==============================

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    check_compatibility=False,  # avoids version warning
)


# ==============================
# 🧠 CREATE COLLECTION
# ==============================


def create_collection():
    """
    Creates (or recreates) the ecommerce collection.
    OpenAI text-embedding-3-large → 3072 dimensions
    """
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
    )
    print("Collection created successfully.")


# ==============================
# 📥 INSERT DOCUMENT
# ==============================


def insert_document(text: str, metadata: dict):
    """
    Inserts document into Qdrant with embedding + metadata
    """
    vector = embed_text(text)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=str(uuid.uuid4()), vector=vector, payload={"text": text, **metadata}
            )
        ],
    )

    print("Document inserted successfully.")


# ==============================
# 🔍 SEARCH (NEW API)
# ==============================


def search(query: str, limit: int = 5):
    """
    Searches Qdrant using new query_points() API
    Returns list of points
    """
    query_vector = embed_text(query)

    results = client.query_points(
        collection_name=COLLECTION_NAME, query=query_vector, limit=limit
    )
    print(QDRANT_URL)

    # Safe handling
    if results and hasattr(results, "points"):
        return results.points

    return []
