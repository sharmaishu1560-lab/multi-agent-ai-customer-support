import json
from datetime import datetime

LOG_FILE = "chat_logs.json"


def log_chat(session_id, intent, user_message, ai_response):

    print(">>> Logging started...")

    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "session_id": session_id,
        "intent": intent,
        "user_message": user_message,
        "ai_response": ai_response
    }

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as file:
            file.write(json.dumps(log_entry))
            file.write("\n")

        print(">>> Chat saved successfully")

    except Exception as e:
        print("Logging Error:", e)