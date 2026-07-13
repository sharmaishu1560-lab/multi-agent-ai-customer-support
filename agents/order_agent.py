from services.llm_service import client

def handle_order_query(history):
    print("Conversation History:")
    print(history)
    response = client.chat.completions.create(
        model="qwen2.5-coder-1.5b-instruct",
        temperature=0.3,
    messages=[
    {
        "role": "system",
        "content": """
You are an Order Support Agent.

IMPORTANT:
Read the entire conversation history before answering.

If the customer has already provided an order number anywhere in the conversation, do NOT ask for it again.

Use the conversation history to answer follow-up questions naturally.

Only ask for an order number if it has never been mentioned.

Never ignore previous messages.

Always answer politely and professionally.
"""
    }
] + history)

    return response.choices[0].message.content