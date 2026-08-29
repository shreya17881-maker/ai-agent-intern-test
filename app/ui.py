
import sys
from pathlib import Path

# Add the project root to Python's import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from app.agent import AsterRowAgent


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="Aster & Row Support Agent",
    page_icon="🛍️",
    layout="centered"
)


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("🛍️ Aster & Row Support Agent")
st.caption("Reliable RAG-powered customer support")


# ---------------------------------------------------------
# CREATE AGENT ONCE
# ---------------------------------------------------------

if "agent" not in st.session_state:
    st.session_state.agent = AsterRowAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------------------------------------
# DISPLAY CHAT HISTORY
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------------

user_question = st.chat_input(
    "Ask about returns, shipping, products, or an order..."
)


if user_question:

    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    with st.chat_message("user"):
        st.markdown(user_question)

    # Get agent response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:
                response = st.session_state.agent.ask(
                    user_question
                )

            except Exception as e:
                response = (
                    "Sorry, I encountered an error while "
                    "processing your request."
                )

                st.error(str(e))

        st.markdown(response)

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("About")

    st.write(
        "This demo uses:"
    )

    st.markdown(
        """
        - 🧠 **Llama 3.2**
        - 🦙 **Ollama**
        - 🔎 **RAG**
        - 📚 **ChromaDB**
        - 🔐 **Privacy controls**
        - 📦 **Order lookup**
        - 💬 **Multi-turn conversation**
        """
    )

    st.divider()

    st.subheader("Example questions")

    st.write(
        "What is the standard return window?"
    )

    st.write(
        "Where is ORD-1007?"
    )

    st.write(
        "When will it arrive?"
    )

    st.write(
        "Do you ship internationally?"
    )

    st.divider()

    if st.button("Clear conversation"):

        st.session_state.messages = []
        st.session_state.agent = AsterRowAgent()

        st.rerun()

