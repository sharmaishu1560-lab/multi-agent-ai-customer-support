import time

from services.llm_service import client

MODEL_NAME = "qwen2.5-coder-1.5b-instruct"

start = time.perf_counter()

response = client.chat.completions.create(
    model=MODEL_NAME,
    temperature=0.3,
    max_tokens=100,
    stream=False,
    messages=[
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
)

answer = response.choices[0].message.content

end = time.perf_counter()

print(answer)
print("\n----- TIMING -----")
print(f"Total response time: {end - start:.2f} seconds")
print(f"Characters generated: {len(answer)}")
