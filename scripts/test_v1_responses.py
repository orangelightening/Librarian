#!/usr/bin/env python3
"""
Test LM Studio /v1/responses OpenAI-compatible API.
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Use the correct LM Studio OpenAI-compatible endpoint
api_endpoint = "http://localhost:1234/v1/responses"
api_token = os.getenv("LM_STUDIO_API_TOKEN")
model = os.getenv("LM_STUDIO_MODEL", "unsloth/qwen3.5-9b")

headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

# OpenAI-compatible format
payload = {
    "model": model,
    "messages": [
        {"role": "user", "content": "Who are you? Please respond in one sentence."}
    ]
}

print("Testing /v1/responses OpenAI-compatible API...")
print(f"Model: {model}")
print(f"Endpoint: {api_endpoint}")
print(f"Query: Who are you?")
print()

try:
    response = requests.post(api_endpoint, headers=headers, json=payload, timeout=120)
    response.raise_for_status()

    result = response.json()

    print("Response received successfully!")
    print(f"Status: {response.status_code}")
    print()

    # Try to extract content
    if 'choices' in result and len(result['choices']) > 0:
        message = result['choices'][0].get('message', {})
        if 'content' in message:
            print("Response:")
            print(message['content'])
            print()

            if "librarian" in message['content'].lower():
                print("✅ SUCCESS: /v1/responses API is working with system prompt!")
            else:
                print("⚠️  Model responded but check if system prompt is active")
    else:
        print("Unexpected response format:")
        import json
        print(json.dumps(result, indent=2))

except Exception as e:
    print(f"❌ Error: {e}")
