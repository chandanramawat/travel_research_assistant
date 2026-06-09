# backend/main.py
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_tavily import TavilySearch
from langchain_groq import ChatGroq
from tools.weather_tool import get_weather
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Travel Research Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
)

# Initialize tools
tavily = TavilySearch(max_results=3)

# Bind tools
llm_with_tools = llm.bind_tools([get_weather, tavily])

# ✅ Verify
print(f"\n✅ Tool 1: {get_weather.name}")
print(f"✅ Tool 2: {tavily.name}\n")

# Models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    tool_used: str = "none"
    tool_args: dict = {}

@app.get("/")
def health_check():
    return {"status": "running"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = llm.invoke(request.message)
    return ChatResponse(response=response.content)

@app.post("/ask", response_model=ChatResponse)
def ask(request: ChatRequest):

    messages = [
        SystemMessage(content=(
            "You are a helpful travel assistant. "
            "You have two tools:\n"
            "1. get_weather: ALWAYS use this for weather/temperature questions\n"
            "2. tavily_search_results_json: ALWAYS use this for places/travel questions\n"
            "NEVER say you lack real time data. ALWAYS use tools."
        )),
        HumanMessage(content=request.message)
    ]

    response = llm_with_tools.invoke(messages)

    # ✅ Debug
    print(f"\n{'='*40}")
    print(f"Question   : {request.message}")
    print(f"Tool calls : {response.tool_calls}")
    print(f"{'='*40}\n")

    if response.tool_calls:
        tool_call = response.tool_calls[0]
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        print(f"Tool used  : {tool_name}")
        print(f"Tool args  : {tool_args}")

        # Weather tool
        if tool_name == "get_weather":
            tool_result = get_weather.invoke(tool_args)

        # Tavily tool
        elif tool_name == "tavily_search":
            results = tavily.invoke(tool_args["query"])
            tool_result = "\n".join([
                f"Source: {r['url']}\n{r['content'][:200]}"
                for r in results
            ])
        else:
            tool_result = "Tool not found"

        print(f"Tool result: {str(tool_result)[:150]}\n")

        # Final answer
        final_messages = [
            SystemMessage(content="You are a helpful travel assistant."),
            HumanMessage(content=request.message),
            HumanMessage(content=f"Tool result:\n{tool_result}")
        ]
        final_response = llm.invoke(final_messages)

        return ChatResponse(
            response=final_response.content,
            tool_used=tool_name,
            tool_args=tool_args
        )

    print("❌ No tool called!")
    return ChatResponse(
        response=response.content,
        tool_used="none",
        tool_args={}
    )