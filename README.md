# ✈️ AI Travel Research Assistant

A real-world AI Agent project built with LangGraph, Groq, FastAPI, and Streamlit that answers travel questions using real-time web search and live weather data.

---

## 🚀 What It Does

- Answers travel questions using real-time web search (Tavily)
- Fetches live weather for any city (OpenWeatherMap)
- Uses LangGraph multi-agent orchestration
- FastAPI backend with REST API
- Streamlit chat UI frontend

---

## 🏗️ Architecture
User Question
↓
Streamlit Frontend (port 8501)
↓
FastAPI Backend (port 8000)
↓
LangGraph StateGraph
↓
Supervisor Agent
(decides which agent to call)
↙                    ↘
Research Agent      Weather Agent
(Tavily Search)     (OpenWeatherMap)
↘                    ↙
Synthesizer Agent
(creates final answer)
↓
Final Answer → Streamlit

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| LLM | Groq llama-3.3-70b-versatile |
| Agent Framework | LangGraph |
| LLM Framework | LangChain |
| Backend | FastAPI |
| Frontend | Streamlit |
| Search Tool | Tavily Search |
| Weather Tool | OpenWeatherMap API |
| Language | Python 3.10+ |

---

## 📁 Project Structure
travel_research_assistant/
│
├── agents/
│   ├── init.py
│   ├── state.py          # Shared AgentState (TypedDict)
│   └── graph.py          # LangGraph StateGraph — all agents
│
├── tools/
│   ├── init.py
│   ├── weather_tool.py   # OpenWeatherMap API tool
│   └── tavily_tool.py    # Tavily web search tool
│
├── backend/
│   ├── init.py
│   └── main.py           # FastAPI app — /ask endpoint
│
├── frontend/
│   └── app.py            # Streamlit chat UI
│
├── .env                  # API keys (not committed to git)
├── .gitignore
└── README.md

---

## ⚙️ Setup & Installation

### Step 1 — Clone the repo
```bash
git clone https://github.com/yourusername/travel-research-assistant.git
cd travel-research-assistant
```

### Step 2 — Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install langchain langchain-groq langchain-community langchain-tavily langgraph fastapi uvicorn streamlit python-dotenv requests
```

### Step 4 — Create `.env` file
```env
GROQ_API_KEY="your_groq_api_key"
TAVILY_API_KEY="your_tavily_api_key"
OPENWEATHER_API_KEY="your_openweather_api_key"
```

### Step 5 — Get API Keys
| API | Link | Free Tier |
|-----|------|-----------|
| Groq | https://console.groq.com | ✅ Free |
| Tavily | https://app.tavily.com | ✅ Free |
| OpenWeatherMap | https://openweathermap.org/api | ✅ Free |

---

## ▶️ Run the Project

**Terminal 1 — Start Backend:**
```bash
uvicorn backend.main:app --reload --port 8000
```

**Terminal 2 — Start Frontend:**
```bash
streamlit run frontend/app.py
```

Open browser: `http://localhost:8501`

API docs: `http://localhost:8000/docs`

---

## 🤖 How Agents Work

### 1. Supervisor Agent
Reads user question and routes to correct agent:
- Weather keywords (weather, temperature, climate) → Weather Agent
- Everything else → Research Agent

### 2. Research Agent
Uses Tavily Search API to find real-time information from the web about travel destinations, news, places, restaurants, and more.

### 3. Weather Agent
Extracts city name from the question using LLM, then fetches live weather data from OpenWeatherMap API including temperature, humidity, and wind speed.

### 4. Synthesizer Agent
Takes the tool result and creates a helpful, detailed final answer for the user.

---

## 💡 Example Queries
"What is the weather in Jaipur?"
"Best places to visit in Udaipur"
"Plan a 3 day trip to Goa"
"Top restaurants in Mumbai"
"Visa requirements for Dubai"
"Top 5 news today"
"Things to do in Jodhpur"

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | travel_agent_check|
| POST | /ask | Main chat endpoint with LangGraph |

### Request format:
```json
{
  "message": "What is the weather in Jaipur?"
}
```

### Response format:
```json
{
  "response": "The weather in Jaipur is...",
  "tool_used": "weather"
}
```

---

## 🧠 LangGraph State

```python
class AgentState(TypedDict):
    question: str         # User question
    research_result: str  # Tavily search result
    weather_result: str   # OpenWeatherMap result
    final_answer: str     # Synthesized answer
    tool_used: str        # Which tool was used
```

---

---

## 🚧 Future Improvements

- [ ] Add streaming responses
- [ ] Add trip itinerary planner
- [ ] Add hotel and flight search
- [ ] Add memory to remember past conversations
- [ ] Deploy on cloud (Railway / Render)

---

## 👨‍💻 About

Built by **Chandan** as part of a 120-day AI Engineer Challenge.

This project demonstrates:
- Multi-agent AI systems with LangGraph
- Real-time data integration with external APIs
- Full-stack AI application development
- FastAPI + Streamlit integration

---
