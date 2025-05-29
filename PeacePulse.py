import streamlit as st
import google.generativeai as genai

# Import components and core functionalities
from core.config import configure_gemini, PAGE_CONFIG
from core.utils import get_current_time, create_new_conversation
from css.styles import apply_custom_css
from components.header import render_header
from components.sidebar import render_sidebar
from components.chat_interface import render_chat_interface, handle_chat_input

# Initialize session state variables if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "conversations" not in st.session_state:
    st.session_state.conversations = []
if "active_conversation" not in st.session_state:
    st.session_state.active_conversation = -1
if "mental_disorders" not in st.session_state:
    st.session_state.mental_disorders = [
        "Depression & Mood Disorders",
        "Anxiety & Panic Disorders",
        "Bipolar Disorder",
        "PTSD & Trauma",
        "OCD & Related Disorders",
        "Eating Disorders",
        "Substance Use Disorders",
        "ADHD & Neurodevelopmental",
        "Personality Disorders",
        "Sleep Disorders"
    ]
# Initialize sidebar state - default to 'expanded'
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"

# --- Set page configuration with dynamic sidebar state ---
st.set_page_config(
    page_title=PAGE_CONFIG["page_title"],
    page_icon=PAGE_CONFIG["page_icon"],
    layout=PAGE_CONFIG["layout"],
    initial_sidebar_state=st.session_state.sidebar_state # Use session state here
)

# Apply custom CSS
apply_custom_css()

# Configure Gemini API
model = configure_gemini()

# --- Persistent Sidebar Toggle Button (outside of st.sidebar) ---
# Use an empty placeholder or a fixed column to place the button
# This creates a small column on the left for the toggle button
col_toggle, col_main = st.columns([0.05, 0.95]) # Adjust column ratios as needed

with col_toggle:
    # Use st.markdown for a custom button to control the sidebar
    # We use a unique key and an invisible span to make it clickable and prevent Streamlit's default behavior
    if st.button("☰", key="persistent_sidebar_toggle", help="Toggle Sidebar"):
        if st.session_state.sidebar_state == "expanded":
            st.session_state.sidebar_state = "collapsed"
        else:
            st.session_state.sidebar_state = "expanded"
        st.rerun() # Rerun to apply the new sidebar state

# Left Sidebar: Conversation History and Resources
render_sidebar()

# Main Chat Area Header (will now adapt to sidebar state)
render_header()

# Ensure we have at least one conversation
if not st.session_state.conversations:
    create_new_conversation()
    st.session_state.active_conversation = 0 # Ensure a conversation is active

# Render Chat Interface
render_chat_interface()

# Handle Chat Input
handle_chat_input(model)

# Auto-scroll chat to bottom (JavaScript injection)
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