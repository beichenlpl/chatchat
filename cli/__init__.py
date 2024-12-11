from agent.hotspot_extract_agent import hotspot_extract_agent
from config import chatchat_config
from model import ChatModel

chat = ChatModel(
    url=chatchat_config["model_list"][chatchat_config["current_model"]]["url"],
    api_key=chatchat_config["model_list"][chatchat_config["current_model"]]["api_key"],
    model=chatchat_config["model_list"][chatchat_config["current_model"]]["name"],
    max_tokens=chatchat_config["model_list"][chatchat_config["current_model"]]["max_tokens"],
    temperature=chatchat_config["model_list"][chatchat_config["current_model"]]["temperature"],
    top_p=chatchat_config["model_list"][chatchat_config["current_model"]]["top_p"]
)


def call_agent(code: str, question: str = ""):
    if code == "hotspot_extract":
        return hotspot_extract_agent.execute()
    else:
        return "Agent not found"


def call_agent_stream(code: str, question: str = ""):
    if code == "hotspot_extract":
        print(f"调用智能体：{hotspot_extract_agent.name}")
        return hotspot_extract_agent.execute_stream()
    else:
        return "Agent not found"

def chat_in_cli() -> None:
    while True:
        prompt = input("User: ")
        chat.prompt(prompt)
        if prompt == "exit":
            break
        if prompt == "reset":
            chat.reset()
            continue
        if prompt == "agent":
            code = input("Agent code: ")
            print("Chatbot: ", end="")
            for chunk in call_agent_stream(code):
                print(chunk, end="")
            print()
            continue
        print("Chatbot: ", end="")
        for chunk in chat.stream_chat():
            print(chunk, end="")
        print()


