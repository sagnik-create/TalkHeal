import streamlit as st
import json
import os
from streamlit_lottie import st_lottie

st.set_page_config(page_title="🧘 Yoga for Mental Health", layout="centered")

def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

lottie_yoga = load_lottiefile("assets/yoga_animation.json")

# --- Load Yoga Data ---
try:
    with open(os.path.join("data", "Yoga.json"), "r") as f:
        yoga_data = json.load(f)
except FileNotFoundError:
    yoga_data = {}

#--CSS--
st.markdown("""
<style>
/* Base background */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stVerticalBlock"],
section[data-testid="stVerticalBlock"] > div,
div[style*="background-color: transparent"],
div[style*="background: transparent"],
div:empty {
    background-color: #ffe6f2 !important;
    margin: 0 !important;
    padding: 0 !important;
    border: none !important;
    box-shadow: none !important;
    height: auto;
    visibility: visible;
}

/* Sidebar visually distinct */
[data-testid="stSidebar"] {
    background-color: #fdd0e8 !important;
    border-right: 2px solid #f5a7d0 !important;
}

/* Header strip */
header[data-testid="stHeader"] {
    background-color: #ffe6f2 !important;
}

/* Remove bars/separators */
hr, div[role="separator"], [data-testid="stHorizontalBlock"],
div[style*="rgba(245"], div[style*="#f5"], div[style*="rgb(245"] {
    display: none !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
    background: transparent !important;
    box-shadow: none !important;
    visibility: hidden !important;
}

/* Block padding */
.block-container {
    padding-top: 0rem !important;
    margin-top: 0rem !important;
}

/* Animation container */
.lottie-container {
    margin-top: -20px;
    margin-bottom: -10px;
    padding: 15px;
    border-radius: 12px;
    background-color: #fcd5ec;
    display: flex;
    justify-content: center;
}

/* Cursor fix for dropdown */
div[data-testid="stSelectbox"] * {
    cursor: pointer !important;
}

/* Watermark effect for placeholder */
div[data-testid="stSelectbox"] > div:first-child > div {
    color: gray !important;
    font-style: italic !important;
}

/* Disable typing in dropdown input */
.stSelectbox input {
    pointer-events: none !important;
    caret-color: transparent !important;
    user-select: none !important;
    background-color: #fff0f6 !important;
}
</style>
""", unsafe_allow_html=True)

# --- Animation ---
st.markdown('<div class="lottie-container">', unsafe_allow_html=True)
if lottie_yoga:
    st_lottie(lottie_yoga, height=220, key="yoga")
st.markdown('</div>', unsafe_allow_html=True)

# --- Title & Description ---
st.markdown("<h1 style='text-align: center; color: #b833a2; margin-top: -15px;'>🧘‍♀️ Yoga for Mental Wellness</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 17px;'>Choose your mood and explore a calming yoga asana to support your mind and body.</p>", unsafe_allow_html=True)

# --- Dropdown --
def format_mood(option):
    return "Select your mood" if option == "Select your mood" else option

mood_options = ["Select your mood"] + list(yoga_data.keys())
selected_mood = st.selectbox(
    "🌸 How are you feeling today?",
    options=mood_options,
    index=0,
    format_func=format_mood,
    key="mood_selector"
)

# --- Asana Section ---
if selected_mood != "Select your mood":
    asana = yoga_data.get(selected_mood)
    if asana:
        st.markdown("<div style='background-color: #fff0f6; padding: 1.2rem; border-radius: 16px; margin-top: 1rem;'>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size: 24px; font-weight: bold; color: #a94ca7;'>🧘 {asana.get('sanskrit_name')} ({asana.get('english_name')})</div>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 16px; font-style: italic; color: #555;'>💖 {asana.get('benefit')}</p>", unsafe_allow_html=True)

        with st.expander("📋 Steps to Perform"):
            steps = asana.get("steps", [])
            if steps:
                for i, step in enumerate(steps, 1):
                    fixed_step = step.replace("â€“", "–").replace("â€‹", "")
                    st.markdown(f"<div style='background-color: #ffe6f2; border-left: 4px solid #d85fa7; padding: 0.5rem; border-radius: 10px; margin-bottom: 0.4rem; font-size: 15px;'>{i}. {fixed_step}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div>No steps available for this asana.</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
