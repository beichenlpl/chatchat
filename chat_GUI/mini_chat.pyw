import jieba
import requests
import json
import uuid
import threading
import os
import time
import copy
from pathlib import Path
from typing import (
    Union,
    Generator
)
from tkinter import (
    Tk,
    Label,
    Entry,
    Text,
    END,
    Button,
    Checkbutton,
    StringVar,
    IntVar,
    messagebox
)

def id_generate():
    return uuid.uuid4().hex

def file_remove(path: Path):
    if path.is_file():
        path.unlink()
    else:
        for item in path.iterdir():
            if item.is_file():
                item.unlink()
            else:
                file_remove(item)
        else:
            path.rmdir()

class MiniSearch(object):
    def __init__(self):
        self.__data_path = "search_data"
        self.__current_index = "default"

        if not os.path.exists(f"{self.__data_path}"):
            os.makedirs(f"{self.__data_path}")

    def index(self, name: str):
        self.__current_index = name
        return self

    def indexes(self):
        return os.listdir(f"{self.__data_path}")

    def create(self, doc_name: str, doc_content: str, _id: Union[int, str, None] = None):
        _id = _id if _id else id_generate()
        doc_content = doc_content.strip()
        index_path = Path(f"{self.__data_path}/{self.__current_index}")
        index_mapping_path = Path(f"{index_path}/_index")
        index_mapping = {}
        if not index_path.exists():
            index_path.mkdir()
            for i in range(1, len(doc_content) + 1):
                for j in range(0, len(doc_content), i):
                    index_mapping[doc_content[j:j + i]] = {
                        "doc_ids": [_id]
                    }

            for item in jieba.lcut(doc_content):
                if index_mapping.get(item):
                    if _id in index_mapping[item]["doc_ids"]:
                        continue
                    else:
                        index_mapping[item]["doc_ids"].append(_id)
                else:
                    index_mapping[item] = {
                        "doc_ids": [_id]
                    }

        else:
            with index_mapping_path.open("r", encoding="utf-8") as index_reader:
                index_mapping = json.loads(index_reader.read())
            for i in range(1, len(doc_content) + 1):
                for j in range(0, len(doc_content), i):
                    if index_mapping.get(doc_content[j:j + i]):
                        if _id in index_mapping[doc_content[j:j + i]]["doc_ids"]:
                            continue
                        index_mapping[doc_content[j:j + i]]["doc_ids"].append(_id)
                    else:
                        index_mapping[doc_content[j:j + i]] = {
                            "doc_ids": [_id]
                        }

                for item in jieba.lcut(doc_content):
                    if index_mapping.get(item):
                        if _id in index_mapping[item]["doc_ids"]:
                            continue
                        else:
                            index_mapping[item]["doc_ids"].append(_id)
                    else:
                        index_mapping[item] = {
                            "doc_ids": [_id]
                        }

        with index_mapping_path.open("w", encoding="utf-8") as index_writer:
            data = json.dumps(index_mapping)
            index_writer.write(data)

        doc_path = Path(f"{index_path}/docs/{_id}/data")
        if not doc_path.parent.exists():
            os.makedirs(doc_path.parent)
        with doc_path.open("w", encoding="utf-8") as doc_writer:
            data = {
                "_index": self.__current_index,
                "_name": doc_name,
                "_id": _id,
                "_length": len(doc_content),
                "data": doc_content,
                "timestamp": time.time() * 1000
            }
            doc_writer.write(json.dumps(data))

        return _id

    def drop(self) -> bool:
        index_path = Path(f"{self.__data_path}/{self.__current_index}")
        if not index_path.exists():
            return True
        if self.__current_index == "default":
            index_mapping_path = Path(f"{index_path}/_index")
            with index_mapping_path.open("w", encoding="utf-8") as index_writer:
                index_writer.write("")

            docs_path = Path(f"{index_path}/docs")
            file_remove(docs_path)
        else:
            file_remove(index_path)
        return True

    def search(self, query: str, page: int = 0, limit: int = 10, sort_by: str = "default"):
        index_path = Path(f"{self.__data_path}/{self.__current_index}")
        index_mapping_path = Path(f"{index_path}/_index")
        if not index_path.exists():
            return []
        else:
            with index_mapping_path.open("r", encoding="utf-8") as index_reader:
                index_mapping = json.loads(index_reader.read())

            if not index_mapping.get(query):
                return []
            else:
                result = []
                docs = index_mapping[query]["doc_ids"]
                for doc in docs:
                    doc_path = Path(f"{index_path}/docs/{doc}/data")
                    if doc_path.exists():
                        with doc_path.open("r", encoding="utf-8") as doc_reader:
                            data = json.loads(doc_reader.read())
                            data["_word_index"] = data["data"].find(query)
                            result.append(data)

                for item in sorted(jieba.lcut(query), key=lambda x: len(x), reverse=True):
                    if not index_mapping.get(item):
                        continue
                    else:
                        word_docs = index_mapping[item]["doc_ids"]
                        for doc in word_docs:
                            if doc in docs:
                                continue
                            else:
                                doc_path = Path(f"{index_path}/docs/{doc}/data")
                                if doc_path.exists():
                                    with doc_path.open("r", encoding="utf-8") as doc_reader:
                                        data = json.loads(doc_reader.read())
                                        data["_word_index"] = data["data"].find(item)
                                        result.append(data)

                if page is not None and limit is not None:
                    if sort_by == "default":
                        return result[page * limit:(page + 1) * limit]
                    elif sort_by == "timestamp":
                        return sorted(result, key=lambda x: x["timestamp"], reverse=True)[page * limit:(page + 1) * limit]
                else:
                    if sort_by == "default":
                        return result
                    elif sort_by == "timestamp":
                        return sorted(result, key=lambda x: x["timestamp"], reverse=True)

    def add(self, doc_name: str, doc_content: str, _id: Union[int, str, None] = None):
        return self.create(doc_name, doc_content, _id), self

    def get(self, _id: Union[int, str]):
        index_path = Path(f"{self.__data_path}/{self.__current_index}")
        doc_path = Path(f"{index_path}/docs/{_id}/data")
        if doc_path.exists():
            with doc_path.open("r", encoding="utf-8") as doc_reader:
                return json.loads(doc_reader.read())
        else:
            return None

    def set(self, doc_name: str, doc_content: str, _id: Union[int, str]):
        return self.create(doc_name, doc_content, _id)

    def delete(self, _id: Union[int, str]):
        index_path = Path(f"{self.__data_path}/{self.__current_index}")
        index_mapping_path = Path(f"{index_path}/_index")
        with index_mapping_path.open("r", encoding="utf-8") as index_reader:
            index_mapping = json.loads(index_reader.read())

        index_mapping_copy = copy.deepcopy(index_mapping)
        for key in index_mapping_copy.keys():
            if _id in index_mapping[key]["doc_ids"]:
                index_mapping[key]["doc_ids"].remove(_id)
            if len(index_mapping[key]["doc_ids"]) == 0:
                del index_mapping[key]

        del index_mapping_copy

        with index_mapping_path.open("w", encoding="utf-8") as index_writer:
            index_writer.write(json.dumps(index_mapping))

        doc_path = Path(f"{index_path}/docs/{_id}")
        return file_remove(doc_path)


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


    def prompt(self, prompt: str):
        if len(self.messages) > 10:
            self.messages.pop(0)
        if self.memory_enhance:
            for item in self.mini_search.index("__model_chat_history_index__").search(prompt, page=0, limit=self.top_n):
                self.messages.append({"role": "assistant", "content": item["data"]})
        self.messages.append({"role": "user", "content": prompt})

    def reset(self):
        self.messages = []
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
                if data_line == "[DONE]":
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


chat = ChatModel(
    url="",
    api_key="",
    model="",
    max_tokens=4096,
    temperature=0.7,
    top_p=0.95
)

# 更新模型参数
def update_model():
    chat.url = model_url_var.get()
    chat.api_key = model_api_key_var.get()
    chat.model = model_name_var.get()
    chat.max_tokens = int(max_tokens_var.get())
    chat.temperature = float(temperature_var.get())
    chat.top_p = float(top_p_var.get())
    chat.memory_enhance = memory_enhance_checkbox_var.get() == 1
    chat.top_n = int(memory_enhance_top_n_var.get())

# 新建对话
def reset():
    chat.reset()
    user_input_text.delete("1.0", END)
    model_output_text.delete("1.0", END)

def send():
    threading.Thread(target=_send).start()

def _send():
    update_model()
    prompt = user_input_text.get("1.0", END)
    if history_checkbox_var.get() != 1:
        chat.reset()
    chat.prompt(prompt)
    try:
        model_output_text.delete("1.0", END)
        for chunk in chat.stream_chat():
            model_output_text.insert(END, chunk)
            model_output_text.see(END)
    except Exception as e:
        raise e
        # messagebox.showerror("错误", "模型参数错误：" + str(e))

root = Tk()
root.title("mini chat")
root.geometry("850x800")
root.resizable(False, False)

# 模型地址
model_url_label = Label(root, text="模型地址:", font=("微软雅黑", 12))
model_url_label.place(x=10, y=10)
model_url_var = StringVar()
model_url_entry = Entry(root, textvariable=model_url_var, width=105)
model_url_entry.place(x=95, y=15)

# 模型API Key
model_api_key_label = Label(root, text="API Key:", font=("微软雅黑", 12))
model_api_key_label.place(x=10, y=50)
model_api_key_var = StringVar()
model_api_key_password_entry = Entry(root, textvariable=model_api_key_var, width=105, show="*")
model_api_key_password_entry.place(x=95, y=55)

# 模型名称
model_name_label = Label(root, text="模型名称:", font=("微软雅黑", 12))
model_name_label.place(x=10, y=95)
model_name_var = StringVar()
model_name_entry = Entry(root, textvariable=model_name_var, width=105)
model_name_entry.place(x=95, y=95)

# 最大token
max_tokens_label = Label(root, text="最大token:", font=("微软雅黑", 12))
max_tokens_label.place(x=10, y=130)
max_tokens_var = StringVar()
max_tokens_var.set("4096")
max_tokens_entry = Entry(root, textvariable=max_tokens_var, width=105)
max_tokens_entry.place(x=95, y=135)

# 温度
temperature_label = Label(root, text="温度:", font=("微软雅黑", 12))
temperature_label.place(x=10, y=170)
temperature_var = StringVar()
temperature_var.set("0.7")
temperature_entry = Entry(root, textvariable=temperature_var, width=105)
temperature_entry.place(x=95, y=175)

# 概率
top_p_label = Label(root, text="概率:", font=("微软雅黑", 12))
top_p_label.place(x=10, y=210)
top_p_var = StringVar()
top_p_var.set("0.95")
top_p_entry = Entry(root, textvariable=top_p_var, width=105)
top_p_entry.place(x=95, y=215)

# 是否开启历史记录
history_label = Label(root, text="历史记录:", font=("微软雅黑", 12))
history_label.place(x=10, y=250)
history_checkbox_var = IntVar()
history_checkbox = Checkbutton(root, variable=history_checkbox_var)
history_checkbox.place(x=80, y=255)

# 是否开启记忆增强
memory_enhance_label = Label(root, text="记忆增强:", font=("微软雅黑", 12))
memory_enhance_label.place(x=125, y=250)
memory_enhance_checkbox_var = IntVar()
memory_enhance_checkbox = Checkbutton(root, variable=memory_enhance_checkbox_var)
memory_enhance_checkbox.place(x=200, y=255)

# 记忆增强top_n
memory_enhance_top_n_label = Label(root, text="记忆增强top_n:", font=("微软雅黑", 12))
memory_enhance_top_n_label.place(x=245, y=250)
memory_enhance_top_n_var = StringVar()
memory_enhance_top_n_var.set("3")
memory_enhance_top_n_entry = Entry(root, textvariable=memory_enhance_top_n_var, width=30)
memory_enhance_top_n_entry.place(x=370, y=255)

# 用户输入
user_input_label = Label(root, text="用户输入:", font=("微软雅黑", 12))
user_input_label.place(x=10, y=290)
user_input_text = Text(root, width=90, height=10)
user_input_text.place(x=95, y=295)

# 模型输出
model_output_label = Label(root, text="模型输出:", font=("微软雅黑", 12))
model_output_label.place(x=10, y=440)
model_output_text = Text(root, width=105, height=20)
model_output_text.place(x=95, y=445)


# 发送按钮
send_button = Button(root, text="发送", font=("微软雅黑", 12), width=8, height=1, command=send)
send_button.place(x=750, y=290)
# 重置按钮
reset_button = Button(root, text="重置", font=("微软雅黑", 12), width=8, height=1, command=reset)
reset_button.place(x=750, y=340)


root.mainloop()