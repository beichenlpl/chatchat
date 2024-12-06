from model import ChatModel
from config import chatchat_config

chat = ChatModel(
    url=chatchat_config["model_list"][chatchat_config["current_model"]]["url"],
    api_key=chatchat_config["model_list"][chatchat_config["current_model"]]["api_key"],
    model=chatchat_config["model_list"][chatchat_config["current_model"]]["name"],
    max_tokens=chatchat_config["model_list"][chatchat_config["current_model"]]["max_tokens"],
    temperature=chatchat_config["model_list"][chatchat_config["current_model"]]["temperature"],
    top_p=chatchat_config["model_list"][chatchat_config["current_model"]]["top_p"]
)

def chat_in_cli() -> None:
    while True:
        prompt = input("User: ")
        chat.prompt(prompt)
        if prompt == "exit":
            break
        if prompt == "reset":
            chat.reset()
            continue
        print("Chatbot: ", end="")
        for chunk in chat.stream_chat():
            print(chunk, end="")
        print()

