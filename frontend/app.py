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

# import uuid
# import streamlit as st
# import requests

# st.set_page_config(
#     page_title="AI Travel Planner",
#     page_icon="✈️",
#     layout="centered"
# )

# # ---------------------------------------------------------------------------
# # Theme: light lavender background + purple→blue gradient accent
# # (inspired by dSilo's marketing site palette)
# # ---------------------------------------------------------------------------
# st.markdown("""
# <style>
#     :root {
#         --bg-primary: #FAFAFF;
#         --bg-card: #FFFFFF;
#         --bg-soft: #F3F0FC;
#         --border-soft: #E6E1F7;
#         --text-primary: #17151F;
#         --text-secondary: #6B7280;
#         --accent-purple: #7C3AED;
#         --accent-purple-dark: #6D28D9;
#         --accent-blue: #3B82F6;
#         --gradient: linear-gradient(90deg, #7C3AED 0%, #3B82F6 100%);
#     }

#     .stApp, .main {
#         background-color: var(--bg-primary);
#     }

#     /* Header */
#     .title {
#         text-align: center;
#         font-size: 2.6rem;
#         font-weight: 800;
#         letter-spacing: -0.02em;
#         color: var(--text-primary);
#         padding: 1.2rem 0 0.3rem 0;
#     }
#     .title .accent {
#         background: var(--gradient);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         background-clip: text;
#     }
#     .subtitle {
#         text-align: center;
#         color: var(--text-secondary);
#         font-size: 0.95rem;
#         margin-bottom: 2rem;
#     }

#     /* Sidebar */
#     section[data-testid="stSidebar"] {
#         background-color: var(--bg-card);
#         border-right: 1px solid var(--border-soft);
#     }
#     section[data-testid="stSidebar"] * {
#         color: var(--text-primary) !important;
#     }
#     section[data-testid="stSidebar"] hr {
#         border-color: var(--border-soft) !important;
#     }

#     /* st.success / st.info pills in sidebar -> soft purple/blue cards */
#     section[data-testid="stSidebar"] div[data-testid="stAlertContainer"] {
#         border-radius: 10px;
#         border: 1px solid var(--border-soft);
#     }
#     section[data-testid="stSidebar"] div[data-baseweb="notification"] {
#         background-color: var(--bg-soft) !important;
#         border-radius: 10px;
#     }

#     /* st.code blocks in sidebar */
#     section[data-testid="stSidebar"] code {
#         background-color: var(--bg-soft) !important;
#         color: var(--accent-purple-dark) !important;
#         border: 1px solid var(--border-soft);
#     }

#     /* Chat messages */
#     div[data-testid="stChatMessage"] {
#         background-color: var(--bg-card);
#         border: 1px solid var(--border-soft);
#         border-radius: 14px;
#         padding: 0.4rem 0.6rem;
#     }
#     div[data-testid="stChatMessage"] p, div[data-testid="stChatMessage"] li {
#         color: var(--text-primary) !important;
#     }

#     /* Chat input */
#     div[data-testid="stChatInput"] {
#         background-color: var(--bg-card) !important;
#         border: 1px solid var(--border-soft) !important;
#         border-radius: 999px !important;
#     }
#     div[data-testid="stChatInput"] textarea {
#         color: var(--text-primary) !important;
#     }
#     div[data-testid="stChatInput"] button {
#         background: var(--gradient) !important;
#         border-radius: 999px !important;
#     }

#     /* Generic buttons -> solid purple pill, matching "Request a demo" */
#     .stButton>button {
#         background: var(--gradient);
#         color: #ffffff;
#         border: none;
#         border-radius: 999px;
#         padding: 0.5rem 1.4rem;
#         font-weight: 600;
#     }
#     .stButton>button:hover {
#         opacity: 0.9;
#     }

#     /* Tool badges (soft pill chips on light bg) */
#     .tool-badge-weather { background: #E4F5EA; color: #1E8E5A; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; display: inline-block; margin: 4px; font-weight: 600; }
#     .tool-badge-research { background: #E5EEFF; color: #2563EB; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; display: inline-block; margin: 4px; font-weight: 600; }
#     .tool-badge-itinerary { background: #F1E7FF; color: #7C3AED; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; display: inline-block; margin: 4px; font-weight: 600; }
#     .tool-badge-none { background: #F1F1F4; color: #6B7280; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; display: inline-block; margin: 4px; font-weight: 600; }

#     .agent-flow { background: var(--bg-soft); border: 1px solid var(--border-soft); border-radius: 10px; padding: 10px; margin: 8px 0; font-size: 0.8rem; color: var(--text-secondary); }
# </style>
# """, unsafe_allow_html=True)

# # Header
# st.markdown(
#     '<div class="title">AI Travel <span class="accent">Research Assistant</span></div>',
#     unsafe_allow_html=True
# )
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

#         # tokens are requested with stream=True, and st.write_stream()
#         # displays them as they arrive (typewriter effect) instead of
#         # waiting for the full answer.
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
    page_title="AI Travel Research Assistant",
    page_icon="✈️",
    layout="centered"
)

# ---------------------------------------------------------------------------
# Design system
# Canvas: soft violet-white · Ink: warm near-black · Accent: violet -> blue
# Display face: Sora (geometric, distinctive) · Body: Inter · Data/tags: JetBrains Mono
# Signature element: a small pipeline diagram in the hero, because that's what
# this product actually is — a supervisor agent routing to specialist agents.
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap');

:root {
    --bg: #F7F6FB;
    --surface: #FFFFFF;
    --surface-muted: #F0EDFA;
    --ink: #14121B;
    --ink-soft: #6B6478;
    --line: #E4DFF3;
    --violet: #7C3AED;
    --violet-dark: #5F27C9;
    --blue: #3E6DF6;
    --gradient: linear-gradient(90deg, var(--violet) 0%, var(--blue) 100%);
    --green: #1E9E6B;
    --green-bg: #E4F6ED;
    --blue-bg: #E8EEFF;
    --violet-bg: #F1E8FF;
    --gray-bg: #EFEDF3;
    --shadow: 0 1px 2px rgba(20,18,27,0.04), 0 10px 28px rgba(124,58,237,0.08);
    --radius-lg: 20px;
    --radius-md: 14px;
    --radius-pill: 999px;
}

html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"],
[data-testid="stMainBlockContainer"],
.main {
    background-color: var(--bg) !important;
}
[data-testid="stHeader"] { border-bottom: none; }
[data-testid="stBottom"] > div { background-color: var(--bg) !important; }

.stApp, .stApp p {
    font-family: 'Inter', sans-serif;
}

/* Avatars are rendered with an icon-ligature font (Material Symbols) by
   Streamlit itself; never touch their font-family, and clip overflow so a
   font-load hiccup can never visually collide with the message text. */
div[data-testid="stChatMessageAvatarUser"],
div[data-testid="stChatMessageAvatarAssistant"] {
    overflow: hidden;
    display: flex !important;
    align-items: center;
    justify-content: center;
}

.block-container { padding-top: 1.6rem; max-width: 760px; }
#MainMenu, footer { visibility: hidden; }

/* ---------------- Hero ---------------- */
.hero { text-align: center; padding: 1rem 0.5rem 0.5rem; }

.hero-bar {
    width: 46px;
    height: 4px;
    border-radius: 4px;
    margin: 0 auto 1.3rem;
    background: linear-gradient(90deg, var(--violet), var(--blue), var(--violet));
    background-size: 200% 100%;
    animation: bar-shift 3s ease-in-out infinite;
}
@keyframes bar-shift {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

.eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    color: var(--violet);
    text-transform: uppercase;
    margin-bottom: 0.7rem;
}

.title {
    font-family: 'Sora', sans-serif;
    font-weight: 800;
    font-size: clamp(1.9rem, 5vw, 2.7rem);
    letter-spacing: -0.02em;
    line-height: 1.15;
    color: var(--ink);
}
.title .accent {
    background: var(--gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.subtitle {
    color: var(--ink-soft);
    font-size: 0.95rem;
    margin-top: 0.5rem;
}

/* ---- Pipeline diagram: the real architecture, as the signature visual ---- */
.pipeline { margin-top: 1.8rem; display: flex; flex-direction: column; align-items: center; gap: 0.35rem; }
.pl-node {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.74rem;
    font-weight: 600;
    color: var(--ink);
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--radius-pill);
    padding: 0.4rem 1rem;
    box-shadow: var(--shadow);
    transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
}
.pl-node:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(124,58,237,0.14);
    border-color: #DCC8FA;
}
.pl-node.root { color: var(--violet-dark); border-color: #DCC8FA; }
.pl-arrow { color: var(--ink-soft); font-size: 0.85rem; line-height: 1; }
.pl-branch { display: flex; gap: 0.5rem; flex-wrap: wrap; justify-content: center; }

/* ---------------- Sidebar ---------------- */
section[data-testid="stSidebar"] {
    background-color: var(--surface);
    border-right: 1px solid var(--line);
}
section[data-testid="stSidebar"] * { color: var(--ink) !important; font-family: 'Inter', sans-serif !important; }
section[data-testid="stSidebar"] hr { border-color: var(--line) !important; }

.sb-heading {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--ink-soft) !important;
    margin: 0.2rem 0 0.9rem 0 !important;
}

/* Agent timeline (a genuine handoff sequence, so numbering is meaningful) */
.timeline { position: relative; padding-left: 1.6rem; margin-bottom: 0.4rem; }
.timeline::before {
    content: "";
    position: absolute;
    left: 0.55rem;
    top: 0.35rem;
    bottom: 0.35rem;
    width: 1px;
    background: var(--line);
}
.tl-item { position: relative; padding-bottom: 1.1rem; }
.tl-item:last-child { padding-bottom: 0; }
.tl-dot {
    position: absolute;
    left: -1.6rem;
    top: 0.15rem;
    width: 1.15rem;
    height: 1.15rem;
    border-radius: 50%;
    background: var(--surface-muted);
    border: 1px solid var(--line);
    color: var(--violet-dark);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
}
.tl-title { font-weight: 700; font-size: 0.87rem; color: var(--ink); }
.tl-desc { font-size: 0.82rem; color: var(--ink-soft); margin-top: 0.1rem; }

/* Tool chips */
.tool-chip {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    border-radius: var(--radius-md);
    padding: 0.6rem 0.8rem;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    border: 1px solid transparent;
}
.tool-chip .dot { width: 7px; height: 7px; border-radius: 50%; background: currentColor; flex-shrink: 0; }
.tool-chip-green { background: var(--green-bg); color: var(--green); }
.tool-chip-blue { background: var(--blue-bg); color: var(--blue); }

/* Sidebar suggestion buttons */
section[data-testid="stSidebar"] .stButton>button {
    background: var(--bg) !important;
    color: var(--ink) !important;
    border: 1px solid var(--line) !important;
    border-radius: 12px !important;
    text-align: left !important;
    justify-content: flex-start !important;
    width: 100%;
    min-height: 2.7rem;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    padding: 0.6rem 1rem !important;
    box-shadow: none !important;
    margin-bottom: 0.45rem;
    position: relative;
    transition: transform .15s ease, border-color .15s ease, color .15s ease,
                background .15s ease, box-shadow .15s ease, padding-right .15s ease;
}
section[data-testid="stSidebar"] .stButton>button:hover {
    background: var(--surface) !important;
    border-color: var(--violet) !important;
    color: var(--violet-dark) !important;
    box-shadow: 0 4px 14px rgba(124,58,237,0.12);
    transform: translateY(-1px);
    padding-right: 1.6rem !important;
}
section[data-testid="stSidebar"] .stButton>button:active {
    transform: translateY(0px) scale(0.98);
    box-shadow: 0 1px 4px rgba(124,58,237,0.10);
}
section[data-testid="stSidebar"] .stButton>button::after {
    content: "\2192";
    position: absolute;
    right: 0.9rem;
    top: 50%;
    transform: translate(6px, -50%);
    opacity: 0;
    transition: transform .15s ease, opacity .15s ease;
    color: var(--violet);
    font-weight: 700;
}
section[data-testid="stSidebar"] .stButton>button:hover::after {
    opacity: 1;
    transform: translate(0, -50%);
}
section[data-testid="stSidebar"] .stButton>button:focus-visible {
    outline: 2px solid var(--violet);
    outline-offset: 2px;
}

/* ---------------- Chat ---------------- */
div[data-testid="stChatMessage"] {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--radius-lg);
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.9rem;
    box-shadow: var(--shadow);
    animation: fade-up 0.3s ease;
    transition: box-shadow .2s ease, transform .2s ease;
}
div[data-testid="stChatMessage"]:hover {
    box-shadow: 0 4px 20px rgba(124,58,237,0.10);
    transform: translateY(-1px);
}
div[data-testid="stChatMessage"] p, div[data-testid="stChatMessage"] li {
    color: var(--ink) !important;
    line-height: 1.6;
    font-size: 0.95rem;
}
@keyframes fade-up {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
}

div[data-testid="stChatMessageAvatarUser"] { background: var(--ink) !important; border-radius: 50% !important; }
div[data-testid="stChatMessageAvatarAssistant"] { background: var(--gradient) !important; border-radius: 50% !important; }

div[data-testid="stChatInput"] {
    background: var(--surface) !important;
    border: 1.5px solid var(--line) !important;
    border-radius: var(--radius-pill) !important;
    box-shadow: var(--shadow);
    padding: 0.35rem 0.35rem 0.35rem 1.3rem !important;
    overflow: visible !important;
    min-height: 3.2rem;
}
div[data-testid="stChatInput"]:focus-within { border-color: var(--violet) !important; }

/* The textarea itself carries its own dark background from Streamlit's
   base theme — overriding only the wrapper (above) wasn't enough, which
   is why typed text was unreadable against a still-dark field. */
div[data-testid="stChatInput"] textarea,
div[data-testid="stChatInput"] [data-baseweb="textarea"] {
    background-color: transparent !important;
}
div[data-testid="stChatInput"] textarea {
    color: var(--ink) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    line-height: 1.5 !important;
}
div[data-testid="stChatInput"] textarea::placeholder { color: var(--ink-soft) !important; opacity: 1; }

/* Send button: solid gradient face + a contained rotating conic-gradient
   ring + soft blurred glow behind it, isolated so the negative z-index
   layers can't leak behind the page (same fix as the earlier title bug). */
div[data-testid="stChatInput"] button {
    position: relative;
    isolation: isolate;
    background: var(--gradient) !important;
    border-radius: 50% !important;
    width: 2.3rem;
    height: 2.3rem;
    min-width: 2.3rem;
    z-index: 0;
    transition: transform .15s ease;
}
div[data-testid="stChatInput"] button::before,
div[data-testid="stChatInput"] button::after {
    content: "";
    position: absolute;
    border-radius: 50%;
    background: conic-gradient(
        from 0deg,
        transparent 0%, transparent 40%,
        #ffffff 55%, #C4B5FD 65%,
        var(--violet) 78%, var(--blue) 90%,
        transparent 100%
    );
    animation: btn-glow-spin 2.4s linear infinite;
}
div[data-testid="stChatInput"] button::before { inset: -3px; z-index: -1; }
div[data-testid="stChatInput"] button::after  { inset: -7px; z-index: -2; filter: blur(7px); opacity: 0.85; }
@keyframes btn-glow-spin { to { transform: rotate(360deg); } }

div[data-testid="stChatInput"] button:hover { transform: scale(1.08); }
div[data-testid="stChatInput"] button:active { transform: scale(0.95); }
div[data-testid="stChatInput"] button svg { fill: #fff !important; }

/* Tool-used tags (mono, technical, matches the agentic product itself) */
.tag {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    padding: 0.32rem 0.7rem;
    border-radius: var(--radius-pill);
    font-weight: 600;
    margin-top: 0.5rem;
}
.tag::before { content: ""; width: 6px; height: 6px; border-radius: 50%; background: currentColor; }
.tag-weather { background: var(--green-bg); color: var(--green); }
.tag-research { background: var(--blue-bg); color: var(--blue); }
.tag-itinerary { background: var(--violet-bg); color: var(--violet-dark); }
.tag-none { background: var(--gray-bg); color: var(--ink-soft); }

.stButton>button {
    background: var(--gradient);
    color: #fff;
    border: none;
    border-radius: var(--radius-pill);
    min-height: 2.6rem;
    padding: 0.55rem 1.5rem;
    font-weight: 600;
    box-shadow: 0 2px 8px rgba(124,58,237,0.25);
    transition: transform .15s ease, box-shadow .15s ease, opacity .15s ease;
}
.stButton>button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(124,58,237,0.32);
    opacity: 0.96;
}
.stButton>button:active {
    transform: translateY(0) scale(0.98);
    box-shadow: 0 2px 6px rgba(124,58,237,0.2);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown(
    '''
    <div class="hero">
        <div class="hero-bar"></div>
        <div class="eyebrow">Real-time · Multi-agent · AI Travel Intelligence</div>
        <div class="title">AI Travel <span class="accent">Research Assistant</span></div>
        <div class="subtitle">Powered by Groq + LangGraph + real-time tools</div>
        <div class="pipeline">
            <div class="pl-node root">Supervisor Agent</div>
            <div class="pl-arrow">&#8595;</div>
            <div class="pl-branch">
                <div class="pl-node">Weather</div>
                <div class="pl-node">Research</div>
                <div class="pl-node">Itinerary</div>
            </div>
            <div class="pl-arrow">&#8595;</div>
            <div class="pl-node root">Synthesizer</div>
        </div>
    </div>
    ''',
    unsafe_allow_html=True
)

BACKEND_URL = "https://travel-research-assistant.onrender.com/ask/stream"

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sb-heading">Agent System</div>', unsafe_allow_html=True)
    st.markdown('''
    <div class="timeline">
        <div class="tl-item">
            <div class="tl-dot">1</div>
            <div class="tl-title">Supervisor Agent</div>
            <div class="tl-desc">Decides which agent to call</div>
        </div>
        <div class="tl-item">
            <div class="tl-dot">2</div>
            <div class="tl-title">Weather Agent</div>
            <div class="tl-desc">Fetches real-time weather</div>
        </div>
        <div class="tl-item">
            <div class="tl-dot">3</div>
            <div class="tl-title">Research Agent</div>
            <div class="tl-desc">Searches the web via Tavily</div>
        </div>
        <div class="tl-item">
            <div class="tl-dot">4</div>
            <div class="tl-title">Synthesizer</div>
            <div class="tl-desc">Creates the final answer</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.divider()
    st.markdown('<div class="sb-heading">Tools Available</div>', unsafe_allow_html=True)
    st.markdown('<div class="tool-chip tool-chip-green"><span class="dot"></span>OpenWeatherMap</div>', unsafe_allow_html=True)
    st.markdown('<div class="tool-chip tool-chip-blue"><span class="dot"></span>Tavily Web Search</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown('<div class="sb-heading">Try Asking</div>', unsafe_allow_html=True)
    suggestions = [
        "Weather in Jaipur?",
        "Best places in Udaipur",
        "Top 5 news today",
        "Plan a trip to Goa",
        "3 day itinerary for Udaipur",
    ]
    for i, suggestion in enumerate(suggestions):
        if st.button(suggestion, key=f"suggest_{i}", use_container_width=True):
            st.session_state.pending_query = suggestion

# ---------------------------------------------------------------------------
# Chat state
# ---------------------------------------------------------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

TAG_HTML = {
    "weather": '<span class="tag tag-weather">Weather Tool</span>',
    "research": '<span class="tag tag-research">Tavily Search</span>',
    "itinerary": '<span class="tag tag-itinerary">Itinerary Planner</span>',
    "none": '<span class="tag tag-none">Direct LLM</span>',
}

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message["role"] == "assistant":
            tool_used = message.get("tool_used", "none")
            st.markdown(TAG_HTML.get(tool_used, TAG_HTML["none"]), unsafe_allow_html=True)

user_input = st.chat_input("Ask about any travel destination...")

if not user_input and st.session_state.get("pending_query"):
    user_input = st.session_state.pop("pending_query")

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

        st.markdown(TAG_HTML.get(tool_used, TAG_HTML["none"]), unsafe_allow_html=True)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "tool_used": tool_used
    })