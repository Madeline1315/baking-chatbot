import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

if "history" not in st.session_state:
    st.session_state.history = []

st.title("Baking Assistant Chatbot")

for message in st.session_state.history:
    role = "You" if message.role == "user" else "Gemini"
    st.chat_message(message.role).write(message.parts[0].text)

user_input = st.chat_input("Ask a question...")

if user_input:
    st.session_state.history.append(
        types.Content(role="user", parts=[types.Part(text=user_input)])
    )

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=st.session_state.history,
        config=types.GenerateContentConfig(
            system_instruction="""You are a baking asssitant for any type of baker
            If the question isnt about baking, answer politely and then shift the conversation back to baking. 
            Your tone should be encouraging but professional. 
            Never be rude when answering a question."""
        )
    )

    st.session_state.history.append(
        types.Content(role="model", parts=[types.Part(text=response.text)])
    )

    st.rerun()