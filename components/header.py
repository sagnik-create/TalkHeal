import streamlit as st
from components.sidebar import render_mood_tracker # Import the new function

def render_header():
    """Renders the main header area, now containing the Mood Tracker."""
    render_mood_tracker() # Call the mood tracker function here