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
- email
- general


ORDER includes:

- order status
- track my order
- where is my order
- delivery status
- shipping my order
- when will my order arrive


REFUND includes:

- I want a refund
- refund my order
- get my money back
- request a refund
- refund status


PAYMENT includes:

- payment failed
- payment issue
- billing problem
- payment not working
- charged incorrectly


TECHNICAL SUPPORT includes:

- technical problem
- application not working
- website not working
- login problem
- technical issue


FAQ includes:

- warranty
- return policy
- refund policy
- shipping policy
- business hours
- contact information
- company information


ESCALATION includes:

- talk to a human
- speak to an agent
- customer representative
- manager
- complaint
- not satisfied
- unresolved issue


EMAIL includes:

- show my emails
- show my latest emails
- check my emails
- read my emails
- what emails did I receive
- latest email
- recent email
- summarize my email
- summarize my latest email
- find an email
- search my emails
- do I have an email from someone
- email from a person
- emails about a topic
- check my Gmail
- read my Gmail
- Gmail messages


IMPORTANT:

Return ONLY one word.

Valid outputs are:

order
refund
payment
technical_support
faq
escalation
email
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