import requests
import json
import threading
import uuid

from typing import Generator

from mini_search import MiniSearch



class ChatModel(object):
    def __init__(self, url: str, api_key, model: str, max_tokens: int, temperature: float, top_p: float, memory_enhance: bool = False, top_n: int = 3):
        self.url = url
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.messages = []
        self.mini_search = MiniSearch()
        self.memory_enhance = memory_enhance
        self.top_n = top_n
        self.__is_stop = False


    def prompt(self, prompt: str):
        if len(self.messages) > 10:
            self.messages.pop(0)
        if self.memory_enhance:
            for item in self.mini_search.index("__model_chat_history_index__").search(prompt, page=0, limit=self.top_n):
                self.messages.append({"role": "assistant", "content": item["data"]})
        self.messages.append({"role": "user", "content": prompt})

    def reset(self):
        self.messages = []
        self.__is_stop = True
        if self.memory_enhance:
            self.mini_search.index("__model_chat_history_index__").drop()

    def chat(self) -> str:
        response = self.__request(False)
        content = response.json()["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": content})
        if self.memory_enhance:
            threading.Thread(target=self.mini_search.index("__model_chat_history_index__").create, args=(uuid.uuid4().hex, content)).start()
        return content

    def stream_chat(self) -> Generator[str, None, None]:
        response = self.__request(True)
        content = ""
        for line in response.iter_lines():
            if line:
                data_line = line.decode('utf-8')[6:]
                if data_line == "[DONE]" or self.__is_stop:
                    self.__is_stop = False
                    break
                chunk = json.loads(data_line)["choices"][0]["delta"].get("content")
                if chunk:
                    yield chunk
                    content += chunk
        self.messages.append({"role": "assistant", "content": content})
        if self.memory_enhance:
            threading.Thread(target=self.mini_search.index("__model_chat_history_index__").create, args=(uuid.uuid4().hex, content)).start()


    def __request(self, stream: bool):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "model": self.model,
            "messages": self.messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "stream": stream
        }
        return requests.post(self.url, headers=headers, data=json.dumps(data), stream=stream)


