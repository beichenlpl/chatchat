from agent import Agent
from model import ChatModel
from config import chatchat_config



class EventSummary(Agent):
    def __init__(self, chat: ChatModel, prompt: str):
        super().__init__("事件总结", chat, prompt)

    def call_tool_after_chat(self, chat_result: str) -> str:
        pass

    def call_tool_before_chat(self) -> str:
        pass

event_summary = EventSummary(chat=ChatModel(
    url=chatchat_config["model_list"][chatchat_config["current_model"]]["url"],
    api_key=chatchat_config["model_list"][chatchat_config["current_model"]]["api_key"],
    model=chatchat_config["model_list"][chatchat_config["current_model"]]["name"],
    max_tokens=4000,
    temperature=0.0,
    top_p=0.1
), prompt="""
分析下面使用首次使用```符号包裹的文本中表述的事件的**初始状态**、**事件发生**、**事件过程**、**事件结果**。并对事件内容进行总结。最后将结果以标准的JSON格式输出。
```
{{input}}
```

示例：
输入
```textile
猎人去打猎，一棵树上站着10只鸟，猎人开枪打死了一只，这颗树上的鸟都飞走了。
```
输出
```json
{
    "事件名称"：{
        "名称": "猎人打鸟"
        "关键词": [
            "猎人",
            "打猎",
            "鸟"
    },
    "事件概括": {
       "初始状态": "猎人去打猎，一棵树上站着10只鸟",
       "事件发生": "猎人开枪打死了一只鸟",
       "事件过程": "猎人进行打猎活动并使用枪支射杀了一只鸟",
       "事件结果": "这棵树上的鸟都飞走了",
    },
    "事件总结": {
        "总结": "猎人在打猎过程中射杀了一只站在树上的鸟，导致该树上的其他鸟全部受惊飞走。"
    }
}
```

输出限制：
1、禁止输出结果外的任何信息。
""")

event_summary.set_prompt_variable("input", """
多名网友在社交平台发帖表示，疑似因被游客投喂食物而变得膘肥体壮的“可可西里网红狼初代目”被一辆大货车不慎压死。有网友表示自己拨打了救助电话，但工作人员赶来后表示“网红狼”已经死亡，无法救治。24日，发帖网友王女士（化名）告诉上游新闻记者，被压死的这只狼体型较大，尸体被救助站工作人员装入麻袋中运走。三江源国家公园管理局工作人员表示，目前在公路等待游客投喂的狼有四五只，被压死的为其中一只，当时大货车司机发现狼后紧急刹车，但是已经来不及，具体情况还在核实中。该工作人员呼吁，游客不要向野生动物投喂食物，会导致它们失去自主觅食的本领，而且降低对车辆的警惕性，从而导致交通事故。
""")

print(event_summary.execute())