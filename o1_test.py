## python o1_test.py  | jq

import requests
import json
import os
# "Use python pyautogen lib  to write a code agent: need multiple roles: generate code, generate tests and run tests, code summary" 
question = "Use python pyautogen lib  how to write ReAct?"
response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
    "HTTP-Referer": "https://www.clackypaas.com/",
    "X-Title": "clacky"
  },
  data=json.dumps({
    "model": "openai/o1-preview", #"openai/o1-mini", # Optional
    "messages": [
      { "role": "user", "content": question }
    ]

  })
)
#print(f"{response.json()}")
##print(response.json())

# Output the JSON response in a format compatible with jq.
if response.status_code == 200:
    print(json.dumps(response.json(), indent=2))  # Use `json.dumps` to ensure valid JSON output
    print("========================\n")
    print(response.json()['choices'][0]['message']['content'])
else:
    print(json.dumps({"error": f"Error: {response.status_code}", "message": response.text}, indent=2))

