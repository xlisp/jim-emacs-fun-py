## ZH: https://baoyu.io/translations/openai/assistant-api => 不用流的版本：https://platform.openai.com/docs/assistants/overview?context=without-streaming
## EN: https://platform.openai.com/docs/assistants/overview
# Assistant API 使您能够在自己的应用中创建 AI 助理。这样的助理根据指令运作，能够结合模型、工具和知识库来解答用户的问题。
## Assistant API 支持三种 工具111111 (都是外部手脚相关的)：代码解释器（Code Interpreter）=> Repl Server、信息检索（Retrieval）和函数调用（Function calling => function_calling_agent_important.py 例子）。我们未来的计划是推出更多由 OpenAI 创建的工具，并让您能在我们的平台上使用您自己的工具。

from openai import OpenAI
client = OpenAI()

## Step 1: Create an Assistant: 一个启用了代码解释器工具的个人数学辅导 Assistant
assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code
 to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o",
)

## Step 2: Create a Thread : Thread 就像是一场会话。我们建议在用户开始交流时就为每位用户创建一个 Thread。在这个 Thread 里，您可以通过创建消息（Messages）来添加用户特定的情境和文件 。相当于session
thread = client.beta.threads.create()

assistant #=>
Assistant(id='asst_jrgDEVIB5xFT0PtL8og5gziq', created_at=1719490632, description=None, instructions='You are a personal math tutor. Write and run code to answer math questions.', metadata={}, model='gpt-4o', name='Math Tutor', object='assistant', tools=[CodeInterpreterTool(type='code_interpreter')], response_format='auto', temperature=1.0, tool_resources=ToolResources(code_interpreter=ToolResourcesCodeInterpreter(file_ids=[]), file_search=None), top_p=1.0)

thread #=>
Thread(id='thread_qdHXsqAYR0k62AlVugZbKWeB', created_at=1719490637, metadata={}, object='thread', tool_resources=ToolResources(code_interpreter=None, file_search=None))

## Step 3: Add a Message to the Thread: 向 Thread 添加消息消息（Message）包含用户的文本内容，用户还可以选择上传任何 文件
message = client.beta.threads.messages.create(
     thread_id=thread.id,
     role="user",
     content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
)

message #=>
Message(id='msg_SmCP8YYkyWslT9b9zUrTyQXJ', assistant_id=None, attachments=[], completed_at=None, content=[TextContentBlock(text=Text(annotations=[], value='I need to solve the equation `3x + 11 = 14`. Can you help me?'), type='text')], created_at=1719490652, incomplete_at=None, incomplete_details=None, metadata={}, object='thread.message', role='user', run_id=None, status=None, thread_id='thread_qdHXsqAYR0k62AlVugZbKWeB')

## 4. Create Run: 要让 Assistant 对用户的消息做出反应，您需要创建一个 运行实例（Run）。这会让 Assistant 阅读整个 Thread，并决定是调用工具还是直接使用模型来以最合适的方式回答用户的问题。在运行过程中，Assistant 会添加标记为 role="assistant" 的消息到 Thread 中。
坚持去λ化(中-易) ~  @ run = client.beta.threads.runs.create_and_poll(
.....................   thread_id=thread.id,
.....................   assistant_id=assistant.id,
.....................   instructions="Please address the user as Jane Doe. The user has a premium account."
..................... )
.....................
坚持去λ化(中-易) ~  @
坚持去λ化(中-易) ~  @ run
Run(id='run_n6UMAELMZJLZWAhLcMsBJdwD', assistant_id='asst_jrgDEVIB5xFT0PtL8og5gziq', cancelled_at=None, completed_at=1719495485, created_at=1719495481, expires_at=None, failed_at=None, incomplete_details=None, instructions='Please address the user as Jane Doe. The user has a premium account.', last_error=None, max_completion_tokens=None, max_prompt_tokens=None, metadata={}, model='gpt-4o', object='thread.run', parallel_tool_calls=True, required_action=None, response_format='auto', started_at=1719495481, status='completed', thread_id='thread_qdHXsqAYR0k62AlVugZbKWeB', tool_choice='auto', tools=[CodeInterpreterTool(type='code_interpreter')], truncation_strategy=TruncationStrategy(type='auto', last_messages=None), usage=Usage(completion_tokens=182, prompt_tokens=151, total_tokens=333), temperature=1.0, top_p=1.0, tool_resources={})
坚持去λ化(中-易) ~  @ if run.status == 'completed':
.....................   messages = client.beta.threads.messages.list(
.....................     thread_id=thread.id
.....................   )
.....................   print(messages)
..................... else:
.....................   print(run.status)
.....................

SyncCursorPage[Message](data=[Message(id='msg_aqEXkuOs2ABXMW74cLqwyYqH', assistant_id='asst_jrgDEVIB5xFT0PtL8og5gziq', attachments=[], completed_at=None, content=[TextContentBlock(text=Text(annotations=[], value="Of course, Jane Doe! Let's solve the equation \\(3x + 11 = 14\\).\n\nFirst, we need to isolate \\(x\\). Here are the steps:\n\n1. Subtract 11 from both sides of the equation:\n   \\[\n   3x + 11 - 11 = 14 - 11\n   \\]\n   Simplifying this, we get:\n   \\[\n   3x = 3\n   \\]\n\n2. Next, divide both sides by 3 to solve for \\(x\\):\n   \\[\n   \\frac{3x}{3} = \\frac{3}{3}\n   \\]\n   Simplifying this, we get:\n   \\[\n   x = 1\n   \\]\n\nSo, the solution to the equation \\(3x + 11 = 14\\) is \\(x = 1\\)."), type='text')], created_at=1719495482, incomplete_at=None, incomplete_details=None, metadata={}, object='thread.message', role='assistant', run_id='run_n6UMAELMZJLZWAhLcMsBJdwD', status=None, thread_id='thread_qdHXsqAYR0k62AlVugZbKWeB'), Message(id='msg_SmCP8YYkyWslT9b9zUrTyQXJ', assistant_id=None, attachments=[], completed_at=None, content=[TextContentBlock(text=Text(annotations=[], value='I need to solve the equation `3x + 11 = 14`. Can you help me?'), type='text')], created_at=1719490652, incomplete_at=None, incomplete_details=None, metadata={}, object='thread.message', role='user', run_id=None, status=None, thread_id='thread_qdHXsqAYR0k62AlVugZbKWeB')], object='list', first_id='msg_aqEXkuOs2ABXMW74cLqwyYqH', last_id='msg_SmCP8YYkyWslT9b9zUrTyQXJ', has_more=False)

坚持去λ化(中-易) ~  @ print("Of course, Jane Doe! Let's solve the equation \\(3x + 11 = 14\\).\n\nFirst, we nee
d to isolate \\(x\\). Here are the steps:\n\n1. Subtract 11 from both sides of the equation:\n   \\[\n   3x + 1
1 - 11 = 14 - 11\n   \\]\n   Simplifying this, we get:\n   \\[\n   3x = 3\n   \\]\n\n2. Next, divide both sides
 by 3 to solve for \\(x\\):\n   \\[\n   \\frac{3x}{3} = \\frac{3}{3}\n   \\]\n   Simplifying this, we get:\n
\\[\n   x = 1\n   \\]\n\nSo, the solution to the equation \\(3x + 11 = 14\\) is \\(x = 1\\).")
Of course, Jane Doe! Let's solve the equation \(3x + 11 = 14\).

First, we need to isolate \(x\). Here are the steps:

1. Subtract 11 from both sides of the equation:
   \[
   3x + 11 - 11 = 14 - 11
   \]
   Simplifying this, we get:
   \[
   3x = 3
   \]

2. Next, divide both sides by 3 to solve for \(x\):
   \[
   \frac{3x}{3} = \frac{3}{3}
   \]
   Simplifying this, we get:
   \[
   x = 1
   \]

So, the solution to the equation \(3x + 11 = 14\) is \(x = 1\).
坚持去λ化(中-易) ~  @
