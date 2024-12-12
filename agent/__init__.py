from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Generator
from model import ChatModel


class Agent(ABC):
    def __init__(self, name: str, chat: ChatModel, prompt: str, open_history: bool = False):
        self.name = name
        self.chat = chat
        self.prompt = prompt
        self.open_history = open_history
        self.prompt_copy = deepcopy(self.prompt)

    @abstractmethod
    def call_tool_before_chat(self) -> str:
        pass

    @abstractmethod
    def call_tool_after_chat(self, chat_result: str) -> str:
        pass

    def set_prompt_variable(self, name: str, value: str):
        self.prompt_copy= self.prompt_copy.replace(f"{{{{{name}}}}}", value)

    def reset(self):
        self.chat.reset()

    def execute(self) -> str:
        if not self.open_history:
            self.chat.reset()

        chat_before = self.call_tool_before_chat()
        if chat_before:
            self.chat.prompt(chat_before)

        self.chat.prompt(self.prompt_copy)

        result = self.chat.chat()

        chat_after = self.call_tool_after_chat(result)
        result = chat_after if chat_after else result
        self.prompt_copy = deepcopy(self.prompt)
        return result

    def execute_stream(self) -> Generator[str, None, None]:
        if not self.open_history:
            self.chat.reset()
        chat_before = self.call_tool_before_chat()
        if chat_before:
            self.chat.prompt(chat_before)

        self.chat.prompt(self.prompt_copy)
        chat_generate = self.chat.stream_chat()
        self.prompt_copy = deepcopy(self.prompt)
        return chat_generate
