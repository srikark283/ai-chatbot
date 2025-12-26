import streamlit as st
from google import genai
from database import ChatDatabase
import os
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Gemini AI", page_icon="✨", layout="wide")

# --- PREMIUM DARK MODE CSS ---
st.markdown("""
    <style>
        /* Main background and text */
        .stApp { 
            background-color: #0e1117; 
            color: #ffffff;
        }
        
        /* SIDEBAR DARK THEME */
        section[data-testid="stSidebar"] {
            background-color: #17191e !important;
            border-right: 1px solid #2d2d2d;
            min-width: 300px !important;
        }
        
        /* Sidebar text visibility */
        section[data-testid="stSidebar"] * {
            color: #e0e0e0 !important;
        }

        /* Sidebar Buttons (History Items) */
        .stButton > button {
            border: none !important;
            background-color: transparent !important;
            text-align: left !important;
            width: 100% !important;
            padding: 10px 14px !important;
            border-radius: 10px !important;
            color: #b0b0b0 !important;
            transition: background-color 0.3s ease;
        }

        .stButton > button:hover {
            background-color: #2d2d2d !important;
            color: #ffffff !important;
        }

        /* Primary 'New Chat' Button */
        div[data-testid="stSidebar"] .stButton > button[kind="primary"] {
            background-color: #2d2d2d !important;
            border: 1px solid #3d3d3d !important;
            border-radius: 24px !important;
            font-weight: 600 !important;
            margin-bottom: 20px !important;
            color: #ffffff !important;
        }
        
        div[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
            background-color: #3d3d3d !important;
            border-color: #4d4d4d !important;
        }

        /* Main Chat Area Headers */
        .main-header {
            text-align: center;
            font-size: 2.2rem;
            font-weight: 600;
            margin-top: 10vh;
            margin-bottom: 3rem;
            color: #ffffff;
            font-family: 'Inter', sans-serif;
        }

        /* Message Bubbles - Modern Minimalist */
        .stChatMessage {
            max-width: 850px;
            margin: auto;
            border-bottom: 0px !important;
        }
        
        /* Darker background for chat input */
        .stChatInputContainer {
            background-color: transparent !important;
            border-top: none !important;
        }
        
        .stChatInput {
            background-color: #2d2d2d !important;
            border: 1px solid #3d3d3d !important;
            color: #ffffff !important;
        }

        /* Popover Styling */
        div[data-testid="stPopoverContent"] {
            background-color: #1e1e1e !important;
            border: 1px solid #3d3d3d !important;
            color: white !important;
        }
        
        /* Small caption styling */
        .sidebar-caption {
            font-size: 0.75rem;
            color: #6e6e6e;
            padding-left: 12px;
            margin-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

db = ChatDatabase()

# --- INITIALIZATION ---
if "session_id" not in st.session_state:
    st.session_id = str(uuid.uuid4())
    db.create_session(st.session_id, title="New Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "gemini_client" not in st.session_state:
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        st.session_state.gemini_client = genai.Client(api_key=api_key)
        st.session_state.model_name = 'gemini-2.0-flash'

def get_gemini_response(prompt: str, history: list) -> str:
    try:
        contents = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({"role": role, "parts": [{"text": msg["content"]}]})
        
        if not history or history[-1]["content"] != prompt:
            contents.append({"role": "user", "parts": [{"text": prompt}]})

        response = st.session_state.gemini_client.models.generate_content(
            model=st.session_state.model_name, contents=contents
        )
        return response.text
    except Exception as e:
        return f"Error: {e}"

# --- SIDEBAR UI ---
with st.sidebar:
    st.markdown("<h2 style='margin-bottom:0; color:white;'>✨ Gemini</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#888; font-size:0.8rem; margin-top:0;'>Pro Workspace</p>", unsafe_allow_html=True)
    
    if st.button("＋ New Chat", use_container_width=True, type="primary"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        db.create_session(st.session_state.session_id)
        st.rerun()

    st.markdown('<p class="sidebar-caption">History</p>', unsafe_allow_html=True)
    sessions = db.get_all_sessions()
    for session in sessions:
        title = session["title"] or "Untitled Chat"
        
        col_t, col_r, col_d = st.columns([0.7, 0.15, 0.15])
        
        with col_t:
            if st.button(f"💬 {title[:18]}", key=f"s_{session['session_id']}"):
                st.session_state.session_id = session["session_id"]
                st.session_state.messages = db.get_session_history(session["session_id"])
                st.rerun()
        
        with col_r:
            with st.popover("✏️"):
                new_t = st.text_input("Rename", value=title, key=f"re_{session['session_id']}")
                if st.button("Save", key=f"sv_{session['session_id']}"):
                    db.update_session_title(session['session_id'], new_t)
                    st.rerun()
        
        with col_d:
            if st.button("🗑️", key=f"dl_{session['session_id']}"):
                db.delete_session(session['session_id'])
                if st.session_state.session_id == session['session_id']:
                    st.session_state.session_id = str(uuid.uuid4())
                    st.session_state.messages = []
                    db.create_session(st.session_state.session_id)
                st.rerun()

# --- MAIN CHAT UI ---
if not st.session_state.messages:
    st.markdown('<div class="main-header">How can I help you today?</div>', unsafe_allow_html=True)
    st.session_state.messages = db.get_session_history(st.session_state.session_id)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Message Gemini..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    db.add_message(st.session_state.session_id, "user", prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        response = get_gemini_response(prompt, st.session_state.messages)
        st.markdown(response)
    db.add_message(st.session_state.session_id, "assistant", response)
    st.session_state.messages.append({"role": "assistant", "content": response})

    if len(st.session_state.messages) <= 2:
        summary = get_gemini_response(f"Summarize this into 2 words: {prompt}", [])
        db.update_session_title(st.session_state.session_id, summary.strip('"'))
        st.rerun()