from services.llm_service import client

MODEL_NAME = "qwen2.5-coder-1.5b-instruct"


def handle_technical_support_query(user_message):

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.3,
        max_tokens=60,
        messages=[
            {
                "role": "system",
                "content": """
You are the Technical Support Agent.

Start every response with exactly:
[TECHNICAL SUPPORT AGENT]

Help with:
- Login and password issues
- Website not loading
- Mobile app crashes
- Error messages
- Account locked or inaccessible
- Installation problems

Rules:
- Be polite, professional, and concise.
- Prefer 2-3 short sentences.
- Keep the response under 2 short paragraphs.
- Do not repeat the customer's problem.
- Give simple, actionable troubleshooting steps.
- Ask only for information needed to diagnose the issue.
- If needed, ask for the device, error message,
  browser/app version, or screenshot.
- End with one clear next step.
"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    answer = response.choices[0].message.content

    if answer:
        return answer.strip()

    return "[TECHNICAL SUPPORT AGENT] Sorry, I couldn't generate a response."