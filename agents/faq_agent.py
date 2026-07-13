from services.llm_service import client
from services.rag_service import search_documents


def handle_faq_query(user_message):

    # Search the knowledge base
    documents = search_documents(user_message)

    # Combine retrieved documents into one context
    context = "\n\n".join([doc.page_content for doc in documents])

    response = client.chat.completions.create(
        model="qwen2.5-coder-1.5b-instruct",
        temperature=0.3,
        messages=[
            {
                "role": "system",
                "content": f"""
You are a FAQ Support Agent.

Answer the customer's question ONLY using the company information below.

If the answer is not found in the company information,
politely say that you do not have that information.

Company Information:

{context}

Always answer politely and professionally.
"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    return response.choices[0].message.content