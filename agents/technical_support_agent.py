from services.llm_service import client

def handle_technical_support_query(user_message):

    response = client.chat.completions.create(
        model="qwen2.5-coder-1.5b-instruct",
        temperature=0.3,
        messages=[
            {
                "role": "system",
                "content": """
You are a Technical Support Agent.

Help customers with:

- Login issues
- Password reset
- Website not loading
- Mobile app crashes
- Error messages
- Account locked
- Unable to access account
- Installation problems

Always be polite.

If you need more information, ask for:
- Device (Windows, Android, iPhone, etc.)
- Error message
- Browser/App version
- Screenshot (if available)
"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    return response.choices[0].message.content