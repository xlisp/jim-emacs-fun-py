from anthropic import Anthropic
import os

API_KEY = os.environ['OPENROUTER_API_KEY']
BASE_URL = "https://api.deepbricks.ai"
client = Anthropic(api_key=API_KEY, base_url=BASE_URL)

with client.messages.stream(
       max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": """Hello!"""
            }
        ],
        model="claude-3.5-sonnet") as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

# $ python deepbricks_cladue.py
# Hello! How can I assist you today?

