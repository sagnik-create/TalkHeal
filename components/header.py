import streamlit as st
from streamlit_modal import Modal # Import Modal from streamlit_modal
import time

def render_header():
    with st.container():
        st.markdown("""
        <div class="main-header">
            <h1>I'm TalkHeal</h1>
            <p>I'm here to listen, support, and help guide you toward the resources you need. How are you feeling today? 😊</p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("📍 Find Help Nearby"):
            location_input = st.text_input("Enter your city", key="header_location_search")
            
            # When this button is clicked, we'll generate and open the link
            if st.button("🔍 Search Centers", key="header_search_nearby"):
                if location_input:
                    # Constructing a standard Google Maps search URL
                    # This URL is suitable for opening directly in a browser tab
                    search_url = f"https://www.google.com/maps/search/mental+health+centers+{location_input.replace(' ', '+')}"
                    
                    # Using st.markdown to create an HTML link that opens in a new tab
                    # This is the effective way to "open a new tab" from Streamlit Cloud
                    st.markdown(f'<a href="{search_url}" target="_blank">🗺️ View Mental Health Centers Near {location_input}</a>', unsafe_allow_html=True)
                    
                    # Optionally, you might want to provide immediate feedback to the user
                    st.success("Opening search results in a new tab...")
                else:
                    st.warning("Please enter a city name")