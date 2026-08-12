import os
import base64
import re

from bs4 import BeautifulSoup

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


# ==================================================
# GMAIL PERMISSIONS
# ==================================================

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]


# ==================================================
# GET GMAIL SERVICE
# ==================================================

def get_gmail_service():

    creds = None

    # ------------------------------------------
    # Check existing token
    # ------------------------------------------

    if os.path.exists("token.json"):

        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    # ------------------------------------------
    # Refresh expired token
    # ------------------------------------------

    if creds and creds.expired and creds.refresh_token:

        creds.refresh(
            Request()
        )

    # ------------------------------------------
    # Login if no valid credentials
    # ------------------------------------------

    if not creds or not creds.valid:

        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json",
            SCOPES
        )

        creds = flow.run_local_server(
            port=0
        )

        # Save token
        with open(
            "token.json",
            "w"
        ) as token:

            token.write(
                creds.to_json()
            )

    # ------------------------------------------
    # Create Gmail API service
    # ------------------------------------------

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    return service


# ==================================================
# GET EMAIL HEADER
# ==================================================

def get_header(headers, name):

    for header in headers:

        if header.get("name", "").lower() == name.lower():

            return header.get(
                "value",
                ""
            )

    return ""


# ==================================================
# DECODE EMAIL BODY
# ==================================================

def decode_message_body(payload):

    body = ""

    # ------------------------------------------
    # Direct body
    # ------------------------------------------

    body_data = payload.get(
        "body",
        {}
    ).get(
        "data"
    )

    if body_data:

        try:

            body = base64.urlsafe_b64decode(
                body_data
            ).decode(
                "utf-8",
                errors="ignore"
            )

        except Exception:

            body = ""

    # ------------------------------------------
    # Multipart email
    # ------------------------------------------

    parts = payload.get(
        "parts",
        []
    )

    for part in parts:

        mime_type = part.get(
            "mimeType",
            ""
        )

        part_body = part.get(
            "body",
            {}
        )

        part_data = part_body.get(
            "data"
        )

        # Prefer plain text
        if (
            mime_type == "text/plain"
            and part_data
        ):

            try:

                return base64.urlsafe_b64decode(
                    part_data
                ).decode(
                    "utf-8",
                    errors="ignore"
                )

            except Exception:

                pass

        # Recursively check nested parts
        if part.get("parts"):

            nested_body = decode_message_body(
                part
            )

            if nested_body:

                return nested_body

    return body


# ==================================================
# CLEAN EMAIL BODY
# ==================================================

def clean_email_body(body):

    if not body:

        return ""

    # ------------------------------------------
    # Remove HTML
    # ------------------------------------------

    try:

        soup = BeautifulSoup(
            body,
            "html.parser"
        )

        body = soup.get_text(
            separator=" ",
            strip=True
        )

    except Exception:

        pass

    # ------------------------------------------
    # Remove excessive whitespace
    # ------------------------------------------

    body = re.sub(
        r"\s+",
        " ",
        body
    )

    # ------------------------------------------
    # Limit extremely large emails
    # ------------------------------------------

    body = body.strip()

    return body[:5000]


# ==================================================
# GET EMAILS
# ==================================================

def get_emails(max_results=10):

    try:

        service = get_gmail_service()

        # ------------------------------------------
        # Get latest messages
        # ------------------------------------------

        results = service.users().messages().list(
            userId="me",
            maxResults=max_results
        ).execute()

        messages = results.get(
            "messages",
            []
        )

        print(
            f"Emails found: {len(messages)}"
        )

        emails = []

        # ------------------------------------------
        # Read each message
        # ------------------------------------------

        for message in messages:

            message_id = message.get(
                "id"
            )

            print(
                f"Message ID: {message_id}"
            )

            email_data = service.users().messages().get(
                userId="me",
                id=message_id,
                format="full"
            ).execute()

            payload = email_data.get(
                "payload",
                {}
            )

            headers = payload.get(
                "headers",
                []
            )

            sender = get_header(
                headers,
                "From"
            )

            receiver = get_header(
                headers,
                "To"
            )

            subject = get_header(
                headers,
                "Subject"
            )

            date = get_header(
                headers,
                "Date"
            )

            raw_body = decode_message_body(
                payload
            )

            message_body = clean_email_body(
                raw_body
            )

            emails.append({

                "id": message_id,

                "sender": sender,

                "receiver": receiver,

                "subject": subject,

                "date": date,

                "message": message_body

            })

        return emails

    except Exception as e:

        print(
            "Gmail Error:",
            e
        )

        return []


# ==================================================
# SEARCH EMAILS
# ==================================================

def search_emails(
    query,
    max_results=10
):

    try:

        service = get_gmail_service()

        print(
            f"Gmail Query: {query}"
        )

        # ------------------------------------------
        # Search Gmail
        # ------------------------------------------

        results = service.users().messages().list(
            userId="me",
            q=query,
            maxResults=max_results
        ).execute()

        messages = results.get(
            "messages",
            []
        )

        print(
            f"Search results: {len(messages)}"
        )

        emails = []

        # ------------------------------------------
        # Get complete email information
        # ------------------------------------------

        for message in messages:

            message_id = message.get(
                "id"
            )

            print(
                f"Message ID: {message_id}"
            )

            email_data = service.users().messages().get(
                userId="me",
                id=message_id,
                format="full"
            ).execute()

            payload = email_data.get(
                "payload",
                {}
            )

            headers = payload.get(
                "headers",
                []
            )

            sender = get_header(
                headers,
                "From"
            )

            receiver = get_header(
                headers,
                "To"
            )

            subject = get_header(
                headers,
                "Subject"
            )

            date = get_header(
                headers,
                "Date"
            )

            raw_body = decode_message_body(
                payload
            )

            message_body = clean_email_body(
                raw_body
            )

            emails.append({

                "id": message_id,

                "sender": sender,

                "receiver": receiver,

                "subject": subject,

                "date": date,

                "message": message_body

            })

        return emails

    except Exception as e:

        print(
            "Gmail Search Error:",
            e
        )

        return []