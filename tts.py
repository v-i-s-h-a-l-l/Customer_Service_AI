# ==========================================================
# 🔊 SARVAM TEXT TO SPEECH (FINAL WORKING VERSION)
# Handles:
# ✅ Binary audio response
# ✅ Base64 audio JSON response
# Saves REAL playable WAV file
# ==========================================================

import requests
import base64
import os
from datetime import datetime

# ==========================================================
# CONFIG
# ==========================================================

SARVAM_API_KEY = "sk_s9c7y8bc_e1KNE0e5gEKmWYxCbx5BZTLk"
TTS_URL = "https://api.sarvam.ai/text-to-speech"

MODEL = "bulbul:v3"
CURRENT_VOICE = "Kavya"

AUDIO_DIR = "audio_outputs"
os.makedirs(AUDIO_DIR, exist_ok=True)


# ==========================================================
# VOICE SELECTION
# ==========================================================


def set_voice(gender: str):
    global CURRENT_VOICE

    if gender.lower() in ["1", "male"]:
        CURRENT_VOICE = "Aditya"
    else:
        CURRENT_VOICE = "Kavya"

    print(f"✅ Voice selected: {CURRENT_VOICE}")


# ==========================================================
# GENERATE FILE NAME
# ==========================================================


def generate_filename():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(AUDIO_DIR, f"response_{timestamp}.wav")


# ==========================================================
# SAVE AUDIO FROM SARVAM RESPONSE
# ==========================================================


def save_audio_from_response(response):
    content_type = response.headers.get("Content-Type", "")

    filepath = generate_filename()

    # ======================================================
    # CASE 1: DIRECT AUDIO RESPONSE
    # ======================================================
    if "audio" in content_type:
        with open(filepath, "wb") as f:
            f.write(response.content)

        print("✅ Direct audio received")
        return filepath

    # ======================================================
    # CASE 2: JSON WITH BASE64 AUDIO (MOST COMMON)
    # ======================================================
    data = response.json()

    if "audios" not in data:
        print("❌ Unexpected response:", data)
        return None

    audio_base64 = data["audios"][0]

    audio_bytes = base64.b64decode(audio_base64)

    with open(filepath, "wb") as f:
        f.write(audio_bytes)

    print("✅ Base64 audio decoded")

    return filepath


# ==========================================================
# TEXT → SPEECH MAIN FUNCTION
# ==========================================================


def speak(text: str):
    headers = {
        "Authorization": f"Bearer {SARVAM_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {"model": MODEL, "voice": CURRENT_VOICE, "text": text}

    response = requests.post(TTS_URL, headers=headers, json=payload, timeout=60)

    if response.status_code != 200:
        print("❌ TTS Error:", response.text)
        return None

    audio_path = save_audio_from_response(response)

    if audio_path:
        print(f"💾 Audio saved successfully:\n{audio_path}")

    return audio_path
