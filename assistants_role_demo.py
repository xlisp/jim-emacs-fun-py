## ZH: https://baoyu.io/translations/openai/assistant-api
## EN: https://platform.openai.com/docs/assistants/overview
# Assistant API 使您能够在自己的应用中创建 AI 助理。这样的助理根据指令运作，能够结合模型、工具和知识库来解答用户的问题。目前，Assistant API 支持三种 工具：代码解释器（Code Interpreter）、信息检索（Retrieval）和函数调用（Function calling）。我们未来的计划是推出更多由 OpenAI 创建的工具，并让您能在我们的平台上使用您自己的工具。

from openai import OpenAI
client = OpenAI()

assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code
 to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o",
)


thread = client.beta.threads.create()

assistant #=>
Assistant(id='asst_jrgDEVIB5xFT0PtL8og5gziq', created_at=1719490632, description=None, instructions='You are a personal math tutor. Write and run code to answer math questions.', metadata={}, model='gpt-4o', name='Math Tutor', object='assistant', tools=[CodeInterpreterTool(type='code_interpreter')], response_format='auto', temperature=1.0, tool_resources=ToolResources(code_interpreter=ToolResourcesCodeInterpreter(file_ids=[]), file_search=None), top_p=1.0)

thread #=>
Thread(id='thread_qdHXsqAYR0k62AlVugZbKWeB', created_at=1719490637, metadata={}, object='thread', tool_resources=ToolResources(code_interpreter=None, file_search=None))
 message = client.beta.threads.messages.create(
     thread_id=thread.id,
     role="user",
     content="I need to solve the equation `3x + 11 = 14`. Can you h
elp me?"
)

message #=>
Message(id='msg_SmCP8YYkyWslT9b9zUrTyQXJ', assistant_id=None, attachments=[], completed_at=None, content=[TextContentBlock(text=Text(annotations=[], value='I need to solve the equation `3x + 11 = 14`. Can you help me?'), type='text')], created_at=1719490652, incomplete_at=None, incomplete_details=None, metadata={}, object='thread.message', role='user', run_id=None, status=None, thread_id='thread_qdHXsqAYR0k62AlVugZbKWeB')
