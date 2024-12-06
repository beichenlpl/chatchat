import uvicorn

from typing import Generator
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from config import chatchat_config
from model import ChatModel


app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str = Field(description="用户请求问题", examples=["你好"])
    stream: bool = Field(default=False, description="是否流式输出")

model = ChatModel(
    url=chatchat_config["model_list"][chatchat_config["current_model"]]["url"],
    api_key=chatchat_config["model_list"][chatchat_config["current_model"]]["api_key"],
    model=chatchat_config["model_list"][chatchat_config["current_model"]]["name"],
    max_tokens=chatchat_config["model_list"][chatchat_config["current_model"]]["max_tokens"],
    temperature=chatchat_config["model_list"][chatchat_config["current_model"]]["temperature"],
    top_p=chatchat_config["model_list"][chatchat_config["current_model"]]["top_p"]
)


async def generate_response(prompt: str) -> Generator[str, None, None]:
    model.prompt(prompt)
    for chunk in model.stream_chat():
        yield b"data: { \"message\": \"" + chunk.encode('utf-8') + b"\" }"
        yield b"\n\n"


@app.get("/reset")
async def reset() -> dict:
    model.reset()
    return {"message": "reset success"}

@app.post("/chat")
async def chat(request: ChatRequest):
    if request.stream:
        return StreamingResponse(generate_response(request.prompt), media_type='text/plain')
    else:
        model.prompt(request.prompt)
        return {"message": model.chat()}


def start_api():
    uvicorn.run(app, host="0.0.0.0", port=chatchat_config["api_port"])
