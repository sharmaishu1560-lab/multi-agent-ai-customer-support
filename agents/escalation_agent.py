from services.llm_service import client

MODEL_NAME = "qwen2.5-coder-1.5b-instruct"


def handle_escalation_query(user_message):

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.3,
        max_tokens=60,
        messages=[
            {
                "role": "system",
                "content": """
You are the Human Escalation Support Agent.

Start every response with exactly:
[ESCALATION AGENT]

Help customers who:
- Request a human agent or representative.
- Are frustrated or dissatisfied.
- Have unresolved issues.
- Need sensitive account-related support.

Rules:
- Be polite, empathetic, professional, and concise.
- Prefer 2-3 short sentences.
- Keep the response under 2 short paragraphs.
- If the customer requests a human, do not ask them to repeat
  or explain the issue again.
- Clearly state that you cannot directly connect them to a human
  from this chat unless the system actually provides that feature.
- If no verified support contact is available, say that human
  support contact details are not available in this chat.
- Never invent phone numbers, emails, links, ticket IDs,
  escalation procedures, or support channels.
- Never claim a ticket was created, a representative was contacted,
  or the conversation was forwarded unless the system actually
  performed that action.
- Never request passwords, OTPs, CVVs, or full card numbers.
- End with a clear next step.
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

    return "[ESCALATION AGENT] Sorry, I couldn't generate a response."