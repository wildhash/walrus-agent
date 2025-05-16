from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from create_agent import create_agent
from langchain_core.messages import HumanMessage

class ChatRequest(BaseModel):
    prompt: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

agent_executor, config = create_agent()

@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    async def stream_response():
        for chunk in agent_executor.stream({"messages": [HumanMessage(content=req.prompt)]}, config):
            if "agent" in chunk:
                yield f"data: {chunk['agent']['messages'][0].content}\n\n"
            elif "tools" in chunk:
                yield f"data: {chunk['tools']['messages'][0].content}\n\n"
    return StreamingResponse(stream_response(), media_type="text/event-stream")

@app.post("/chat")
async def chat(req: ChatRequest):
    full = ""
    for chunk in agent_executor.stream({"messages": [HumanMessage(content=req.prompt)]}, config):
        if "agent" in chunk:
            full += chunk["agent"]["messages"][0].content
        elif "tools" in chunk:
            full += chunk["tools"]["messages"][0].content
    return {"response": full}
