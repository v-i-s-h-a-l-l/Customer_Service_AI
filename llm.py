from openai import OpenAI
from config import OPENAI_API_KEY, LLM_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

# 🔹 Simple in-memory session storage
# Structure:
# {
#   "user_id_1": [{"role": "user", "content": "..."},
#                 {"role": "assistant", "content": "..."}],
#   "user_id_2": [...]
# }
conversation_sessions = {}

# Limit number of turns to prevent token overflow
MAX_TURNS = 10


SYSTEM_PROMPT = """
You are a multilingual eCommerce customer support assistant.

Rules:
- Answer politely and clearly.
- Reply in the same language as the question.
- Understand the emotion of the customer and respond empathetically.
- Behave like a real human customer support agent.
- Use the provided context to answer.
- If answer is not in context, say you are not sure instead of hallucinating.
"""


def generate_answer(user_id, query, context_docs):
    # 🔹 Create session if not exists
    if user_id not in conversation_sessions:
        conversation_sessions[user_id] = []

    # 🔹 Prepare RAG context
    context = "\n".join(context_docs[:5])

    # 🔹 Build messages list
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Add previous history
    messages.extend(conversation_sessions[user_id])

    # Add current query with context
    messages.append(
        {
            "role": "user",
            "content": f"""
Context:
{context}

Customer Question:
{query}
""",
        }
    )

    # 🔹 Call LLM
    response = client.chat.completions.create(
        model=LLM_MODEL, messages=messages, temperature=0.3
    )

    answer = response.choices[0].message.content

    # 🔹 Save conversation
    conversation_sessions[user_id].append({"role": "user", "content": query})

    conversation_sessions[user_id].append({"role": "assistant", "content": answer})

    # 🔹 Trim memory (keep last MAX_TURNS turns)
    if len(conversation_sessions[user_id]) > MAX_TURNS * 2:
        conversation_sessions[user_id] = conversation_sessions[user_id][
            -MAX_TURNS * 2 :
        ]

    return answer
