 curl -s https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR-API-KEY" \
  -d '{
    "model": "gpt-3.5-turbo-16k",
    "messages": [
          {
         "role": "system",
         "content": "您是足球专家"
          },
          {
                 "role": "user",
                 "content": "谁赢得了2018年的FIFA世界杯？"
          },
          {
                 "role": "assistant",
                 "content": "法国赢得了2018年的FIFA世界杯。"
          },
          {
                 "role": "user",
                 "content": "下一届FIFA世界杯什么时候

举行？"
          }
        ]
  }'


