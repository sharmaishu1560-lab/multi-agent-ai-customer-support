from openai import OpenAI
import time

client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)

start = time.perf_counter()
first_token_time = None
full_text = ""

stream = client.chat.completions.create(
    model="qwen2.5-coder-1.5b-instruct",
    messages=[
    {
        "role": "system",
        "content": "Answer customer support questions briefly. Use at most 2 sentences."
    },
    {
        "role": "user",
        "content": "A payment was deducted but my order failed. What should I do?"
    }
],
    max_tokens=60,
    temperature=0.2,
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        if first_token_time is None:
            first_token_time = time.perf_counter()
        full_text += chunk.choices[0].delta.content

end = time.perf_counter()

print(full_text)
print("\n----- TIMING -----")

if first_token_time:
    print(f"Time to first token: {first_token_time - start:.2f} seconds")

print(f"Total response time: {end - start:.2f} seconds")
print(f"Tokens/characters generated: {len(full_text)}")