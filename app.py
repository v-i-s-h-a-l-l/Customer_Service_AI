from fastapi import FastAPI
from pydantic import BaseModel
from rag_pipeline import run_rag
from collections_api import router as collections_router

app = FastAPI()
app.include_router(collections_router)


class ChatRequest(BaseModel):
    user_id: str
    query: str
    customer_type: str | None = None  # e.g. "ecommerce" or "car_booking"


@app.post("/chat")
def chat(payload: ChatRequest):
    response = run_rag(
        user_id=payload.user_id,
        query=payload.query,
        customer_type=payload.customer_type,
    )
    return {"response": response}
