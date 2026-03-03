import pdfplumber
from vector_store import client
from embeddings import embed_text
from qdrant_client.models import PointStruct
import uuid


COLLECTION_NAME = "car_booking"


def insert_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        full_text = ""

        for page in pdf.pages:
            full_text += page.extract_text() + "\n"

    vector = embed_text(full_text)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={"text": full_text, "domain": "car_booking"},
            )
        ],
    )

    print(f"✅ Inserted {file_path} into car_booking collection")


if __name__ == "__main__":
    # insert_pdf("car_booking_policy_mahindra.pdf")
    # insert_pdf("cancellation_rules_mahindra.pdf")
    insert_pdf("Car details.pdf")
