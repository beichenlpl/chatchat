import uvicorn

from typing import Generator
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from config import chatchat_config
from model import ChatModel
from agent.hotspot_extract_agent import hotspot_extract_agent


app = FastAPI()

model = ChatModel(
    url=chatchat_config["model_list"][chatchat_config["current_model"]]["url"],
    api_key=chatchat_config["model_list"][chatchat_config["current_model"]]["api_key"],
    model=chatchat_config["model_list"][chatchat_config["current_model"]]["name"],
    max_tokens=chatchat_config["model_list"][chatchat_config["current_model"]]["max_tokens"],
    temperature=chatchat_config["model_list"][chatchat_config["current_model"]]["temperature"],
    top_p=chatchat_config["model_list"][chatchat_config["current_model"]]["top_p"]
)

class ChatRequest(BaseModel):
    prompt: str = Field(description="用户请求问题", examples=["你好"])
    stream: bool = Field(default=False, description="是否流式输出")

class AgentRequest(BaseModel):
    code: str = Field(description="智能体代码", examples=["hotspot_extract"])
    question: str = Field(default="", description="用户请求问题(非必选参数)", examples=["你好"])
    stream: bool = Field(default=False, description="是否流式输出")

async def chat_generate_response(prompt: str) -> Generator[str, None, None]:
    model.prompt(prompt)
    for chunk in model.stream_chat():
        yield b"data: { \"message\": \"" + chunk.encode('utf-8') + b"\" }"
        yield b"\n\n"

async def agent_generate_response(code: str, question: str) -> Generator[str, None, None]:
    if code == "hotspot_extract":
        print(f"调用智能体：{hotspot_extract_agent.name}")
        for chunk in hotspot_extract_agent.execute_stream():
            yield b"data: { \"message\": \"" + chunk.encode('utf-8') + b"\" }"
            yield b"\n\n"
    else:
        yield b"data: { \"message\": \"Agent not found\" }"
        yield b"\n\n"

@app.get("/reset")
async def reset() -> dict:
    model.reset()
    return {"message": "reset success"}

@app.post("/chat")
async def chat(request: ChatRequest):
    print(f"请求参数：{request}")
    if request.stream:
        return StreamingResponse(chat_generate_response(request.prompt), media_type='text/plain')
    else:
        model.prompt(request.prompt)
        return {"message": model.chat()}


@app.post("/agent")
async def agent(request: AgentRequest):
    print(f"请求参数：{request}")
    if request.stream:
        return StreamingResponse(agent_generate_response(request.code, request.question), media_type='text/plain')
    else:
        return {"message": hotspot_extract_agent.execute()}



def start_api():
    uvicorn.run(app, host="0.0.0.0", port=chatchat_config["api_port"])
