from model import ChatModel
from typing import Callable, Generator
from abc import ABC, abstractmethod


class Agent(ABC):
    def __init__(self, name: str, chat: ChatModel, prompt: str, open_history: bool = False):
        self.name = name
        self.chat = chat
        self.prompt = prompt
        self.open_history = open_history

    @abstractmethod
    def call_tool_before_chat(self) -> str:
        pass

    @abstractmethod
    def call_tool_after_chat(self, chat_result: str) -> str:
        pass

    def set_prompt_variable(self, name: str, value: str):
        self.prompt = self.prompt.replace(f"{{{{{name}}}}}", value)

    def execute(self) -> str:
        if not self.open_history:
            self.chat.reset()

        chat_before = self.call_tool_before_chat()
        if chat_before:
            self.chat.prompt(chat_before)

        self.chat.prompt(self.prompt)

        result = self.chat.chat()

        chat_after = self.call_tool_after_chat(result)

        return chat_after if chat_after else result

    def execute_stream(self) -> Generator[str, None, None]:
        if not self.open_history:
            self.chat.reset()
        chat_before = self.call_tool_before_chat()
        if chat_before:
            self.chat.prompt(chat_before)

        self.chat.prompt(self.prompt)

        return self.chat.stream_chat()
