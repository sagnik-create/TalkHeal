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