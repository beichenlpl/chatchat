import requests
import json

from typing import Generator


class ChatModel(object):
    def __init__(self, url: str, api_key, model: str, max_tokens: int, temperature: float, top_p: float):
        self.url = url
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.messages = []

    def prompt(self, prompt: str):
        if len(self.messages) > 10:
            self.messages.pop(0)
        self.messages.append({"role": "user", "content": prompt})

    def reset(self):
        self.messages = []

    def chat(self) -> str:
        response = self.__request(False)
        content = response.json()["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": content})
        return content

    def stream_chat(self) -> Generator[str, None, None]:
        response = self.__request(True)
        content = ""
        for line in response.iter_lines():
            if line:
                data_line = line.decode('utf-8')[6:]
                if data_line == "[DONE]":
                    break
                chunk = json.loads(data_line)["choices"][0]["delta"]["content"]
                yield chunk
                content += chunk
        self.messages.append({"role": "assistant", "content": content})


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


