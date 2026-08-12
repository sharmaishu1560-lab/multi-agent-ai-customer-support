from fastapi import FastAPI
from pydantic import BaseModel

from services.llm_service import client
from services.memory_service import save_message, get_history
from services.logging_service import log_chat

from agents.intent_agent import detect_intent
from agents.order_agent import handle_order_query
from agents.refund_agent import handle_refund_query
from agents.payment_agent import handle_payment_query
from agents.technical_support_agent import handle_technical_support_query
from agents.faq_agent import handle_faq_query
from agents.escalation_agent import handle_escalation_query
from agents.email_agent import handle_email_query


# -----------------------------------
# Create FastAPI Application
# -----------------------------------

app = FastAPI(
    title="Multi-Agent AI Customer Support Assistant",
    description="AI-powered customer support system using multiple specialized agents.",
    version="1.0.0"
)


# -----------------------------------
# Request Model
# -----------------------------------

class ChatRequest(BaseModel):

    session_id: str
    message: str


# -----------------------------------
# Home Endpoint
# -----------------------------------

@app.get("/")
def home():

    return {
        "message": "Multi-Agent AI Customer Support Assistant",
        "status": "running"
    }


# -----------------------------------
# Chat Endpoint
# -----------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    try:

        # -----------------------------------
        # Save User Message
        # -----------------------------------

        save_message(
            request.session_id,
            "user",
            request.message
        )


        # -----------------------------------
        # Get Conversation History
        # -----------------------------------

        history = get_history(
            request.session_id
        )


        # -----------------------------------
        # Detect Intent
        # -----------------------------------

        intent = detect_intent(
            request.message
        )


        # -----------------------------------
        # Intent Mapping
        # -----------------------------------

        intent_mapping = {

            # FAQ
            "warranty": "faq",
            "shipping": "faq",
            "shipping policy": "faq",
            "refund policy": "faq",
            "business hours": "faq",
            "contact": "faq",
            "company information": "faq",

            # Order
            "order_status": "order",
            "tracking": "order",
            "delivery": "order",
            "order_cancellation": "order",
            "cancel_order": "order",

            # Refund
            "refund": "refund",
            "refund_request": "refund",

            # Payment
            "payment_issue": "payment",
            "billing": "payment",
            "payment": "payment",

            # Technical Support
            "tech_support": "technical_support",
            "technical": "technical_support",
            "technical_support": "technical_support",

            # Escalation
            "human": "escalation",
            "human agent": "escalation",
            "agent": "escalation",
            "representative": "escalation",
            "customer support": "escalation",
            "manager": "escalation",
            "complaint": "escalation",
            "not satisfied": "escalation",
            "unresolved": "escalation",

            # Email
            "email": "email"
        }


        # -----------------------------------
        # Convert Intent
        # -----------------------------------

        intent = intent_mapping.get(
            intent,
            intent
        )

        print(
            f"Detected Intent: {intent}"
        )


        # -----------------------------------
        # Route Request
        # -----------------------------------

        if intent == "order":

            answer = handle_order_query(
                history
            )


        elif intent == "refund":

            answer = handle_refund_query(
                request.message
            )


        elif intent == "payment":

            answer = handle_payment_query(
                request.message
            )


        elif intent == "technical_support":

            answer = handle_technical_support_query(
                request.message
            )


        elif intent == "faq":

            answer = handle_faq_query(
                request.message
            )


        elif intent == "escalation":

            answer = handle_escalation_query(
                request.message
            )


        elif intent == "email":

            answer = handle_email_query(
                request.message
            )


        else:

            # -----------------------------------
            # General AI Response
            # -----------------------------------

            response = client.chat.completions.create(

                model="qwen2.5-coder-1.5b-instruct",

                temperature=0.7,

                messages=[

                    {
                        "role": "system",
                        "content": (
                            "You are a helpful AI customer "
                            "support assistant."
                        )
                    }

                ] + history
            )

            answer = response.choices[0].message.content


        # -----------------------------------
        # Save Assistant Response
        # -----------------------------------

        save_message(
            request.session_id,
            "assistant",
            answer
        )


        # -----------------------------------
        # Log Conversation
        # -----------------------------------

        log_chat(
            request.session_id,
            intent,
            request.message,
            answer
        )


        # -----------------------------------
        # Get Updated History
        # -----------------------------------

        updated_history = get_history(
            request.session_id
        )


        # -----------------------------------
        # Return Response
        # -----------------------------------

        return {

            "status": "success",

            "session_id": request.session_id,

            "detected_intent": intent,

            "user_message": request.message,

            "ai_response": answer,

            "conversation_history": updated_history
        }


    except Exception as e:

        print(
            "Application Error:",
            e
        )

        return {

            "status": "error",

            "message": "Unable to process your request.",

            "details": str(e)
        }