import uuid
import streamlit as st
import requests

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .title { text-align: center; font-size: 2.5rem; font-weight: bold; color: #ffffff; padding: 1rem 0; }
    .subtitle { text-align: center; color: #888; margin-bottom: 2rem; }
    .tool-badge-weather { background: #1a3a2a; color: #4caf50; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; display: inline-block; margin: 4px; }
    .tool-badge-research { background: #1a2a3a; color: #2196f3; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; display: inline-block; margin: 4px; }
    .tool-badge-none { background: #2a2a1a; color: #ff9800; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; display: inline-block; margin: 4px; }
    .agent-flow { background: #1a1a2e; border: 1px solid #333; border-radius: 10px; padding: 10px; margin: 8px 0; font-size: 0.8rem; color: #aaa; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="title">AI Travel Research Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Powered by Groq + LangGraph + Real-time Tools</div>', unsafe_allow_html=True)

BACKEND_URL = "https://travel-research-assistant.onrender.com/ask"

# Sidebar
with st.sidebar:
    st.markdown("## Agent System")
    st.markdown("""
    **How it works:**

    1. **Supervisor Agent**
       Decides which agent to call

    2. **Weather Agent**
       Fetches real-time weather

    3. **Research Agent**
       Searches web via Tavily

    4. **Synthesizer**
       Creates final answer
    """)

    st.divider()
    st.markdown("## Tools Available")
    st.success("OpenWeatherMap")
    st.info("Tavily Web Search")

    st.divider()
    st.markdown("## Try asking:")
    st.code("Weather in Jaipur?")
    st.code("Best places in Udaipur")
    st.code("Top 5 news today")
    st.code("Plan a trip to Goa")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message["role"] == "assistant":
            tool_used = message.get("tool_used", "none")

            if tool_used == "weather":
                st.markdown('<span class="tool-badge-weather">Weather Tool used</span>', unsafe_allow_html=True)
            elif tool_used == "research":
                st.markdown('<span class="tool-badge-research">Tavily Search used</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="tool-badge-none">Direct LLM</span>', unsafe_allow_html=True)

user_input = st.chat_input("Ask about any travel destination...")

if user_input:

    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("assistant"):

        with st.status("Agents working...", expanded=True) as status:
            st.write("Supervisor deciding...")

            try:
                api_response = requests.post(
                    BACKEND_URL,
                    json={
                        "message": user_input,
                        "session_id": st.session_state.session_id,
                    },
                    timeout=60
                )

                data      = api_response.json()
                answer    = data.get("response", "No response")
                tool_used = data.get("tool_used", "none")

                if tool_used == "weather":
                    st.write("Weather Agent fetching data...")
                elif tool_used == "research":
                    st.write("Research Agent searching web...")

                st.write("Synthesizer creating answer...")
                status.update(label="Done!", state="complete")

            except requests.exceptions.Timeout:
                st.error("Timeout!")
                answer    = "Timeout error"
                tool_used = "none"
                status.update(label="Failed", state="error")

            except Exception as e:
                st.error(f"Error: {e}")
                answer    = "Something went wrong!"
                tool_used = "none"
                status.update(label="Failed", state="error")

        st.write(answer)

        if tool_used == "weather":
            st.markdown('<span class="tool-badge-weather">Weather Tool used</span>', unsafe_allow_html=True)
        elif tool_used == "research":
            st.markdown('<span class="tool-badge-research">Tavily Search used</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="tool-badge-none">Direct LLM</span>', unsafe_allow_html=True)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "tool_used": tool_used
    })