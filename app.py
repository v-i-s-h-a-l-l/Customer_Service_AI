from fastapi import FastAPI
from rag_pipeline import run_rag

app = FastAPI()


@app.post("/chat")
def chat(query: str):
    response = run_rag(query)
    return {"response": response}
