from openai import OpenAI
from config import OPENAI_API_KEY, LLM_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_answer(query, context_docs):
    context = "\n".join(context_docs[:5])

    prompt = f"""
You are a multilingual eCommerce customer support assistant.
Answer politely and clearly.
Answer in the same language as the question.
try to understand the emotion of the person and respond accordinly instead of giving similar tone responses.
try to behave like a human customer support and not like ai


Context:
{context}

Question:
{query}
"""

    response = client.chat.completions.create(
        model=LLM_MODEL, messages=[{"role": "user", "content": prompt}], temperature=0.3
    )

    return response.choices[0].message.content
