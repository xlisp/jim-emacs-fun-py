# https://langfuse.com/docs/integrations/litellm/tracing
from litellm import completion
 
## set env variables
os.environ["LANGFUSE_PUBLIC_KEY"] = ""
os.environ["LANGFUSE_SECRET_KEY"] = ""
 
# Langfuse host
os.environ["LANGFUSE_HOST"]="https://cloud.langfuse.com" # 🇪🇺 EU region
# os.environ["LANGFUSE_HOST"]="https://us.cloud.langfuse.com" # 🇺🇸 US region
 
os.environ["OPENAI_API_KEY"] = ""
os.environ["COHERE_API_KEY"] = ""
 
# set callbacks
litellm.success_callback = ["langfuse"]
litellm.failure_callback = ["langfuse"]
 
import litellm
 
# openai call
openai_response = litellm.completion(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": "Hi 👋 - i'm openai"}
  ]
)
 
print(openai_response)
 
# cohere call
cohere_response = litellm.completion(
  model="command-nightly",
  messages=[
    {"role": "user", "content": "Hi 👋 - i'm cohere"}
  ]
)
print(cohere_response)
 
