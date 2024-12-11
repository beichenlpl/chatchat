import datetime
import requests

from agent import Agent
from config import chatchat_config
from model import ChatModel


def get_weibo_hot_search() -> str:
    target_url = "https://weibo.com/ajax/side/hotSearch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url=target_url, headers=headers, timeout=30)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    return response.text


class HotspotExtractAgent(Agent):
    """
    微博热搜热点提取智能体
    """

    def __init__(self, chat: ChatModel, prompt: str, open_history: bool = False):
        super().__init__(name="微博热搜新闻稿撰写智能体", chat=chat, prompt=prompt,
                         open_history=open_history)

    def call_tool_before_chat(self) -> str:
        self.set_prompt_variable("current_time", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.set_prompt_variable("hot_search", get_weibo_hot_search())
        return ""

    def call_tool_after_chat(self, chat_result: str) -> str:
        pass


hotspot_extract_agent = HotspotExtractAgent(chat=ChatModel(
    url=chatchat_config["model_list"][chatchat_config["current_model"]]["url"],
    api_key=chatchat_config["model_list"][chatchat_config["current_model"]]["api_key"],
    model=chatchat_config["model_list"][chatchat_config["current_model"]]["name"],
    max_tokens=chatchat_config["model_list"][chatchat_config["current_model"]]["max_tokens"],
    temperature=chatchat_config["model_list"][chatchat_config["current_model"]]["temperature"],
    top_p=chatchat_config["model_list"][chatchat_config["current_model"]]["top_p"]
), prompt="""
# 角色
你是一名新闻学领域擅长信息提取和撰写新闻稿的专家。

# 能力
你擅长从大量文本中提取出关键的信息，并且你可以根据这些信息按照一定的权重进行排序。

# 目标
从提供的输入中提取热搜信息并根据热度排序，结合你自己的理解以此写一份新闻稿。

# 工作流程
1、理解**输入**的内容，输入内容为JSON格式，其中字段**word**为热搜标题，字段**num**为热搜的热度，字段**category**为热搜的类别。
2、对于提取到的热搜信息按照热度进行排序。
3、对排序的信息进行内容总结和概括。
3、结合总结的信息和**当前时间**撰写一篇新闻稿。

# 输入
{{hot_search}}

# 当前时间
{{current_time}}


# 输出限制
1、你应当严格遵循新闻稿的格式输出你撰写的新闻稿，撰写的新闻稿应当易于理解且引人入胜, 明确输出**当前时间**，且你不得夸大和歪曲事实。
2、禁止输出除**输入**中提取到的信息外的任何冗余信息。
3、你只需要输出新闻稿即可。
""")
