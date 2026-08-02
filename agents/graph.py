# agents/graph.py
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import sqlite3
from langgraph.graph import StateGraph, END
from agents.state import AgentState
from langgraph.checkpoint.sqlite import SqliteSaver
from tools.weather_tool import get_weather
from dotenv import load_dotenv

load_dotenv()

# Initialize LLM
llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)

# Initialize Tavily
tavily = TavilySearch(max_results=3)

# Node 1 - Supervisor
def supervisor_node(state: AgentState) -> AgentState:
    print(f"\n[Supervisor] Question: {state['question']}")
    question = state["question"].lower()

    itinerary_keywords = ["itinerary", "day plan", "days in", "day trip", "trip plan", "plan a trip", "plan my trip"]
    weather_keywords = ["weather", "temperature", "climate", "rain", "humid"]

    if any(word in question for word in itinerary_keywords):
        print("[Supervisor] -> Research Agent (itinerary mode)")
        return {**state, "tool_used": "itinerary"}
    elif any(word in question for word in weather_keywords):
        print("[Supervisor] -> Weather Agent")
        return {**state, "tool_used": "weather"}
    else:
        print("[Supervisor] -> Research Agent")
        return {**state, "tool_used": "research"}


# Node 2 - Research Agent
def research_node(state: AgentState) -> AgentState:
    print(f"\n[Research Agent] Searching: {state['question']}")
    try:
        # NEW: when building an itinerary, search for attractions/things to do
        # instead of just the raw question, so the data is more useful.
        if state.get("tool_used") == "itinerary":
            search_query = f"top attractions things to do best places to visit {state['question']}"
        else:
            search_query = state["question"]

        results = tavily.invoke(search_query)

        print(f"[Research Agent] Result type: {type(results)}")
        print(f"[Research Agent] Result: {str(results)[:200]}")

        if isinstance(results, str):
            research_result = results
        elif isinstance(results, list):
            research_result = "\n".join([
                f"Source: {r['url']}\n{r['content'][:300]}"
                if isinstance(r, dict)
                else str(r)
                for r in results
            ])
        else:
            research_result = str(results)

        print(f"[Research Agent] Done!")

    except Exception as e:
        research_result = f"Search error: {e}"
        print(f"[Research Agent] Error: {e}")

    return {**state, "research_result": research_result}


# Node 3 - Weather Agent
def weather_node(state: AgentState) -> AgentState:
    print(f"\n[Weather Agent] Question: {state['question']}")

    history = state.get("messages", [])[:-1][-4:]

    messages = [
        SystemMessage(content=(
            "Extract only the city name from this question. "
            "If this question doesn't mention a city, check the conversation "
            "history and use the most recently mentioned city. "
            "Return only the city name, nothing else. "
            "Example: 'What is weather in Jaipur?' -> 'Jaipur'"
        )),
        *history,
        HumanMessage(content=state["question"])
    ]
    city = llm.invoke(messages).content.strip()
    print(f"[Weather Agent] City: {city}")
    try:
        weather_result = get_weather.invoke({"city": city})
        print(f"[Weather Agent] Result: {weather_result}")
    except Exception as e:
        weather_result = f"Weather error: {e}"
        print(f"[Weather Agent] Error: {e}")
    return {**state, "weather_result": weather_result}


# Node 4 - Synthesizer
def synthesizer_node(state: AgentState) -> AgentState:
    print(f"\n[Synthesizer] Creating final answer...")
    tool_used = state.get("tool_used")

    if tool_used == "weather":
        context = state.get("weather_result", "")
    else:
        context = state.get("research_result", "")

    history = state.get("messages", [])[:-1][-6:]

    print(f"[DEBUG] Total messages in state: {len(state.get('messages', []))}")
    print(f"[DEBUG] History being sent to LLM: {len(history)} messages")

    # NEW: different system prompt for itinerary requests, asking for a
    # structured day-by-day plan instead of a plain paragraph answer.
    if tool_used == "itinerary":
        system_prompt = (
            "You are a helpful travel assistant. Create a clear, day-by-day "
            "itinerary (Day 1, Day 2, etc.) using the research data provided. "
            "If the user specified a number of days, use that; otherwise "
            "default to a 3-day itinerary. For each day, suggest 2-3 "
            "activities or places with a short one-line note for each. "
            "Use the conversation history to remember facts the user has "
            "told you when relevant."
        )
    else:
        system_prompt = (
            "You are a helpful travel assistant. Use the conversation history "
            "to remember facts the user has told you (like their name or "
            "previously mentioned city) when relevant to answering."
        )

    messages = [
        SystemMessage(content=system_prompt),
        *history,
        HumanMessage(content=(
            f"Question: {state['question']}\n\n"
            f"Data:\n{context}"
        ))
    ]
    response = llm.invoke(messages)
    print(f"[Synthesizer] Done!")

    return {
        **state,
        "final_answer": response.content,
        "messages": [AIMessage(content=response.content)],
    }


# Routing function
def route_after_supervisor(state: AgentState) -> str:
    if state.get("tool_used") == "weather":
        return "weather_agent"
    return "research_agent"


# Build graph
def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("research_agent", research_node)
    graph.add_node("weather_agent", weather_node)
    graph.add_node("synthesizer", synthesizer_node)
    graph.set_entry_point("supervisor")
    graph.add_conditional_edges(
        "supervisor",
        route_after_supervisor,
        {
            "weather_agent": "weather_agent",
            "research_agent": "research_agent",
        }
    )
    graph.add_edge("research_agent", "synthesizer")
    graph.add_edge("weather_agent", "synthesizer")
    graph.add_edge("synthesizer", END)

    conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
    checkpointer = SqliteSaver(conn)
    return graph.compile(checkpointer=checkpointer)


_travel_graph = None

def get_travel_graph():
    """Lazy initialize the travel graph on first access"""
    global _travel_graph
    if _travel_graph is None:
        try:
            _travel_graph = build_graph()
            print("LangGraph Travel Agent ready!")
        except Exception as e:
            print(f"Error building graph: {e}")
            raise
    return _travel_graph

# Export for backward compatibility
travel_graph = get_travel_graph()