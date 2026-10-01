
import re


def detect_intent(user_message):
    """
    Fast rule-based customer support intent detection.
    Returns one intent without calling the LLM.
    """

    message = user_message.lower().strip()

    # Normalize punctuation and extra spaces
    message = re.sub(r"\s+", " ", message)

    # -----------------------------------
    # 1. EMAIL
    # -----------------------------------

    email_phrases = [
        "email",
        "emails",
        "gmail",
        "inbox",
        "latest mail",
        "latest mails",
        "latest email",
        "latest emails",
        "read my mail",
        "read my email",
        "summarize my mail",
        "summarize my email",
        "search my mail",
        "search my email",
    ]

    if any(phrase in message for phrase in email_phrases):
        print("RULE-BASED INTENT: email")
        return "email"

    # -----------------------------------
    # 2. ESCALATION
    # -----------------------------------

    escalation_phrases = [
        "human agent",
        "human support",
        "talk to a human",
        "speak to a human",
        "talk to an agent",
        "speak to an agent",
        "customer representative",
        "customer support representative",
        "connect me to",
        "manager",
        "supervisor",
        "make a complaint",
        "file a complaint",
        "not satisfied",
        "still unresolved",
        "issue is unresolved",
        "not resolved",
        "this is not helping",
    ]

    if any(phrase in message for phrase in escalation_phrases):
        print("RULE-BASED INTENT: escalation")
        return "escalation"

    # -----------------------------------
    # 3. PAYMENT
    # -----------------------------------

    payment_phrases = [
        "payment failed",
        "payment issue",
        "payment problem",
        "payment not working",
        "payment deducted",
        "money deducted",
        "amount deducted",
        "charged but",
        "charged, but",
        "charged and",
        "duplicate charge",
        "double charged",
        "incorrect charge",
        "wrong amount charged",
        "transaction failed",
        "order was not confirmed",
        "order is not confirmed",
        "order wasn't confirmed",
        "order not confirmed",
        "paid but",
        "payment successful but",
        "payment processed but",
        "billing problem",
        "billing issue",
        "payment",
        "billing",
        "transaction",
        "charged",
    ]

    if any(phrase in message for phrase in payment_phrases):
        print("RULE-BASED INTENT: payment")
        return "payment"

    # -----------------------------------
    # 4. REFUND
    # -----------------------------------

    refund_phrases = [
        "i want a refund",
        "i need a refund",
        "request a refund",
        "refund my order",
        "get my money back",
        "money back",
        "initiate a refund",
        "process my refund",
        "check my refund",
        "refund status",
        "return my product for a refund",
        "refund",
        "return my order",
        "return this product",
    ]

    if any(phrase in message for phrase in refund_phrases):
        print("RULE-BASED INTENT: refund")
        return "refund"

    # -----------------------------------
    # 5. ORDER
    # -----------------------------------

    order_phrases = [
        "track my order",
        "track order",
        "order status",
        "where is my order",
        "where's my order",
        "delivery status",
        "when will my order arrive",
        "when is my order arriving",
        "shipping status",
        "order tracking",
        "order number",
        "cancel my order",
        "cancel order",
        "late delivery",
        "delayed order",
    ]

    if any(phrase in message for phrase in order_phrases):
        print("RULE-BASED INTENT: order")
        return "order"

    # -----------------------------------
    # 6. TECHNICAL SUPPORT
    # -----------------------------------

    technical_phrases = [
        "technical issue",
        "technical problem",
        "app is not working",
        "application is not working",
        "website is not working",
        "site is not working",
        "login issue",
        "login problem",
        "can't log in",
        "cannot log in",
        "unable to log in",
        "password issue",
        "error message",
        "app crashed",
        "website crashed",
        "screen is frozen",
        "not loading",
        "bug",
        "software issue",
    ]

    if any(phrase in message for phrase in technical_phrases):
        print("RULE-BASED INTENT: technical_support")
        return "technical_support"

    # -----------------------------------
    # 7. FAQ
    # -----------------------------------

    faq_phrases = [
        "warranty",
        "return policy",
        "refund policy",
        "shipping policy",
        "delivery policy",
        "business hours",
        "working hours",
        "company information",
        "about your company",
        "contact information",
        "contact details",
        "how do i return",
        "what is your return",
        "what is the refund",
        "what is your refund",
    ]

    if any(phrase in message for phrase in faq_phrases):
        print("RULE-BASED INTENT: faq")
        return "faq"

    # -----------------------------------
    # 8. GENERAL
    # -----------------------------------

    print("RULE-BASED INTENT: general")
    return "general"