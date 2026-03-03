from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from config import QDRANT_URL, QDRANT_API_KEY

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, check_compatibility=False)

client.recreate_collection(
    collection_name="car_booking",
    vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
)

print("✅ car_booking collection created successfully.")
