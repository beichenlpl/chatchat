from agent.store import agent_store
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


def call_agent(code: str):
    crt_agent = agent_store.get(code)
    if crt_agent:
        name = crt_agent.get("agent").name
        print(f"调用智能体：{name}")
        if crt_agent.get("is_params"):
            question = input("User：")
            crt_agent.get("agent").set_prompt_variable(crt_agent.get("param_variable"), question)
        return crt_agent.get("agent").execute()
    else:
        return "Agent not found"




def call_agent_stream(code: str):
    crt_agent = agent_store.get(code)
    if crt_agent:
        name = crt_agent.get("agent").name
        print(f"调用智能体：{name}")
        if crt_agent.get("is_params"):
            question = input("User：")
            crt_agent.get("agent").set_prompt_variable(crt_agent.get("param_variable"), question)
        return crt_agent.get("agent").execute_stream()
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


