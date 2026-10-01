from services.llm_service import client

MODEL_NAME = "qwen2.5-coder-1.5b-instruct"


def handle_order_query(history):

    print("Conversation History:")
    print(history)

    print("History messages:", len(history))
    print("History characters:", sum(len(str(msg.get("content", ""))) for msg in history))

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.3,
        max_tokens=60,
        messages=[
            {
                "role": "system",
                "content": """
You are the Order Support Agent.

Start every response with exactly:
[ORDER AGENT]

Help with order tracking, delivery status, delayed orders,
and order-related questions.

Rules:
- Be polite, professional, and concise.
- Prefer 2-3 short sentences.
- Keep the response under 2 short paragraphs.
- Do not repeat the customer's problem.
- Never invent order status or tracking information.
- If live tracking is unavailable, explain how the customer
  can check it.
- Read the conversation history before answering.
- If an order number was already provided, do not ask for it again.
- Ask for an order number only if it has never been provided.
- Use previous messages when answering follow-up questions.
- Never ignore relevant conversation history.
- End with one clear next step.
"""
            }
        ] + history
    )

    answer = response.choices[0].message.content

    if answer:
        return answer.strip()

    return "[ORDER AGENT] Sorry, I couldn't generate a response."