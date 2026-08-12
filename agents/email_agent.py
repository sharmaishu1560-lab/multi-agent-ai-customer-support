from services.llm_service import client
from services.gmail_service import get_emails, search_emails


# ==================================================
# CREATE GMAIL SEARCH QUERY
# ==================================================

def create_gmail_query(user_message):

    message = user_message.lower().strip()

    # ------------------------------------------
    # Search by sender
    # ------------------------------------------

    if "email from " in message:

        person = message.split(
            "email from ",
            1
        )[1].strip()

        return f"from:{person}"

    if "emails from " in message:

        person = message.split(
            "emails from ",
            1
        )[1].strip()

        return f"from:{person}"

    # ------------------------------------------
    # Search by subject
    # ------------------------------------------

    if "subject:" in message:

        subject = message.split(
            "subject:",
            1
        )[1].strip()

        return f"subject:{subject}"

    # ------------------------------------------
    # Search by topic
    # ------------------------------------------

    if "about " in message:

        topic = message.split(
            "about ",
            1
        )[1].strip()

        return topic

    if "regarding " in message:

        topic = message.split(
            "regarding ",
            1
        )[1].strip()

        return topic

    if "related to " in message:

        topic = message.split(
            "related to ",
            1
        )[1].strip()

        return topic

    # ------------------------------------------
    # No Gmail search
    # ------------------------------------------

    return None


# ==================================================
# EMAIL AGENT
# ==================================================

def handle_email_query(user_message):

    try:

        # ------------------------------------------
        # Create Gmail search query
        # ------------------------------------------

        gmail_query = create_gmail_query(
            user_message
        )

        # ------------------------------------------
        # If there is a specific search
        # ------------------------------------------

        if gmail_query:

            print(
                f"Gmail Search Query: {gmail_query}"
            )

            emails = search_emails(
                gmail_query,
                max_results=5
            )

        # ------------------------------------------
        # Otherwise get latest emails
        # ------------------------------------------

        else:

            print(
                "Getting latest emails..."
            )

            emails = get_emails(
                max_results=5
            )

        # ------------------------------------------
        # Check emails
        # ------------------------------------------

        if not emails:

            return (
                "I couldn't find any emails."
            )

        print(
            f"Email Agent received "
            f"{len(emails)} emails."
        )

        # ------------------------------------------
        # Build small email context
        # ------------------------------------------

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

            # Keep context small
            message = message[:500]

            email_context += f"""
EMAIL {index}

From: {sender}

Subject: {subject}

Date: {date}

Content:
{message}

--------------------------------
"""

        # ------------------------------------------
        # LLM prompt
        # ------------------------------------------

        prompt = f"""
You are a helpful email assistant.

User request:
{user_message}

Here are the emails retrieved from Gmail:

{email_context}

Answer the user's request using ONLY
the information contained in these emails.

If the user asks for a summary:
- Summarize the important emails.
- Mention the sender and subject when useful.
- Keep the response concise.

If the user asks about the latest email:
- Use the first email in the list.

Never invent information.
"""

        # ------------------------------------------
        # Call LLM
        # ------------------------------------------

        response = client.chat.completions.create(

            model="qwen2.5-coder-1.5b-instruct",

            temperature=0.2,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        answer = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        return answer

    # ------------------------------------------
    # Error handling
    # ------------------------------------------

    except Exception as e:

        print(
            "Email Agent Error:",
            e
        )

        return (
            "I was able to access your emails, "
            "but I couldn't generate the summary."
        )