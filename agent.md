1. llm 大语言模型，就是大脑，训练好的分词规则决定token数量
token就是大模型要处理的数据，是通过tokenizer编码器把你的中文翻译成llm 能处理的数据
Context（上下文）就是在和大模型对话时要把历史聊天记录一起带过去给llm，它才能结合历史记录和我们对他，不然就失忆了
Context windows（上下文窗口）就是能带多少聊天记录过去，越大当然就能聊得越久不容易失忆，和我们大脑容量一样
tool就是提供工具给llm调用，让其能够感知和影响外界环境，而不是只能聊天
mcp就是解决tool规范统一问题，大家在制作tool工具包时都遵循mcp这个规范，tool就能在不同llm平台都能使用，不用一个平台开发一套tool
agent本质也是就是llm+tool，且具有一定自主规划能力(reAct或者plan等方式），能帮我干活直到解决问题
Agent Skills则是指把常用技能固化为一个固定格式的一个markdown文件，方便llm知道调用tool的流程（其具有渐进式披露能力也能帮你省token消耗）

2.  transformer核心
    Query = 我想找谁
    Key   = 我是谁
    Value = 我带的信息