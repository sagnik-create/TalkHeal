# header.py:
import streamlit as st

def render_header():
    """Renders the main header of the application."""
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
        # <h1>PeacePulse</h1>
        # <p>Your Mental Health Companion 💙</p>
    with st.expander("📍 Find Help Nearby"):
        location_input = st.text_input("Enter your city", key="location_search")
        if st.button("🔍 Search Centers", key="search_nearby"):
            if location_input:
                # Using a more robust Google Maps search URL
                search_url = f"https://www.google.com/maps/search/mental+health+centers+near+{location_input.replace(' ', '+')}"
                st.markdown(f"[🗺️ View Mental Health Centers Near {location_input}]({search_url})")
            else:
                st.warning("Please enter a city name")
    st.markdown('</div>', unsafe_allow_html=True)