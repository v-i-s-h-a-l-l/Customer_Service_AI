from sarvam_streaming_stt import stream_audio_to_sarvam
from rag_pipeline import run_rag


def handle_query(text):
    print("\n🚀 Running RAG...\n")

    response = run_rag(text)

    print("\n🤖 Assistant:")
    print(response)
    print("\n========================\n")


if __name__ == "__main__":
    stream_audio_to_sarvam(handle_query)
