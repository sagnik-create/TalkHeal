import streamlit as st

# ✅ MUST be the first Streamlit command
st.set_page_config(
    page_title="TalkHeal",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state=st.session_state.get("sidebar_state", "expanded")
)

import google.generativeai as genai
from core.db import init_db, create_user, get_user_by_username, create_chat, add_message, get_messages

# --- ENSURE TABLES EXIST BEFORE ANY DB USAGE ---
init_db()

from core.utils import save_conversations, load_conversations
from core.config import configure_gemini, PAGE_CONFIG
from core.utils import get_current_time,get_ai_response
from css.styles import apply_custom_css
from components.header import render_header
from components.sidebar import render_sidebar
from components.chat_interface import render_chat_interface
from components.emergency_page import render_emergency_page
from core.db import init_db, get_messages, add_message, create_chat
from core.db import get_user_by_username, create_user  # <-- Add this line, adjust module if needed
# --- ENSURE TABLES EXIST BEFORE ANY DB USAGE ---
init_db()

# --- 1. INITIALIZE SESSION STATE ---
if "show_emergency_page" not in st.session_state:
    st.session_state.show_emergency_page = False
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"
if "mental_disorders" not in st.session_state:
    st.session_state.mental_disorders = [
        "Depression & Mood Disorders", "Anxiety & Panic Disorders", "Bipolar Disorder",
        "PTSD & Trauma", "OCD & Related Disorders", "Eating Disorders",
        "Substance Use Disorders", "ADHD & Neurodevelopmental", "Personality Disorders",
        "Sleep Disorders"
    ]
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = None

# --- 2. SET PAGE CONFIG ---


# --- 3. APPLY STYLES & CONFIGURATIONS ---
apply_custom_css()
model = configure_gemini()

# --- 4. TONE SELECTION DROPDOWN IN SIDEBAR ---
TONE_OPTIONS = {
    "Compassionate Listener": "You are a compassionate listener — soft, empathetic, patient — like a therapist who listens without judgment.",
    "Motivating Coach": "You are a motivating coach — energetic, encouraging, and action-focused — helping the user push through rough days.",
    "Wise Friend": "You are a wise friend — thoughtful, poetic, and reflective — giving soulful responses and timeless advice.",
    "Neutral Therapist": "You are a neutral therapist — balanced, logical, and non-intrusive — asking guiding questions using CBT techniques.",
    "Mindfulness Guide": "You are a mindfulness guide — calm, slow, and grounding — focused on breathing, presence, and awareness."
}

with st.sidebar:
    st.header("🧠 Choose Your AI Tone")
    selected_tone = st.selectbox(
        "Select a personality tone:",
        options=list(TONE_OPTIONS.keys()),
        index=0
    )
    st.session_state.selected_tone = selected_tone

# --- 5. DEFINE FUNCTION TO GET TONE PROMPT ---
def get_tone_prompt():
    return TONE_OPTIONS.get(st.session_state.get("selected_tone", "Compassionate Listener"), TONE_OPTIONS["Compassionate Listener"])

# --- 6. RENDER SIDEBAR ---
def render_sidebar():
    from core.db import get_chats_for_user, create_chat
    if "user_id" in st.session_state and st.session_state.user_id:
        chats = get_chats_for_user(st.session_state.user_id)
        for chat in chats:
            if st.button(chat["title"], key=f"chat_{chat['id']}"):
                st.session_state.active_chat_id = chat["id"]
                st.rerun()
        if st.button("➕ New Chat"):
            chat_id = create_chat(st.session_state.user_id, "Untitled Chat")
            st.session_state.active_chat_id = chat_id
            st.rerun()

# --- 7. PAGE ROUTING ---
main_area = st.container()

# --- 8. RENDER PAGE ---
if st.session_state.get("show_emergency_page"):
    with main_area:
        render_emergency_page()
else:
    with main_area:
        render_header()
        render_chat_interface(model)

        # User login/register
        from core.db import create_user, get_user_by_username

        if "user_id" not in st.session_state or st.session_state.user_id is None:
            st.title("Login / Register")
            username = st.text_input("Username")
            email = st.text_input("Email")
            if st.button("Register/Login"):
                user = get_user_by_username(username)
                # Add this block to check for existing email
                from core.db import get_user_by_email
                existing_email_user = get_user_by_email(email)
                if existing_email_user and (not user or existing_email_user["id"] != (user["id"] if user else None)):
                    st.error("This email is already registered. Please use another email or log in with the existing username.")
                else:
                    if not user:
                        create_user(username, email)
                        user = get_user_by_username(username)
                    st.session_state.user_id = user["id"]
                    st.success(f"Logged in as {username}")
                    st.rerun()
            st.stop()

        # Start new chat
        if st.button("➕ New Chat"):
            chat_id = create_chat(st.session_state.user_id, "Untitled Chat")
            st.session_state.active_chat_id = chat_id
            st.experimental_rerun()

        # Send message
        user_input = st.text_input("Message", key="message_input")
        if st.button("Send") and user_input.strip() and st.session_state.get("active_chat_id"):
            add_message(st.session_state.active_chat_id, "user", user_input.strip())
            st.experimental_rerun()

        # Display chat history
        if st.session_state.get("active_chat_id"):
            messages = get_messages(st.session_state.active_chat_id)
            for msg in messages:
                st.write(f"{msg['sender']}: {msg['message']}")

st.markdown("""
<script>
    function scrollToBottom() {
        var chatContainer = document.querySelector('.chat-container');
        if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    }
    setTimeout(scrollToBottom, 100);
</script>
""", unsafe_allow_html=True)