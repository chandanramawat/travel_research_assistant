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
from tools.flight_tool import search_flights
from dotenv import load_dotenv

load_dotenv()

# Initialize LLM
llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)

# Initialize Tavily
tavily = TavilySearch(max_results=3)


# NEW: pulled out of supervisor_node so main.py can reuse the same
# classification logic to know tool_used BEFORE streaming starts
# (needed to send it as a response header).
def classify_intent(question: str) -> str:
    q = question.lower()
    flight_keywords = ["flight", "flights", "fly from", "airfare", "plane ticket", "air ticket"]
    itinerary_keywords = ["itinerary", "day plan", "days in", "day trip", "trip plan", "plan a trip", "plan my trip"]
    weather_keywords = ["weather", "temperature", "climate", "rain", "humid"]

    if any(word in q for word in flight_keywords):
        return "flight"
    elif any(word in q for word in itinerary_keywords):
        return "itinerary"
    elif any(word in q for word in weather_keywords):
        return "weather"
    return "research"


# Node 1 - Supervisor
def supervisor_node(state: AgentState) -> AgentState:
    print(f"\n[Supervisor] Question: {state['question']}")
    tool_used = classify_intent(state["question"])
    print(f"[Supervisor] -> tool_used: {tool_used}")
    return {**state, "tool_used": tool_used}


# Node 2 - Research Agent
def research_node(state: AgentState) -> AgentState:
    print(f"\n[Research Agent] Searching: {state['question']}")
    try:
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


# Node - Flight Agent
def flight_node(state: AgentState) -> AgentState:
    print(f"\n[Flight Agent] Question: {state['question']}")

    messages = [
        SystemMessage(content=(
            "Extract flight search details from this question. "
            "Return EXACTLY in this format, nothing else, no explanation: "
            "DEPARTURE_IATA|ARRIVAL_IATA|YYYY-MM-DD\n"
            "Use the 3-letter IATA airport code for the cities mentioned "
            "(e.g. Delhi=DEL, Mumbai=BOM, Jodhpur=JDH, Jaipur=JAI, Goa=GOI, "
            "Udaipur=UDR, Bangalore=BLR, Chennai=MAA, Kolkata=CCU, Hyderabad=HYD, "
            "Ahmedabad=AMD, Pune=PNQ). "
            "If no date is mentioned, use a date 30 days from today. "
            "Example: 'flight from Jodhpur to Delhi' -> 'JDH|DEL|2026-09-02'"
        )),
        HumanMessage(content=state["question"])
    ]
    extraction = llm.invoke(messages).content.strip()
    print(f"[Flight Agent] Extracted: {extraction}")

    try:
        departure_id, arrival_id, outbound_date = extraction.split("|")
        flight_result = search_flights.invoke({
            "departure_id": departure_id.strip(),
            "arrival_id": arrival_id.strip(),
            "outbound_date": outbound_date.strip(),
        })
        print(f"[Flight Agent] Result: {flight_result[:200]}")
    except Exception as e:
        flight_result = f"Could not understand the flight search request: {e}"
        print(f"[Flight Agent] Error: {e}")

    return {**state, "research_result": flight_result}


# Node 4 - Synthesizer
def synthesizer_node(state: AgentState) -> AgentState:
    print(f"\n[Synthesizer] Creating final answer...")
    tool_used = state.get("tool_used")

    if tool_used == "weather":
        context = state.get("weather_result", "")
    else:
        context = state.get("research_result", "")

    history = state.get("messages", [])[:-1][-6:]

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
    elif tool_used == "flight":
        system_prompt = (
            "You are a helpful travel assistant. Present the flight search "
            "results clearly as a short list, one flight option per line "
            "(airline, price, stops, duration). If the data contains an "
            "error or no results, say so plainly and suggest the user check "
            "the city names or date. Do not invent prices that are not in "
            "the data provided."
        )
    else:
        system_prompt = (
            "You are a helpful travel assistant. Directly answer the user's "
            "CURRENT question first and foremost. Only use the conversation "
            "history to fill in missing details the current question relies "
            "on (like a name, city, or group size mentioned earlier) or to "
            "resolve references like 'it' or 'that place'. Do not bring up "
            "or continue earlier unrelated topics (like a previous trip or "
            "search) unless the current question is actually about them."
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
    tool_used = state.get("tool_used")
    if tool_used == "weather":
        return "weather_agent"
    elif tool_used == "flight":
        return "flight_agent"
    return "research_agent"


# Build graph
def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("research_agent", research_node)
    graph.add_node("weather_agent", weather_node)
    graph.add_node("flight_agent", flight_node)
    graph.add_node("synthesizer", synthesizer_node)
    graph.set_entry_point("supervisor")
    graph.add_conditional_edges(
        "supervisor",
        route_after_supervisor,
        {
            "weather_agent": "weather_agent",
            "flight_agent": "flight_agent",
            "research_agent": "research_agent",
        }
    )
    graph.add_edge("research_agent", "synthesizer")
    graph.add_edge("weather_agent", "synthesizer")
    graph.add_edge("flight_agent", "synthesizer")
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