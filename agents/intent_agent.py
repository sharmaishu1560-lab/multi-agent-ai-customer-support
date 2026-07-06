from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)

def detect_intent(user_message):

    response = client.chat.completions.create(
        model="qwen2.5-coder-1.5b-instruct",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": """
You are an intent classifier.

Choose ONLY ONE intent from this list:

- order
- refund
- payment
- technical_support
- general

Return only the intent name.
"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    return response.choices[0].message.content.strip()