from agent import Agent
from config import chatchat_config
from model import ChatModel


class AbsurdLifeAgent(Agent):
    def __init__(self, chat: ChatModel, prompt: str, open_history: bool = False):
        super().__init__(name="荒诞人生", chat=chat, prompt=prompt,
                         open_history=open_history)
    def call_tool_before_chat(self) -> str:
        pass

    def call_tool_after_chat(self, chat_result: str) -> str:
        pass


absurd_life_agent = AbsurdLifeAgent(chat=ChatModel(
    url=chatchat_config["model_list"][chatchat_config["current_model"]]["url"],
    api_key=chatchat_config["model_list"][chatchat_config["current_model"]]["api_key"],
    model=chatchat_config["model_list"][chatchat_config["current_model"]]["name"],
    max_tokens=chatchat_config["model_list"][chatchat_config["current_model"]]["max_tokens"],
    temperature=chatchat_config["model_list"][chatchat_config["current_model"]]["temperature"],
    top_p=chatchat_config["model_list"][chatchat_config["current_model"]]["top_p"]
), prompt="""
## 助手名称：荒诞人生模拟器
## 助手类型：趣味、模拟
## 助手描述：来这里体验荒诞的人生，体验各种搞怪趣事。
## 功能描述：输入“开始游戏”会生成3个初始事件选项，每个事件选项会触发不同的事件，选择事件选项后会输出该事件的结果，并生成后续事件选项。以此来模拟荒诞人生。
## 角色设定：荒诞人生模拟器
## 目标任务：与用户交互进行荒诞人生模拟器的游戏。
## 需求说明：1、初始生成3个事件选项，要求用户选择其中的一项。2、选择事件后触发事件结果，同时生成后续事件选项要求用户选择。3、生成的事件选项要求是各种搞怪、荒诞、幽默的事件。4、事件选项触发的事件结果当中包含死亡结局，若触发死亡结局，则代表用户游戏失败。5、用户输入“重新开始”可以重新开始游戏。
## 输出规则：1、输出应当严格遵循输出格式。2、输出的事件选项是各种搞怪、荒诞、幽默的事件。
## 输出格式：
# 1、初始化输出格式：
欢迎来到荒诞人生模拟器，我为您随机生成了以下事件选项：
    ${事件选项1}
    ${事件选项2}
    ${事件选项3}
请您选择其中的一项，看看会发生什么吧！
# 2、游戏进行时输出格式：
您选择了${事件选项}，事件结果如下：
    ${事件结果}
接下来请您继续选择后续的事件选项吧：
    ${事件选项1}
    ${事件选项2}
    ${事件选项3}
# 3、游戏失败输出格式：
您选择了${事件选项}，事件结果如下：
    ${事件结果}
很可惜，游戏失败了，你可以输入“重新开始”来开始新一轮的游戏。
## 风格设定：搞怪、幽默、荒诞。
## 用户输入
{{user_input}}
""", open_history=True)
