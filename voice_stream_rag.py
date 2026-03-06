from sarvam_streaming_stt import stream_audio_to_sarvam
from rag_pipeline import run_rag
from tts import speak, set_voice
import uuid


# ==========================================================
# USER SESSION (Generate at Runtime)
# ==========================================================

USER_ID = str(uuid.uuid4())
CUSTOMER_TYPE: str | None = None  # "ecommerce" or "car_booking"

print(f"🆔 Session ID: {USER_ID}")


# ==========================================================
# VOICE & CUSTOMER TYPE SELECTION
# ==========================================================


def choose_voice():
    print("\nSelect Assistant Voice")
    print("1 → Male")
    print("2 → Female")

    choice = input("Enter choice: ").strip().lower()

    if choice in ["1", "male", "m"]:
        set_voice("male")
    else:
        set_voice("female")


def choose_customer_type():
    """
    Ask the user which type of customer they are and
    set the global CUSTOMER_TYPE accordingly.
    """
    global CUSTOMER_TYPE

    print("\nSelect Customer Type")
    print("1 → ecommerce")
    print("2 → car_booking")

    choice = input("Enter choice: ").strip().lower()

    if choice in ["1", "ecommerce", "e"]:
        CUSTOMER_TYPE = "ecommerce"
    else:
        CUSTOMER_TYPE = "car_booking"

    print(f"✅ Using '{CUSTOMER_TYPE}' collection for this session.")


# ==========================================================
# HANDLE USER QUERY
# ==========================================================


def handle_query(text: str):
    print("\n🚀 Running RAG...\n")

    try:
        # Pass user_id and selected customer_type/domain
        response = run_rag(USER_ID, text, customer_type=CUSTOMER_TYPE)

        print("\n🤖 Assistant:")
        print(response)
        print("\n========================\n")

        # Save TTS audio response
        speak(response)

    except Exception as e:
        print("❌ Error during RAG execution:", str(e))


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    print("\n🎤 Voice RAG Session\n")
    choose_voice()
    choose_customer_type()

    print("\n🎤 Speak continuously (Ctrl+C to stop)\n")

    # Start streaming speech → RAG
    stream_audio_to_sarvam(handle_query)

