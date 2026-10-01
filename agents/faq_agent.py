from services.llm_service import client
from services.rag_service import search_documents
import time

MODEL_NAME = "qwen2.5-coder-1.5b-instruct"


def handle_faq_query(user_message):

    rag_start = time.perf_counter()

    documents = search_documents(user_message)

    print(f"⏱️ RAG Search: {time.perf_counter() - rag_start:.2f} seconds")

    context = "\n\n".join([doc.page_content for doc in documents])

    print(f"📄 Retrieved Documents: {len(documents)}")
    print(f"📄 Context Characters: {len(context)}")

    llm_start = time.perf_counter()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.3,
        max_tokens=60,
        messages=[
            {
                "role": "system",
                "content": f"""
You are the FAQ Support Agent.

Start every response with exactly:
[FAQ AGENT]

Answer the customer's question ONLY using the company information below.

If the answer is not found in the company information,
say that you do not have that information.

Rules:
- Be polite, professional, and concise.
- Prefer 2-3 short sentences.
- Keep the response under 2 short paragraphs.
- Do not invent company information or policies.
- Do not repeat the customer's question.
- End with one clear next step when appropriate.

Company Information:
{context}
"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    print(f"⏱️ FAQ LLM: {time.perf_counter() - llm_start:.2f} seconds")

    answer = response.choices[0].message.content

    if answer:
        return answer.strip()

    return "[FAQ AGENT] Sorry, I couldn't generate a response."