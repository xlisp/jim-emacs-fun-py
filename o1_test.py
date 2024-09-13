## python o1_test.py  | jq

import requests
import json
import os

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
    "HTTP-Referer": "https://www.clackypaas.com/",
    "X-Title": "clacky"
  },
  data=json.dumps({
    "model": "openai/o1-mini", # Optional
    "messages": [
      { "role": "user", "content": "What is the meaning of life?" }
    ]

  })
)
#print(f"{response.json()}")
##print(response.json())

# Output the JSON response in a format compatible with jq.
if response.status_code == 200:
    print(json.dumps(response.json(), indent=2))  # Use `json.dumps` to ensure valid JSON output
else:
    print(json.dumps({"error": f"Error: {response.status_code}", "message": response.text}, indent=2))

## ===>> erro:
# requests.exceptions.ProxyError: HTTPSConnectionPool(host='openrouter.ai', port=443): Max retries exceeded with url: /api/v1/chat/completions (Caused by ProxyError('Unable to connect to proxy', RemoteDisconnected('Remote end closed connection without response')))

