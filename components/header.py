# header.py:
import streamlit as st

def render_header():
    """Renders the main header of the application."""
    st.markdown("""
    <div class="main-header">
        <h1>PeacePulse</h1>
        <p>Your Mental Health Companion 💙</p>
    </div>
    """, unsafe_allow_html=True)