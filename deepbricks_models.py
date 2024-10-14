from openai import OpenAI
import os

API_KEY =  os.environ['OPENROUTER_API_KEY']
BASE_URL = "https://api.deepbricks.ai/v1/"
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
resp = client.models.list()
print(resp.to_json())
## ## @ python deepbricks_models.py
## {
##   "data": [
##     {
##       "id": "llama-3-70b",
##       "created": 1713385421,
##       "object": "model",
##       "owned_by": "llama"
##     },
##     {
##       "id": "dall-e-3",
##       "created": 1698785189,
##       "object": "model",
##       "owned_by": "openai"
##     },
##     {
##       "id": "gpt-4o",
##       "created": 1715367049,
##       "object": "model",
##       "owned_by": "openai"
##     },
##     {
##       "id": "gpt-4o-mini",
##       "created": 1721358778,
##       "object": "model",
##       "owned_by": "openai"
##     },
##     {
##       "id": "gpt-4o-mini-2024-07-18",
##       "created": 1721358778,
##       "object": "model",
##       "owned_by": "openai"
##     },
##     {
##       "id": "gpt-3.5-turbo",
##       "created": 1677610602,
##       "object": "model",
##       "owned_by": "openai"
##     },
##     {
##       "id": "gpt-3.5-turbo-1106",
##       "created": 1677610602,
##       "object": "model",
##       "owned_by": "openai"
##     },
##     {
##       "id": "gpt-3.5-turbo-0125",
##       "created": 1677610602,
##       "object": "model",
##       "owned_by": "openai"
##     },
##     {
##       "id": "llama-3.1-70b",
##       "created": 1721730592,
##       "object": "model",
##       "owned_by": "llama"
##     },
##     {
##       "id": "llama-3.1-405b",
##       "created": 1721730592,
##       "object": "model",
##       "owned_by": "llama"
##     },
##     {
##       "id": "claude-3.5-sonnet",
##       "created": 1718945463,
##       "object": "model",
##       "owned_by": "anthropic"
##     },
##     {
##       "id": "claude-3-5-sonnet-20240620",
##       "created": 1718945463,
##       "object": "model",
##       "owned_by": "anthropic"
##     },
##     {
##       "id": "gpt-4o-2024-08-06",
##       "created": 1723528128,
##       "object": "model",
##       "owned_by": "openai"
##     },
##     {
##       "id": "gpt-4-turbo",
##       "created": 1712361441,
##       "object": "model",
##       "owned_by": "openai"
##     },
##     {
##       "id": "gpt-4-turbo-preview",
##       "created": 1712361441,
##       "object": "model",
##       "owned_by": "openai"
##     },
##     {
##       "id": "gpt-4-turbo-0125-preview",
##       "created": 1712361441,
##       "object": "model",
##       "owned_by": "openai"
##     },
##     {
##       "id": "gpt-4-turbo-1106-preview",
##       "created": 1712361441,
##       "object": "model",
##       "owned_by": "openai"
##     },
##     {
##       "id": "gpt-3.5-turbo-instruct",
##       "created": 1692901427,
##       "object": "model",
##       "owned_by": "openai"
##     }
##   ],
##   "object": "list"
## }
## 
