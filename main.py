import os
import time

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# -----------------------------------
# Initialize FastAPI
# -----------------------------------

app = FastAPI(
    title="Multi-Agent AI Customer Support Assistant"
)


# -----------------------------------
# Create Audio Directory
# -----------------------------------

AUDIO_DIRECTORY = "static/audio"

os.makedirs(
    AUDIO_DIRECTORY,
    exist_ok=True
)


# -----------------------------------
# Mount Frontend
# -----------------------------------

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# -----------------------------------
# Mount Audio Files
# -----------------------------------

app.mount(
    "/audio",
    StaticFiles(directory=AUDIO_DIRECTORY),
    name="audio"
)


# -----------------------------------
# Import Services
# -----------------------------------

from services.llm_service import client

from services.memory_service import (
    save_message,
    get_history
)

from services.logging_service import log_chat


# -----------------------------------
# Import Voice Service
# -----------------------------------

from services.voice_service import text_to_speech


# -----------------------------------
# Import Agents
# -----------------------------------

from agents.intent_agent import detect_intent

from agents.order_agent import handle_order_query

from agents.refund_agent import handle_refund_query

from agents.payment_agent import handle_payment_query

from agents.technical_support_agent import (
    handle_technical_support_query
)

from agents.faq_agent import handle_faq_query

from agents.escalation_agent import (
    handle_escalation_query
)

from agents.email_agent import handle_email_query


# -----------------------------------
# Request Model
# -----------------------------------

from pydantic import BaseModel


class ChatRequest(BaseModel):

    session_id: str

    message: str

    # Voice is OFF by default.
    voice_enabled: bool = False


# -----------------------------------
# Root Endpoint
# -----------------------------------

@app.get("/")
def home():

    return {
        "message": (
            "Multi-Agent AI Customer Support Assistant"
        )
    }


# -----------------------------------
# Chat Endpoint
# -----------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    # Start total timer

    total_start = time.perf_counter()

    try:

        # -----------------------------------
        # Save User Message
        # -----------------------------------

        step_start = time.perf_counter()

        save_message(
            request.session_id,
            "user",
            request.message
        )

        print(
            f"⏱️ Save User Message: "
            f"{time.perf_counter() - step_start:.2f} seconds"
        )


        # -----------------------------------
        # Get Conversation History
        # -----------------------------------

        step_start = time.perf_counter()

        history = get_history(
            request.session_id
        )

        print(
            f"⏱️ Get History: "
            f"{time.perf_counter() - step_start:.2f} seconds"
        )


        # -----------------------------------
        # Detect Intent
        # -----------------------------------

        intent_start = time.perf_counter()

        intent = detect_intent(
            request.message
        )

        print(
            f"⏱️ Intent Detection: "
            f"{time.perf_counter() - intent_start:.2f} seconds"
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

        agent_start = time.perf_counter()


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

            answer = (
                response
                .choices[0]
                .message
                .content
            )


        print(
            f"⏱️ Agent/LLM Processing: "
            f"{time.perf_counter() - agent_start:.2f} seconds"
        )


        # -----------------------------------
        # Voice Response
        # -----------------------------------

        audio_file = None


        if request.voice_enabled:

            print(
                "🔊 Voice response requested."
            )

            voice_start = time.perf_counter()

            try:

                # Create unique filename

                filename = (
                    f"response_"
                    f"{request.session_id}_"
                    f"{int(time.time() * 1000)}.mp3"
                )

                audio_path = os.path.join(
                    AUDIO_DIRECTORY,
                    filename
                )


                # Generate speech

                generated_file = text_to_speech(
                    text=answer,
                    output_file=audio_path
                )


                if generated_file:

                    audio_file = (
                        f"/audio/{filename}"
                    )

                    print(
                        f"🔊 Audio file: "
                        f"{audio_file}"
                    )

                else:

                    print(
                        "⚠️ Voice generation failed. "
                        "Continuing with text response."
                    )


            except Exception as voice_error:

                print(
                    "⚠️ Voice Error:",
                    voice_error
                )

                print(
                    "Continuing with text response."
                )


            print(
                f"⏱️ Voice Processing: "
                f"{time.perf_counter() - voice_start:.2f} seconds"
            )

        else:

            print(
                "🔇 Voice disabled for this request."
            )


        # -----------------------------------
        # Save Assistant Response
        # -----------------------------------

        step_start = time.perf_counter()

        save_message(
            request.session_id,
            "assistant",
            answer
        )

        print(
            f"⏱️ Save Assistant Message: "
            f"{time.perf_counter() - step_start:.2f} seconds"
        )


        # -----------------------------------
        # Log Conversation
        # -----------------------------------

        step_start = time.perf_counter()

        log_chat(
            request.session_id,
            intent,
            request.message,
            answer
        )

        print(
            f"⏱️ Log Conversation: "
            f"{time.perf_counter() - step_start:.2f} seconds"
        )


        # -----------------------------------
        # Get Updated History
        # -----------------------------------

        step_start = time.perf_counter()

        updated_history = get_history(
            request.session_id
        )

        print(
            f"⏱️ Get Updated History: "
            f"{time.perf_counter() - step_start:.2f} seconds"
        )


        # -----------------------------------
        # Total Time
        # -----------------------------------

        print(
            f"⏱️ TOTAL CHAT TIME: "
            f"{time.perf_counter() - total_start:.2f} seconds"
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

            "audio_file": audio_file,

            "voice_enabled": request.voice_enabled,

            "conversation_history": updated_history
        }


    except Exception as e:

        print(
            "Application Error:",
            e
        )

        print(
            f"⏱️ FAILED CHAT TIME: "
            f"{time.perf_counter() - total_start:.2f} seconds"
        )

        return {

            "status": "error",

            "message": (
                "Unable to process your request."
            ),

            "details": str(e)
        }