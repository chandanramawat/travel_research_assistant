# import uuid
# import streamlit as st
# import requests

# st.set_page_config(
#     page_title="AI Travel Planner",
#     page_icon="✈️",
#     layout="centered"
# )

# # Custom CSS
# st.markdown("""
# <style>
#     .main { background-color: #0f1117; }
#     .title { text-align: center; font-size: 2.5rem; font-weight: bold; color: #ffffff; padding: 1rem 0; }
#     .subtitle { text-align: center; color: #888; margin-bottom: 2rem; }
#     .tool-badge-weather { background: #1a3a2a; color: #4caf50; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; display: inline-block; margin: 4px; }
#     .tool-badge-research { background: #1a2a3a; color: #2196f3; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; display: inline-block; margin: 4px; }
#     .tool-badge-itinerary { background: #2a1a3a; color: #b388ff; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; display: inline-block; margin: 4px; }
#     .tool-badge-none { background: #2a2a1a; color: #ff9800; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; display: inline-block; margin: 4px; }
#     .agent-flow { background: #1a1a2e; border: 1px solid #333; border-radius: 10px; padding: 10px; margin: 8px 0; font-size: 0.8rem; color: #aaa; }
# </style>
# """, unsafe_allow_html=True)

# # Header
# st.markdown('<div class="title">AI Travel Research Assistant</div>', unsafe_allow_html=True)
# st.markdown('<div class="subtitle">Powered by Groq + LangGraph + Real-time Tools</div>', unsafe_allow_html=True)

# BACKEND_URL = "https://travel-research-assistant.onrender.com/ask/stream"

# # Sidebar
# with st.sidebar:
#     st.markdown("## Agent System")
#     st.markdown("""
#     **How it works:**

#     1. **Supervisor Agent**
#        Decides which agent to call

#     2. **Weather Agent**
#        Fetches real-time weather

#     3. **Research Agent**
#        Searches web via Tavily

#     4. **Synthesizer**
#        Creates final answer
#     """)

#     st.divider()
#     st.markdown("## Tools Available")
#     st.success("OpenWeatherMap")
#     st.info("Tavily Web Search")

#     st.divider()
#     st.markdown("## Try asking:")
#     st.code("Weather in Jaipur?")
#     st.code("Best places in Udaipur")
#     st.code("Top 5 news today")
#     st.code("Plan a trip to Goa")
#     st.code("3 day itinerary for Udaipur")

# if "session_id" not in st.session_state:
#     st.session_state.session_id = str(uuid.uuid4())

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.write(message["content"])

#         if message["role"] == "assistant":
#             tool_used = message.get("tool_used", "none")

#             if tool_used == "weather":
#                 st.markdown('<span class="tool-badge-weather">Weather Tool used</span>', unsafe_allow_html=True)
#             elif tool_used == "research":
#                 st.markdown('<span class="tool-badge-research">Tavily Search used</span>', unsafe_allow_html=True)
#             elif tool_used == "itinerary":
#                 st.markdown('<span class="tool-badge-itinerary">Itinerary Planner used</span>', unsafe_allow_html=True)
#             else:
#                 st.markdown('<span class="tool-badge-none">Direct LLM</span>', unsafe_allow_html=True)

# user_input = st.chat_input("Ask about any travel destination...")

# if user_input:

#     with st.chat_message("user"):
#         st.write(user_input)

#     st.session_state.messages.append({
#         "role": "user",
#         "content": user_input
#     })

#     with st.chat_message("assistant"):

#         # NEW: streaming — tokens are requested with stream=True, and
#         # st.write_stream() displays them as they arrive (typewriter
#         # effect) instead of waiting for the full answer.
#         try:
#             api_response = requests.post(
#                 BACKEND_URL,
#                 json={
#                     "message": user_input,
#                     "session_id": st.session_state.session_id,
#                 },
#                 stream=True,
#                 timeout=60
#             )
#             # Headers arrive before the body starts streaming, so this
#             # is available immediately even though the answer text
#             # below hasn't been read yet.
#             tool_used = api_response.headers.get("X-Tool-Used", "none")

#             def token_stream():
#                 for chunk in api_response.iter_content(chunk_size=None, decode_unicode=True):
#                     if chunk:
#                         yield chunk

#             answer = st.write_stream(token_stream())

#         except requests.exceptions.Timeout:
#             st.error("Timeout!")
#             answer    = "Timeout error"
#             tool_used = "none"

#         except Exception as e:
#             st.error(f"Error: {e}")
#             answer    = "Something went wrong!"
#             tool_used = "none"

#         if tool_used == "weather":
#             st.markdown('<span class="tool-badge-weather">Weather Tool used</span>', unsafe_allow_html=True)
#         elif tool_used == "research":
#             st.markdown('<span class="tool-badge-research">Tavily Search used</span>', unsafe_allow_html=True)
#         elif tool_used == "itinerary":
#             st.markdown('<span class="tool-badge-itinerary">Itinerary Planner used</span>', unsafe_allow_html=True)
#         else:
#             st.markdown('<span class="tool-badge-none">Direct LLM</span>', unsafe_allow_html=True)

#     st.session_state.messages.append({
#         "role": "assistant",
#         "content": answer,
#         "tool_used": tool_used
#     })
import uuid
import streamlit as st
import requests

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="centered"
)

# ---------------------------------------------------------------------------
# Theme: light lavender background + purple→blue gradient accent
# (inspired by dSilo's marketing site palette)
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    :root {
        --bg-primary: #FAFAFF;
        --bg-card: #FFFFFF;
        --bg-soft: #F3F0FC;
        --border-soft: #E6E1F7;
        --text-primary: #17151F;
        --text-secondary: #6B7280;
        --accent-purple: #7C3AED;
        --accent-purple-dark: #6D28D9;
        --accent-blue: #3B82F6;
        --gradient: linear-gradient(90deg, #7C3AED 0%, #3B82F6 100%);
    }

    .stApp, .main {
        background-color: var(--bg-primary);
    }

    /* Header */
    .title {
        text-align: center;
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: var(--text-primary);
        padding: 1.2rem 0 0.3rem 0;
    }
    .title .accent {
        background: var(--gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .subtitle {
        text-align: center;
        color: var(--text-secondary);
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-card);
        border-right: 1px solid var(--border-soft);
    }
    section[data-testid="stSidebar"] * {
        color: var(--text-primary) !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: var(--border-soft) !important;
    }

    /* st.success / st.info pills in sidebar -> soft purple/blue cards */
    section[data-testid="stSidebar"] div[data-testid="stAlertContainer"] {
        border-radius: 10px;
        border: 1px solid var(--border-soft);
    }
    section[data-testid="stSidebar"] div[data-baseweb="notification"] {
        background-color: var(--bg-soft) !important;
        border-radius: 10px;
    }

    /* st.code blocks in sidebar */
    section[data-testid="stSidebar"] code {
        background-color: var(--bg-soft) !important;
        color: var(--accent-purple-dark) !important;
        border: 1px solid var(--border-soft);
    }

    /* Chat messages */
    div[data-testid="stChatMessage"] {
        background-color: var(--bg-card);
        border: 1px solid var(--border-soft);
        border-radius: 14px;
        padding: 0.4rem 0.6rem;
    }
    div[data-testid="stChatMessage"] p, div[data-testid="stChatMessage"] li {
        color: var(--text-primary) !important;
    }

    /* Chat input */
    div[data-testid="stChatInput"] {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-soft) !important;
        border-radius: 999px !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: var(--text-primary) !important;
    }
    div[data-testid="stChatInput"] button {
        background: var(--gradient) !important;
        border-radius: 999px !important;
    }

    /* Generic buttons -> solid purple pill, matching "Request a demo" */
    .stButton>button {
        background: var(--gradient);
        color: #ffffff;
        border: none;
        border-radius: 999px;
        padding: 0.5rem 1.4rem;
        font-weight: 600;
    }
    .stButton>button:hover {
        opacity: 0.9;
    }

    /* Tool badges (soft pill chips on light bg) */
    .tool-badge-weather { background: #E4F5EA; color: #1E8E5A; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; display: inline-block; margin: 4px; font-weight: 600; }
    .tool-badge-research { background: #E5EEFF; color: #2563EB; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; display: inline-block; margin: 4px; font-weight: 600; }
    .tool-badge-itinerary { background: #F1E7FF; color: #7C3AED; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; display: inline-block; margin: 4px; font-weight: 600; }
    .tool-badge-none { background: #F1F1F4; color: #6B7280; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; display: inline-block; margin: 4px; font-weight: 600; }

    .agent-flow { background: var(--bg-soft); border: 1px solid var(--border-soft); border-radius: 10px; padding: 10px; margin: 8px 0; font-size: 0.8rem; color: var(--text-secondary); }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(
    '<div class="title">AI Travel <span class="accent">Research Assistant</span></div>',
    unsafe_allow_html=True
)
st.markdown('<div class="subtitle">Powered by Groq + LangGraph + Real-time Tools</div>', unsafe_allow_html=True)

BACKEND_URL = "https://travel-research-assistant.onrender.com/ask/stream"

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
    st.code("3 day itinerary for Udaipur")

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
            elif tool_used == "itinerary":
                st.markdown('<span class="tool-badge-itinerary">Itinerary Planner used</span>', unsafe_allow_html=True)
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

        # tokens are requested with stream=True, and st.write_stream()
        # displays them as they arrive (typewriter effect) instead of
        # waiting for the full answer.
        try:
            api_response = requests.post(
                BACKEND_URL,
                json={
                    "message": user_input,
                    "session_id": st.session_state.session_id,
                },
                stream=True,
                timeout=60
            )
            # Headers arrive before the body starts streaming, so this
            # is available immediately even though the answer text
            # below hasn't been read yet.
            tool_used = api_response.headers.get("X-Tool-Used", "none")

            def token_stream():
                for chunk in api_response.iter_content(chunk_size=None, decode_unicode=True):
                    if chunk:
                        yield chunk

            answer = st.write_stream(token_stream())

        except requests.exceptions.Timeout:
            st.error("Timeout!")
            answer    = "Timeout error"
            tool_used = "none"

        except Exception as e:
            st.error(f"Error: {e}")
            answer    = "Something went wrong!"
            tool_used = "none"

        if tool_used == "weather":
            st.markdown('<span class="tool-badge-weather">Weather Tool used</span>', unsafe_allow_html=True)
        elif tool_used == "research":
            st.markdown('<span class="tool-badge-research">Tavily Search used</span>', unsafe_allow_html=True)
        elif tool_used == "itinerary":
            st.markdown('<span class="tool-badge-itinerary">Itinerary Planner used</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="tool-badge-none">Direct LLM</span>', unsafe_allow_html=True)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "tool_used": tool_used
    })