import streamlit as st
import google.generativeai as genai

from core.config import configure_gemini, PAGE_CONFIG
from core.utils import get_current_time, create_new_conversation
from css.styles import apply_custom_css
from components.header import render_header
from components.sidebar import render_sidebar
from components.chat_interface import render_chat_interface, handle_chat_input
from components.emergency_page import render_emergency_page

# --- 1. INITIALIZE SESSION STATE ---
# This should be the very first thing in your app
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "conversations" not in st.session_state:
    st.session_state.conversations = []
if "active_conversation" not in st.session_state:
    st.session_state.active_conversation = -1
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

# --- 2. SET PAGE CONFIG ---
# Must be the first Streamlit command
st.set_page_config(
    page_title=PAGE_CONFIG["page_title"],
    page_icon=PAGE_CONFIG["page_icon"],
    layout=PAGE_CONFIG["layout"],
    initial_sidebar_state=st.session_state.sidebar_state
)

# --- 3. APPLY STYLES & CONFIGURATIONS ---
apply_custom_css()
model = configure_gemini()

# --- 4. RENDER UI COMPONENTS ---
# The sidebar is rendered ONCE and is available on all "pages"
render_sidebar()

# --- 5. PAGE ROUTING ---
main_area = st.container()

if st.session_state.get("show_emergency_page"):
    with main_area:
        render_emergency_page()
else:
    # Render the standard chat interface
    with main_area:
        render_header()

        # Ensure a conversation exists before rendering the chat
        if not st.session_state.conversations:
            create_new_conversation()
            st.session_state.active_conversation = 0
            st.rerun()  # Rerun to reflect the new conversation immediately

        render_chat_interface()
        handle_chat_input(model)

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
