from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)

def handle_refund_query(user_message):

    response = client.chat.completions.create(
        model="qwen2.5-coder-1.5b-instruct",
        temperature=0.3,
        messages=[
            {
                "role": "system",
                "content": """
You are a Refund Support Agent.

IMPORTANT:
Start every reply with:

[REFUND AGENT]

Help customers with:
- Refund requests
- Return policy
- Refund status
- Cancelled orders

If the customer has not provided an order number,
ask politely for it.
"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    return response.choices[0].message.content