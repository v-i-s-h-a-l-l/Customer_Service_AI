from sarvamai import SarvamAI
import base64

# Initialize client
client = SarvamAI(api_subscription_key="sk_s9c7y8bc_e1KNE0e5gEKmWYxCbx5BZTLk")

# Sample text input
text = "Hello! Welcome to our AI assistant. How can I help you today?"

# Convert text to speech
response = client.text_to_speech.convert(
    text=text, target_language_code="en-IN", model="bulbul:v3", speaker="ritu"
)

# Decode base64 audio
audio_base64 = response.audios[0]
audio_bytes = base64.b64decode(audio_base64)

# Save audio file
with open("output.wav", "wb") as f:
    f.write(audio_bytes)

print("✅ Audio saved as output.wav")
