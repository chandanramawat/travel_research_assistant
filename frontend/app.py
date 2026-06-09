# frontend/app.py
import streamlit as st
import requests

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="centered"
)

st.title("✈️ AI Travel Research Assistant")
st.caption("Ask me anything about travel destinations!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message["role"] == "assistant" and message.get("tool_used", "none") != "none":
            with st.expander("🔧 Tool Used"):
                st.success(f"Tool : {message['tool_used']}")
                st.info(f"Args : {message['tool_args']}")

# Chat input
user_input = st.chat_input("Ask about any travel destination...")

if user_input:

    # Show user message
    with st.chat_message("user"):
        st.write(user_input)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Call FastAPI
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                api_response = requests.post(
                    "http://localhost:8000/ask",
                    json={"message": user_input},
                    timeout=30
                )

                print(f"Status : {api_response.status_code}")
                print(f"Raw    : {api_response.text}")

                data      = api_response.json()
                answer    = data.get("response", "No response")
                tool_used = data.get("tool_used", "none")
                tool_args = data.get("tool_args", {})

                st.write(answer)

                with st.expander("🔧 Tool Used"):
                    if tool_used == "get_weather":
                        st.success("🌤️ Weather Tool used")
                        st.info(f"City : {tool_args.get('city', '')}")
                    elif tool_used == "tavily_search_results_json":
                        st.success("🔍 Tavily Search used")
                        st.info(f"Query : {tool_args.get('query', '')}")
                    else:
                        st.warning("⚡ No tool — direct LLM answer")

            except Exception as e:
                st.error(f"Error: {e}")
                print(f"Exception: {e}")
                answer    = "Something went wrong!"
                tool_used = "none"
                tool_args = {}

    # Save assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "tool_used": tool_used,
        "tool_args": tool_args
    })
    