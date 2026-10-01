import time
from openai import OpenAI
from services.llm_service import client as service_client

MODEL_NAME = "qwen2.5-coder-1.5b-instruct"

messages = [
    {
        "role": "system",
        "content": """
You are a concise payment support assistant.
Start with [PAYMENT AGENT].
Give a short, helpful answer.
Never request passwords, OTPs, CVV, full card numbers, or UPI PINs.
"""
    },
    {
        "role": "user",
        "content": "My payment was deducted but my order failed. What should I do?"
    }
]


def test_client(name, client):
    start = time.perf_counter()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.3,
        max_tokens=100,
        stream=False,
        messages=messages
    )

    elapsed = time.perf_counter() - start
    answer = response.choices[0].message.content

    print(f"\n{name}")
    print(f"Time: {elapsed:.2f} seconds")
    print(f"Characters: {len(answer)}")


# Fresh client
fresh_client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)

test_client("FRESH CLIENT", fresh_client)

# services.llm_service client
test_client("SERVICE CLIENT", service_client)