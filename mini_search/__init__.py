import json
import jieba
import time
import uuid
import os
import copy
from pathlib import Path
from typing import Union

from config import chatchat_config


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
        self.__data_path = chatchat_config["mini_search"]["data"]
        self.__current_index = chatchat_config["mini_search"]["default_index"]

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
        if self.__current_index == chatchat_config["mini_search"]["default_index"]:
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
