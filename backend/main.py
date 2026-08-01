from agents.graph import travel_graph
from pydantic import BaseModel
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()
app = FastAPI(title="AI travel assistant")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"]
)


# MODELS
# validates request using pydantic base model
class ChatRequest(BaseModel):
    message: str
    # identifies which conversation this message belongs to, so the
    # checkpointer inside graph.py knows whose history to load and save.
    # The frontend will generate one per browser session and reuse it.
    session_id: str = "default-session"


# validate response using pydantic base model
class ChatResponse(BaseModel):
    response: str
    tool_used: str = "none"


@app.get("/")
def query_check():
    return {"status": "running", "app": "AI travel research Assistant"}


# LangGraph connected
@app.post("/ask", response_model=ChatResponse)
def ask(request: ChatRequest):
    print(f"\nRequest: {request.message}")

    # thread_id tells the checkpointer which conversation's history
    # to load before this run, and where to save it after.
    config = {"configurable": {"thread_id": request.session_id}}

    result = travel_graph.invoke(
        {
            "messages": [("user", request.message)],  # merged into saved history by add_messages
            "question": request.message,
            "research_result": "",
            "weather_result": "",
            "final_answer": "",
            "tool_used": ""
        },
        config=config,  # this is what actually connects the call to memory
    )

    print(f"Done! Tool used: {result['tool_used']}")

    return ChatResponse(
        response=result["final_answer"],
        tool_used=result["tool_used"]
    )