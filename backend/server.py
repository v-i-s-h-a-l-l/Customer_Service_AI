import os
import sys
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tempfile

# -----------------------------------------------------------
# Python path wiring so we can import existing pipeline files
# -----------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent  # c:/customer_service_application
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Import existing logic (DO NOT MODIFY these modules)
from rag_pipeline import run_rag
from tts import set_voice, speak, speak_bytes
import base64
from sarvam_streaming_stt import transcribe_chunk


app = FastAPI(title="Aurora Voice AI Backend")

# CORS so the Next.js frontend can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3002",
        "http://localhost:3003",
        "http://127.0.0.1:3003",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------- Pydantic models ----------------------


class QueryRequest(BaseModel):
    text: str
    user_id: str
    domain: str  # e.g. "restaurant", "ecommerce", "car_booking"


class QueryResponse(BaseModel):
    response: str
    audio_base64: str | None = None


class SetVoiceRequest(BaseModel):
    voice: str


class STTResponse(BaseModel):
    text: str


# ---------------------- Endpoints ----------------------


@app.post("/set-voice")
def set_voice_endpoint(body: SetVoiceRequest):
    """
    Set the Sarvam TTS voice.
    """
    try:
        set_voice(body.voice)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"set_voice failed: {e}")

    return {"status": "ok", "voice": body.voice}


@app.post("/query", response_model=QueryResponse)
def query_endpoint(body: QueryRequest):
    """
    Main text query endpoint.

    1. Calls run_rag(user_id, text, customer_type=domain)
    2. Passes the response text to Sarvam TTS (speak)
    3. Returns the text response to the frontend
    """
    try:
        result_text = run_rag(
            user_id=body.user_id,
            query=body.text,
            customer_type=body.domain,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"run_rag failed: {e}")

    # Generate TTS audio bytes and return as base64 to the browser
    audio_b64: str | None = None
    try:
        audio_bytes = speak_bytes(result_text)
        if audio_bytes:
            audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
    except Exception as e:
        print("TTS error:", e)

    return QueryResponse(response=result_text, audio_base64=audio_b64)


@app.post("/stt", response_model=STTResponse)
async def stt_endpoint(file: UploadFile = File(...)):
    """
    STT endpoint using your existing Sarvam pipeline.

    Frontend sends an audio chunk (e.g., webm / wav).
    We save to a temp file and call transcribe_chunk() from sarvam_streaming_stt.py
    """
    try:
        suffix = Path(file.filename or "audio").suffix or ".wav"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            data = await file.read()
            tmp.write(data)
            tmp_path = tmp.name

        text = transcribe_chunk(tmp_path)
    finally:
        try:
            if "tmp_path" in locals() and os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass

    return STTResponse(text=text or "")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.server:app", host="0.0.0.0", port=8001, reload=True)

