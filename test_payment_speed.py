from openai import OpenAI
import time

client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)

MODEL_NAME = "qwen2.5-coder-1.5b-instruct"

user_message = "A payment was deducted but my order failed. What should I do?"

start = time.perf_counter()

response = client.chat.completions.create(
    model=MODEL_NAME,
    temperature=0.3,
    max_tokens=100,
    stream=False,
    messages=[
        {
            "role": "system",
            "content": """
You are the Payment Support Agent.

Start every response with:
[PAYMENT AGENT]

Help with failed/pending payments, card declines, UPI issues,
duplicate charges, and payment confirmation.

Rules:
- Be polite, empathetic, concise, and actionable.
- Use at most 3 short steps.
- Never request full card numbers, CVV, UPI PIN, passwords, or OTPs.
- Never claim to have checked a bank account or transaction.
- Never claim a refund, verification, or company action was completed
  unless the system actually performed it.
- Never invent transaction status, policies, or refund timelines.

If money was deducted but the order failed/pending:
- Acknowledge the concern.
- Do not immediately suggest retrying payment.
- Ask for the order number, transaction ID/UPI reference if available,
  and payment method.
- Suggest checking the transaction status in the bank/UPI app.
- Explain that support may need to verify the transaction.

For duplicate payments:
Ask the customer to verify both transactions and provide their references.
Do not claim a refund was initiated.

For declined payments:
Suggest checking the bank's decline message or contacting the bank.

Ask only for information relevant to the customer's issue.
Keep the response short.
"""
        },
        {
            "role": "user",
            "content": user_message
        }
    ]
)

answer = response.choices[0].message.content

end = time.perf_counter()

print(answer)

print("\n----- TIMING -----")
print(f"Total response time: {end - start:.2f} seconds")
print(f"Characters generated: {len(answer)}")