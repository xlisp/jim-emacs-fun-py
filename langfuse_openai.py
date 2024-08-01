from langfuse.decorators import observe
from langfuse.openai import openai # OpenAI integration
 
# https://langfuse.com/docs/sdk/python/decorators => openai才有这个。

## 这个是一个注入的写法：监听函数的输入输出！
@observe()
def story():
    return openai.chat.completions.create(
        model="gpt-3.5-turbo",
        max_tokens=100,
        messages=[
          {"role": "system", "content": "You are a great storyteller."},
          {"role": "user", "content": "Once upon a time in a galaxy far, far away..."}
        ],
    ).choices[0].message.content
 
@observe()
def main():
    return story()
 
#GPT: convert this picture show me markdown
#- **TRACE**: main (1.57s)
#  - **SPAN**: story (1.57s)
#    - **GENERATION**: OpenAI-generation (1.56s, 30 → 100 (Σ 130))

main()
