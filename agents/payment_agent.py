from services.llm_service import client

def handle_payment_query(user_message):

    response = client.chat.completions.create(
        model="qwen2.5-coder-1.5b-instruct",
        temperature=0.3,
        messages=[
            {
                "role": "system",
                "content": """
You are a Payment Support Agent.

Your job is to help customers with:

- Payment failed
- Card declined
- UPI payment issues
- Debit/Credit card problems
- Double payment
- Payment pending
- Payment confirmation
- Transaction failed

Always reply politely and professionally.

If the customer has not provided enough information,
ask for:

- Order Number
- Transaction ID
- Payment Method (UPI, Card, Net Banking, etc.)

Try to help the customer as much as possible.
"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    return response.choices[0].message.content