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

    # The "Find Help Nearby" section should be rendered here
    # and removed from sidebar.py to avoid key duplication.
    with st.expander("📍 Find Help Nearby"):
        location_input = st.text_input("Enter your city", key="header_location_search") # Changed key to be unique
        if st.button("🔍 Search Centers", key="header_search_nearby"): # Changed key to be unique
            if location_input:
                # Using a more robust Google Maps search URL
                search_url = f"https://www.google.com/maps/search/mental+health+centers+near+{location_input.replace(' ', '+')}"
                st.markdown(f"[🗺️ View Mental Health Centers Near {location_input}]({search_url})")
            else:
                st.warning("Please enter a city name")