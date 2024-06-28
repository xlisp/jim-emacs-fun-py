## 6.1 节定义的 Agent
import pdb


from langchain import hub
from langchain_community.llms.openai import OpenAI
from langchain.agents import load_tools
from langchain.agents import AgentExecutor
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.tools.render import render_text_description

# 通过 python-dotenv 加载环境变量
from dotenv import load_dotenv
load_dotenv()

# 准备大语言模型：这里需要 OpenAI，可以方便地按需停止推理
llm = OpenAI()
llm_with_stop = llm.bind(stop=["\nObservation"]) #=> 这里有个观察者，判断是否停。


# 准备我们的工具：这里用到 DuckDuckGo 搜索引擎，和一个基于 LLM 的计算器 =》相当于用了openai的function calling
tools = load_tools(["ddg-search", "llm-math"], llm=llm)

# 准备核心提示词：这里从 LangChain Hub 加载了 ReAct 模式的提示词，并填充工具的文本描述 =》 反思类型：reason action 理由和动作。
prompt = hub.pull("hwchase17/react")
prompt = prompt.partial(
    tools=render_text_description(tools),
    tool_names=", ".join([t.name for t in tools]),
)

# 构建 Agent 的工作链：这里最重要的是把中间步骤的结构要保存到提示词的 agent_scratchpad 中
agent = (
    {
        "input": lambda x: x["input"],
        ## 中间intermediate的steps，agent很重要的就是step的设计。
        "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
    }
    | prompt
    | llm_with_stop
    | ReActSingleInputOutputParser() ## 反思的LLM暑促结果解析OutputParser
)

# # 构建 Agent 执行器：执行器负责执行 Agent 工作链，直至得到最终答案（的标识）并输出回答
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
agent_executor.invoke({"input": "今天上海和北京的气温差几度？"}) #=>  {'input': '今天上海和北京的气温差几度？', 'output': '8 degrees'}

################## ==================

## 6.10 使用 LangGraph 替代原有 AgentExecutor

import operator
from typing import Annotated, TypedDict, Union
from langchain_core.agents import AgentAction, AgentFinish
from langgraph.graph import StateGraph, END

# 定义状态图的全局状态变量
class AgentState(TypedDict):
    # 接受用户输入
    input: str
    # Agent 每次运行的结果，可以是动作、结束、或为空（初始时）
    agent_outcome: Union[AgentAction, AgentFinish, None]
    # Agent 工作的中间步骤，是一个动作及对应结果的序列
    # 通过 operator.add 声明该状态的更新使用追加模式（而非默认的覆写）以保留中间步骤
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]

# 构造 Agent 节点
def agent_node(state):
    outcome = agent.invoke(state)
    # 输出需对应状态变量中的键值
    return {"agent_outcome": outcome}

# 构造工具节点
def tools_node(state):
    # 从 Agent 运行结果中识别动作
    agent_action = state["agent_outcome"]
    # 从动作中提取对应的工具
    tool_to_use = {t.name: t for t in tools}[agent_action.tool]
    # 调用工具并获取结果
    observation = tool_to_use.invoke(agent_action.tool_input)
    # 将工具执行及结果更新至全局状态变量，因为我们已声明其更新模式，故此处会自动追加至原有列表
    return {"intermediate_steps": [(agent_action, observation)]}


# 初始化状态图，带入全局状态变量
graph = StateGraph(AgentState)

# 分别添加 Agent 节点和工具节点
graph.add_node("agent", agent_node)
graph.add_node("tools", tools_node)

# 设置图入口
graph.set_entry_point("agent")


pdb.set_trace()

# 添加条件边
graph.add_conditional_edges(
    # 条件边的起点
    start_key="agent",
    # 判断条件，我们根据 Agent 运行的结果是动作还是结束返回不同的字符串
    condition=(
        lambda state: "exit"
        if isinstance(state["agent_outcome"], AgentFinish)
        else "continue"
    ),
    # 将条件判断所得的字符串映射至对应的节点
    conditional_edge_mapping={
        "continue": "tools",
        "exit": END,  # END是一个特殊的节点，表示图的出口，一次运行至此终止
    },
)

# 不要忘记连接工具与 Agent 以保证工具输出传回 Agent 继续运行
graph.add_edge("tools", "agent")

# 生成图的 Runnable 对象
agent_graph = graph.compile()

# 采用与 LCEL 相同的接口进行调用
agent_graph.invoke({"input": "今天上海和北京的气温差几度？"})
