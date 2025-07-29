import streamlit as st
import google.generativeai as genai
from pathlib import Path

logo_path = str(Path(__file__).resolve().parent.parent / "TalkHealLogo.png")

PAGE_CONFIG = {
    "page_title": "TalkHeal - Mental Health Support",
    "page_icon": logo_path,
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "menu_items": None
}

#st.set_page_config(**PAGE_CONFIG)

# ---------- Custom Dropdown Style ----------
st.markdown("""
    <style>
        div[data-baseweb="select"] {
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Tone Options ----------
TONE_OPTIONS = {
    "Compassionate Listener": "You are a compassionate listener — soft, empathetic, patient — like a therapist who listens without judgment.",
    "Motivating Coach": "You are a motivating coach — energetic, encouraging, and action-focused — helping the user push through rough days.",
    "Wise Friend": "You are a wise friend — thoughtful, poetic, and reflective — giving soulful responses and timeless advice.",
    "Neutral Therapist": "You are a neutral therapist — balanced, logical, and non-intrusive — asking guiding questions using CBT techniques.",
    "Mindfulness Guide": "You are a mindfulness guide — calm, slow, and grounding — focused on breathing, presence, and awareness."
}

# ---------- Sidebar Tone Selector ----------
with st.sidebar:
    st.header("🧠 Choose Your AI Tone")
    default_tone = list(TONE_OPTIONS.keys())[0]
    selected_tone = st.selectbox(
        "Select a personality tone:",
        options=list(TONE_OPTIONS.keys()),
        index=0,
        key="tone_selector"
    )
    st.session_state["selected_tone"] = selected_tone or default_tone

# ---------- Display Current Tone in Chat Section ----------
st.subheader(f"🗣️ Current Chatbot Tone: **{st.session_state['selected_tone']}**")

# ---------- Gemini Configuration ----------
def configure_gemini():
    try:
        api_key = st.secrets["AIzaSyBElC7yFAKv3cBKKGXpDIw65JbWpXaTiJo"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        return model
    except KeyError:
        st.error("Gemini API key not found in Streamlit secrets.")
    except Exception as e:
        st.error(f"Failed to configure Gemini API: {e}")
    return None