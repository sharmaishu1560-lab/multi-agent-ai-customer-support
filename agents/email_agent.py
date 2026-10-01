import time

from services.llm_service import client
from services.gmail_service import get_emails, search_emails


MODEL_NAME = "qwen2.5-coder-1.5b-instruct"


# ==================================================
# CREATE GMAIL SEARCH QUERY
# ==================================================

def create_gmail_query(user_message):

    message = user_message.lower().strip()

    if "email from " in message:
        person = message.split("email from ", 1)[1].strip()
        return f"from:{person}"

    if "emails from " in message:
        person = message.split("emails from ", 1)[1].strip()
        return f"from:{person}"

    if "subject:" in message:
        subject = message.split("subject:", 1)[1].strip()
        return f"subject:{subject}"

    if "about " in message:
        return message.split("about ", 1)[1].strip()

    if "regarding " in message:
        return message.split("regarding ", 1)[1].strip()

    if "related to " in message:
        return message.split("related to ", 1)[1].strip()

    return None


# ==================================================
# CHECK EMAIL LIST REQUEST
# ==================================================

def is_listing_request(user_message):

    message = user_message.lower().strip()

    has_email = (
        "email" in message
        or "emails" in message
    )

    has_show = (
        "show" in message
        or "list" in message
        or "display" in message
    )

    has_latest = (
        "latest" in message
        or "recent" in message
        or "newest" in message
    )

    return has_email and has_show and has_latest


# ==================================================
# FORMAT EMAIL LIST WITHOUT LLM
# ==================================================

def format_email_list(emails):

    result = (
        "[EMAIL AGENT]\n"
        "Here are your latest emails:\n\n"
    )

    for index, email in enumerate(emails, start=1):

        sender = email.get(
            "sender",
            "Unknown"
        )

        subject = email.get(
            "subject",
            "No subject"
        )

        date = email.get(
            "date",
            ""
        )

        result += (
            f"{index}. {subject}\n"
            f"   From: {sender}\n"
            f"   Date: {date}\n\n"
        )

    return result.strip()


# ==================================================
# EMAIL AGENT
# ==================================================

def handle_email_query(user_message):

    total_start = time.perf_counter()

    try:

        # ------------------------------------------
        # CREATE GMAIL QUERY
        # ------------------------------------------

        gmail_query = create_gmail_query(
            user_message
        )

        # ------------------------------------------
        # GET EMAILS
        # ------------------------------------------

        gmail_start = time.perf_counter()

        if gmail_query:

            print(
                f"Gmail Search Query: {gmail_query}"
            )

            emails = search_emails(
                gmail_query,
                max_results=5
            )

        else:

            print(
                "Getting latest emails..."
            )

            emails = get_emails(
                max_results=5
            )

        print(
            f"⏱️ Gmail Retrieval: "
            f"{time.perf_counter() - gmail_start:.2f} seconds"
        )

        # ------------------------------------------
        # NO EMAILS
        # ------------------------------------------

        if not emails:

            return (
                "[EMAIL AGENT] "
                "I couldn't find any emails."
            )

        print(
            f"Email Agent received "
            f"{len(emails)} emails."
        )

        # ------------------------------------------
        # DEBUG
        # ------------------------------------------

        print(
            "USER MESSAGE:",
            repr(user_message)
        )

        print(
            "IS LISTING REQUEST:",
            is_listing_request(user_message)
        )

        # ------------------------------------------
        # FAST LISTING PATH
        # ------------------------------------------

        if is_listing_request(user_message):

            print(
                "Email listing request - skipping LLM."
            )

            answer = format_email_list(
                emails
            )

            print(
                f"⏱️ Email Agent Internal Time: "
                f"{time.perf_counter() - total_start:.2f} seconds"
            )

            return answer

        # ------------------------------------------
        # BUILD VERY SMALL LLM CONTEXT
        # ------------------------------------------

        context_start = time.perf_counter()

        email_context = ""

        for index, email in enumerate(
            emails,
            start=1
        ):

            sender = email.get(
                "sender",
                "Unknown"
            )

            subject = email.get(
                "subject",
                "No subject"
            )

            date = email.get(
                "date",
                ""
            )

            message = email.get(
                "message",
                ""
            )

            # Only a small preview
            message = message[:100]

            email_context += (
                f"{index}. "
                f"{sender} | "
                f"{subject} | "
                f"{date} | "
                f"{message}\n"
            )

        print(
            f"⏱️ Email Context Creation: "
            f"{time.perf_counter() - context_start:.2f} seconds"
        )

        # ------------------------------------------
        # SHORT LLM PROMPT
        # ------------------------------------------

        prompt = f"""
You are an email assistant.

Start with [EMAIL AGENT].

User:
{user_message}

Emails:
{email_context}

Summarize the important information.
Use only the emails.
Do not invent facts.
Keep the answer very short.
"""

        # ------------------------------------------
        # LLM
        # ------------------------------------------

        llm_start = time.perf_counter()

        response = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=0.2,
            max_tokens=40,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        print(
            f"⏱️ Email LLM: "
            f"{time.perf_counter() - llm_start:.2f} seconds"
        )

        # ------------------------------------------
        # RESPONSE
        # ------------------------------------------

        answer = response.choices[0].message.content

        if answer:

            print(
                f"⏱️ Email Agent Internal Time: "
                f"{time.perf_counter() - total_start:.2f} seconds"
            )

            return answer.strip()

        return (
            "[EMAIL AGENT] "
            "Sorry, I couldn't generate a response."
        )

    except Exception as e:

        print(
            "Email Agent Error:",
            e
        )

        print(
            f"⏱️ Email Agent Failed Time: "
            f"{time.perf_counter() - total_start:.2f} seconds"
        )

        return (
            "[EMAIL AGENT] "
            "I was able to access your emails, "
            "but I couldn't generate the response."
        )