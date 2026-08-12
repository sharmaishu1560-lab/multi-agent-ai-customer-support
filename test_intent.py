from agents.intent_agent import detect_intent


questions = [
    "Show me my latest emails",
    "Check my Gmail",
    "Do I have any new emails?",
    "Where is my order?",
    "I want a refund",
    "My payment failed",
    "What is your warranty policy?"
]


for question in questions:

    intent = detect_intent(question)

    print(
        f"Question: {question}"
    )

    print(
        f"Intent: {intent}"
    )

    print("-" * 50)