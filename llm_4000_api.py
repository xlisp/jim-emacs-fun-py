from fastapi import FastAPI
from pydantic import BaseModel
import openai
import json


client = openai.OpenAI(api_key="anything",base_url="http://0.0.0.0:4000") # set proxy to base_url

app = FastAPI()

# Request model for the content input
class ChatRequest(BaseModel):
    content: str

@app.post("/generate-poem/")
async def generate_poem(request: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": request.content
                }
            ]
        )
        return json.loads(response.json())
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# run: $ uvicorn llm_api:app
# test :
# curl -X 'POST' 'http://127.0.0.1:8000/generate-poem/' -H 'Content-Type: application/json' -d '{"content": "this is a test request, write a short poem"}' | jq


