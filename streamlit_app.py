import streamlit as st
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from parthis_core import ParthisAgent
from modules.local_memory import LocalMemoryEngine

# Streamlit Page Setup for Mobile/PWA Optimization
st.set_page_config(
    page_title="Parthis AI Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize Session States
if "agent" not in st.session_state:
    st.session_state.agent = ParthisAgent()

if "memory" not in st.session_state:
    st.session_state.memory = LocalMemoryEngine()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Title & Status Bar
st.title("🤖 Parthis AI Assistant")
st.caption("Resilient Mobile-Native Autonomous PWA Engine")

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Processing
if prompt := st.chat_input("Ask Parthis anything..."):
    # Render user prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Memory Retrieval (RAG Context)
    relevant_docs = st.session_state.memory.recall_context(query=prompt, top_k=2)
    context_str = "\n".join(relevant_docs) if relevant_docs else "No relevant past context."

    augmented_prompt = f"Context from Memory:\n{context_str}\n\nUser Question:\n{prompt}"

    # Agent Processing with Fallback Execution
    with st.chat_message("assistant"):
        with st.spinner("Processing with resilient fallback matrix..."):
            response = st.session_state.agent.process_request(augmented_prompt)
            st.markdown(response)

    # Store Memory and Conversation History
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.memory.add_memory(
        doc_id=f"doc_{len(st.session_state.messages)}",
        text_content=f"User: {prompt} | Assistant: {response}"
    )
