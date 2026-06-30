import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

PERSONAS = {
    "Assistant": "You are a helpful, concise assistant.",
    "Socratic Tutor": "You are a Socratic tutor. Never give direct answers. Ask one guiding question at a time.",
    "Code Reviewer": "You are a brutally honest senior engineer doing a code review. Be direct, always explain why.",
}

st.set_page_config(page_title="AI Assistant", page_icon="✦")
st.title("✦ AI Assistant")

with st.sidebar:
    persona = st.selectbox("Persona", list(PERSONAS.keys()))
    if st.session_state.get("persona") != persona:
        st.session_state.persona = persona
        st.session_state.messages = []
    if st.button("Clear chat"):
        st.session_state.messages = []

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Say something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    full_messages = [{"role": "system", "content": PERSONAS[st.session_state.persona]}] + st.session_state.messages[-10:]

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=full_messages,
            stream=True
        )
        reply = st.write_stream(chunk.choices[0].delta.content or "" for chunk in stream)

    st.session_state.messages.append({"role": "assistant", "content": reply})