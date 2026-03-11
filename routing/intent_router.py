from openai import OpenAI
from config import OPENAI_API_KEY, LLM_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


ROUTER_PROMPT = """
You are an AI router.

Classify the user's message into one of these intents:

1. faq
   → questions about products, services, policies, information

2. booking
   → requests to make reservations or perform actions
   examples:
   - book a table
   - reserve a seat
   - schedule booking

Return ONLY one word:
faq or booking
"""


def detect_intent(query: str):
    response = client.chat.completions.create(
        model=LLM_MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": ROUTER_PROMPT},
            {"role": "user", "content": query},
        ],
    )

    intent = response.choices[0].message.content.strip().lower()

    if "booking" in intent:
        return "booking"

    return "faq"
