import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Set page configuration with a custom theme
st.set_page_config(
    page_title="Chat with Gemini",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.example.com/help',
        'Report a bug': 'https://www.example.com/bug',
        'About': "Chat with Gemini - A Generative AI Chatbot"
    }
)

# Load API key
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Translate role for Streamlit chat
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.user_messages = []

# Function to display chat history
def display_chat_history():
    for message in st.session_state.chat_history:
        try:
            role = translate_role_for_streamlit(message.role)
        except AttributeError:
            role = "unknown"  # Default role if unavailable
        with st.chat_message(role):
            st.markdown(message.text)

# Add custom CSS for black background and white content areas
st.markdown("""
    <style>
        body {
            background-color: #000000;
            color: #FFFFFF;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .stApp {
            background-color: #000000;
            padding: 25px;
        }
        .stMarkdown, .st-chat-input {
            background-color: #FFFFFF;
            color: #000000;
            border-radius: 15px;
            padding: 15px;
            margin-bottom: 12px;
            box-shadow: 0px 4px 10px rgba(255, 255, 255, 0.2);
        }
        .st-chat-message.assistant {
            background-color: #FFFFFF;
            color: #000000;
            border-left: 8px solid #48c9b0;
            padding-left: 20px;
            font-size: 16px;
            font-weight: 500;
            margin-top: 12px;
            margin-bottom: 12px;
            border-radius: 15px;
        }
        .st-chat-message.user {
            background-color: #FFFFFF;
            color: #000000;
            border-left: 8px solid #e74c3c;
            padding-left: 20px;
            font-size: 16px;
            font-weight: 500;
            margin-top: 12px;
            margin-bottom: 12px;
            border-radius: 15px;
        }
        .st-chat-message.unknown {
            background-color: #FFFFFF;
            color: #000000;
            border-left: 8px solid #f39c12;
            padding-left: 20px;
            font-size: 16px;
            font-weight: 500;
            margin-top: 12px;
            margin-bottom: 12px;
            border-radius: 15px;
        }
        h1 {
            color: #FFFFFF;
            font-size: 42px;
            text-align: center;
            margin-bottom: 40px;
            font-weight: bold;
        }
        .css-18e3th9 {
            background-color: #000000;
            border: none;
        }
    </style>
""", unsafe_allow_html=True)

# Display chat history
st.title("✨ Gemini Chat Bot ✨")
display_chat_history()

# Chat input
user_prompt = st.chat_input("Ask Gemini-pro")

# Process user input and generate response
if user_prompt:
    st.session_state.user_messages.append(user_prompt)
    st.chat_message("user").markdown(user_prompt)

    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    gemini_response = st.session_state.chat_session.send_message(user_prompt)
    st.session_state.chat_history.append(gemini_response)

    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
