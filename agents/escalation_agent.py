from services.llm_service import client


def handle_escalation_query(user_message):

    response = client.chat.completions.create(
        model="qwen2.5-coder-1.5b-instruct",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": """
You are a Human Escalation Agent.

Your job is to determine whether the customer should be transferred to a human support representative.

Escalate when:
- The customer requests a human agent.
- The issue cannot be resolved by AI.
- The customer is unhappy or frustrated.
- The customer has complained multiple times.
- The issue requires account verification or sensitive information.

Always respond politely.

If escalation is required, clearly tell the customer that the conversation has been forwarded to a human support representative.
"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    return response.choices[0].message.content