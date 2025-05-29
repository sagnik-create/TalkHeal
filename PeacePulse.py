import streamlit as st
import google.generativeai as genai

# Import components and core functionalities
from core.config import configure_gemini, PAGE_CONFIG
from core.utils import get_current_time, create_new_conversation
from css.styles import apply_custom_css
from components.header import render_header
from components.sidebar import render_sidebar
from components.chat_interface import render_chat_interface, handle_chat_input

# --- Set page configuration ---
st.set_page_config(**PAGE_CONFIG)

# Apply custom CSS
apply_custom_css()

# Initialize session state variables
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
# Initialize sidebar state
if "sidebar_collapsed" not in st.session_state:
    st.session_state.sidebar_collapsed = False


# Configure Gemini API
model = configure_gemini()


# NO LONGER NEEDED HERE: Sidebar Toggle Button (moved to sidebar.py)
# toggle_button = st.button("☰", key="sidebar_toggle")
# if toggle_button:
#     st.session_state.sidebar_collapsed = not st.session_state.sidebar_collapsed

# Apply sidebar state
st.markdown(f"""
<style>
    [data-testid="stSidebar"] {{
        visibility: {'hidden' if st.session_state.sidebar_collapsed else 'visible'};
        transform: translateX({'0' if not st.session_state.sidebar_collapsed else '-100%'});
        transition: transform 300ms ease-in-out;
    }}
    /* The sidebar-toggle class CSS will now be primarily managed in styles.py for internal sidebar positioning */
</style>
""", unsafe_allow_html=True)


# Left Sidebar: Conversation History and Resources
render_sidebar()

# Main Chat Area Header
render_header()

# Ensure we have at least one conversation
if not st.session_state.conversations:
    create_new_conversation()

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