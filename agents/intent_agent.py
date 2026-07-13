from services.llm_service import client


def detect_intent(user_message):

    response = client.chat.completions.create(
        model="qwen2.5-coder-1.5b-instruct",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": """
You are an intent classification AI.

Classify the user's message into EXACTLY ONE of these intents:

- order
- refund
- payment
- technical_support
- faq
- escalation
- general

FAQ includes:
- warranty
- return policy
- refund policy
- shipping policy
- business hours
- contact information
- company information

Escalation includes:
- talk to a human
- speak to an agent
- customer representative
- manager
- complaint
- not satisfied
- unresolved issue

IMPORTANT:
Return ONLY one word.

Valid outputs are:

order
refund
payment
technical_support
faq
escalation
general

Do not return anything else.
"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    intent = response.choices[0].message.content.strip().lower()

    print("RAW MODEL OUTPUT:", intent)

    return intent