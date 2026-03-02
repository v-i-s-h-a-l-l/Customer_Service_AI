# ==========================================================
# 🎤 VOICE STREAM → GRAPH RAG → SAVE TTS AUDIO
# ==========================================================

from sarvam_streaming_stt import stream_audio_to_sarvam
from rag_pipeline import run_rag
from tts import speak, set_voice


# ==========================================================
# VOICE SELECTION
# ==========================================================


def choose_voice():
    print("\nSelect Assistant Voice")
    print("1 → Male")
    print("2 → Female")

    choice = input("Enter choice: ").strip().lower()

    if choice in ["1", "male"]:
        set_voice("male")
    else:
        set_voice("female")


# ==========================================================
# HANDLE USER QUERY
# ==========================================================


def handle_query(text):
    print("\n🚀 Running RAG...\n")

    try:
        response = run_rag(text)

        print("\n🤖 Assistant:")
        print(response)
        print("\n========================\n")

        # ✅ Save TTS audio response
        speak(response)

    except Exception as e:
        print("❌ Error during RAG execution:", str(e))


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    # Ask voice once
    choose_voice()

    print("\n🎤 Speak continuously (Ctrl+C to stop)\n")

    # Start streaming speech → RAG
    stream_audio_to_sarvam(handle_query)
