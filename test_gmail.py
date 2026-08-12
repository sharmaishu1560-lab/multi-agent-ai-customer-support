from services.gmail_service import get_emails


emails = get_emails(5)

print("\n========== YOUR EMAILS ==========\n")

for email in emails:

    print("From:", email["sender"])
    print("Subject:", email["subject"])
    print("Date:", email["date"])
    print("Message:", email["body"][:500])

    print("--------------------------------")