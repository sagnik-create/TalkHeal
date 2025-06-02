import streamlit as st
import google.generativeai as genai

# Page configuration settings
PAGE_CONFIG = {
    "page_title": "TalkHeal - Mental Health Support",
    "page_icon": "💙",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "menu_items": None
}

# Configure Gemini API
def configure_gemini():
    """Configures the Gemini API with the provided API key."""
    try:
        # Replace with your actual API key or use environment variable
        genai.configure(api_key="AIzaSyBeulOMD_D6_AUVdf1MKG6wnjxQ_gaSYsw") 
        model = genai.GenerativeModel('gemini-2.0-flash')
        return model
    except Exception as e:
        st.error("Failed to configure Gemini API. Please check your API key.")
        return None