from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

from agents.intent_agent import detect_intent
from agents.order_agent import handle_order_query
from agents.refund_agent import handle_refund_query

app = FastAPI()

# Connect to LM Studio
client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "message": "Multi-Agent AI Customer Support Assistant"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    # Step 1: Detect the user's intent
    intent = detect_intent(request.message)

    print(f"Detected Intent: {intent}")

    # Step 2: Route the request to the correct AI agent
    if intent == "order":
        answer = handle_order_query(request.message)

    elif intent == "refund":
        answer = handle_refund_query(request.message)

    else:
        response = client.chat.completions.create(
            model="qwen2.5-coder-1.5b-instruct",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI customer support assistant."
                },
                {
                    "role": "user",
                    "content": request.message
                }
            ],
            temperature=0.7
        )

        answer = response.choices[0].message.content

    # Step 3: Return the response
    return {
        "user_message": request.message,
        "ai_response": answer
    }