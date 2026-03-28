import re
import os
# from weather import get_weather
# from search_attraction import get_attraction

from agent.weather.weather import get_weather
from agent.weather.search_attraction import get_attraction
from agent.weather.openai import OpenAICompatibleClient

API_KEY = "sk-5nV1JkEec33W7D8ZbAuaR0uwYsqoyIUkRWM2JE8ntbMno7Pz"
BASE_URL = "https://api.openai-proxy.org/v1"
MODEL_ID = "gpt-5.4-mini"
TAVILY_API_KEY="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"
os.environ['TAVILY_API_KEY'] = TAVILY_API_KEY

available_tools = {
    "get_weather": get_weather,
    "get_attraction": get_attraction,
}

llm = OpenAICompatibleClient(
    model=MODEL_ID,
    api_key=API_KEY,
    base_url=BASE_URL
)

user_prompt = "你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。"
AGENT_SYSTEM_PROMPT = """
你是一个智能旅行助手。你的任务是分析用户的请求，并使用可用工具一步步地解决问题。

# 可用工具:
- `get_weather(city: str)`: 查询指定城市的实时天气。
- `get_attraction(city: str, weather: str)`: 根据城市和天气搜索推荐的旅游景点。

# 输出格式要求:
你的每次回复必须严格遵循以下格式，包含一对Thought和Action：

Thought: [你的思考过程和下一步计划]
Action: [你要执行的具体行动]

Action的格式必须是以下之一：
1. 调用工具：function_name(arg_name="arg_value")
2. 结束任务：Finish[最终答案]

# 重要提示:
- 每次只输出一对Thought-Action
- Action必须在同一行，不要换行
- 当收集到足够信息可以回答用户问题时，必须使用 Action: Finish[最终答案] 格式结束

请开始吧！
"""
prompt_history = [f"用户请求: {user_prompt}"]

print(f"用户输入: {user_prompt}\n" + "="*40)

for i in range(5):
    print(f"--- 循环 {i+1} ---\n")
    full_prompt = "\n".join(prompt_history)
    llm_output = llm.generate(full_prompt,system_prompt=AGENT_SYSTEM_PROMPT)
    match = re.search(r'(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)', llm_output, re.DOTALL)
    if match:
        truncated = match.group(1).strip()
        if truncated != llm_output.strip():
            llm_output = truncated
            print("已截断多余的 Thought-Action 对")
    print(f"模型输出:\n{llm_output}\n")
    prompt_history.append(llm_output)
    
    # 3.3. 解析并执行行动
    action_match = re.search(r"Action: (.*)", llm_output, re.DOTALL)
    if not action_match:
        observation = "错误: 未能解析到 Action 字段。请确保你的回复严格遵循 'Thought: ... Action: ...' 的格式。"
        observation_str = f"Observation: {observation}"
        print(f"{observation_str}\n" + "="*40)
        prompt_history.append(observation_str)
        continue
    action_str = action_match.group(1).strip()

    if action_str.startswith("Finish"):
        n = re.match(r"Finish\[(.*)\]", action_str)
        if m:
            final_answer = m.group(1)
        print(f"任务完成，最终答案: {final_answer}")
        break
    
    m = re.search(r"(\w+)\(", action_str)
    if m:
        tool_name = m.group(1)
    m = re.search(r"\((.*)\)", action_str)
    if m:
        args_str = m.group(1)
    kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))

    if tool_name in available_tools:
        observation = available_tools[tool_name](**kwargs)
    else:
        observation = f"错误:未定义的工具 '{tool_name}'"

    # 3.4. 记录观察结果
    observation_str = f"Observation: {observation}"
    print(f"{observation_str}\n" + "="*40)
    prompt_history.append(observation_str)