from services.llm_service import client

MODEL_NAME = "qwen2.5-coder-1.5b-instruct"


def handle_refund_query(user_message):

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.3,
        max_tokens=60,
        messages=[
            {
                "role": "system",
                "content": """
                
You are the Refund Support Agent.

Start every response with:
[REFUND AGENT]

Help with refunds, returns, damaged products, incorrect products,
and cancelled orders.

Be polite and concise.
Use 2-3 short sentences.
If an order number is missing, ask for it.
Never claim a refund was processed unless the system confirms it.
Never invent company policies or refund timelines.
Never request passwords, OTPs, CVVs, or full card details.
End with one clear next step.
"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    answer = response.choices[0].message.content

    if answer:
        return answer.strip()

    return "[REFUND AGENT] Sorry, I couldn't generate a response."