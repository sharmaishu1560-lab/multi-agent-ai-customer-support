import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ELEVENLABS_API_KEY")

print("API key loaded:", bool(api_key))

if api_key:
    print("First characters:", api_key[:6])
    print("Key length:", len(api_key))
else:
    print("ELEVENLABS_API_KEY was not found.")