import streamlit as st
from streamlit_modal import Modal # Import Modal from streamlit_modal
import time

def render_header():
    with st.container():
        st.markdown("""
        <div class="main-header">
            <h1>Hello, I'm TalkHeal, Your Best Friend!</h1>
            <p>I'm here to listen, support, and help guide you toward the resources you need. How are you feeling today? 😊</p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("📍 Find Help Nearby"):
            location_input = st.text_input("Enter your city", key="header_location_search")

            # Initialize the modal
            # The 'key' here is for the modal itself, distinct from button/input keys
            modal = Modal(key="maps_modal", title="Mental Health Centers Nearby")

            if st.button("🔍 Search Centers", key="header_search_nearby"):
                if location_input:
                    # Construct a more appropriate Google Maps URL for embedding
                    # Using Google Maps Embed API or a simple search query that Google Maps can interpret
                    # The 'q' parameter is good for searching categories/places.
                    # 'output=embed' might work for direct embedding, but often iframes are restricted.
                    # A more reliable direct search URL for opening in a modal might be:
                    search_url = f"https://www.google.com/maps/search/mental+health+centers+near+{location_input.replace(' ', '+')}"
                    
                    # It's important to set the modal to open
                    modal.open()
                    
                    # Store the URL in session state so it persists across reruns
                    st.session_state['current_search_url'] = search_url
                    st.session_state['current_search_location'] = location_input

                else:
                    st.warning("Please enter a city name")

            # This block only executes when the modal is open
            if modal.is_open():
                with modal.container():
                    st.write(f"Displaying results for: **{st.session_state.get('current_search_location', 'your query')}**")
                    
                    # Display the content inside the modal using an iframe
                    # Note: Many websites (like google.com) restrict embedding in iframes for security reasons (X-Frame-Options header).
                    # This might not always work directly for live Google Maps.
                    # A more reliable approach might be to show a clickable link within the modal to open in a new tab.
                    st.markdown(
                        f'<iframe src="{st.session_state.get("current_search_url", "")}" width="100%" height="400px" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>',
                        unsafe_allow_html=True
                    )
                    
                    st.write("---")
                    st.markdown(f"**If the map doesn't load above, click here:** [🗺️ Open in New Tab]({st.session_state.get('current_search_url', '#')})")

                    # Add a close button if desired, though the modal usually has one by default
                    if st.button("Close Map", key="close_map_modal"):
                        modal.close()