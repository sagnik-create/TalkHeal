import streamlit as st
from geopy.geocoders import Nominatim
import urllib.parse
from .sidebar import GLOBAL_RESOURCES  


def render_emergency_page():
    """Displays emergency help page with dynamic search for local resources."""

    # --- 1. Back Button ---
    if st.button("← Back to Chat"):
        st.session_state.show_emergency_page = False
        if 'location_info' in st.session_state:
            del st.session_state['location_info']
        st.rerun()

    # --- 2. Main Header ---
    st.markdown("""
    <div class="main-header">
        <h1>Help is Available</h1>
        <div class="stAlert stInfo">If you are in immediate danger, please call your local emergency number (e.g., 911) immediately.</div>
    </div>
    """, unsafe_allow_html=True)

    # --- 3. Manual Geolocation Search ---
    st.subheader("Find Local Resources Near You")
    geolocator = Nominatim(user_agent="talkheal_app")
    location_query = st.text_input(
        "Enter your City, State, or Country", placeholder="e.g., London, UK")

    if st.button("🔍 Search for Help"):
        if location_query:
            with st.spinner(f"Searching for '{location_query}'..."):
                try:
                    location = geolocator.geocode(
                        location_query, addressdetails=True, language='en')
                    if location:
                        st.session_state.location_info = location.raw
                    else:
                        st.error(
                            f"Could not find a location for '{location_query}'. Please try a different search.")
                        if 'location_info' in st.session_state:
                            del st.session_state['location_info']
                except Exception as e:
                    st.error(f"An error occurred during search: {e}")
                    if 'location_info' in st.session_state:
                        del st.session_state['location_info']
        else:
            st.warning("Please enter a location to search.")

    # --- 4. Display Map and DYNAMIC Local Resource Link ---
    if 'location_info' in st.session_state and st.session_state.location_info:
        info = st.session_state.location_info
        lat = float(info['lat'])
        lon = float(info['lon'])
        display_name = info.get('display_name', 'your selected location')

        st.success(f"Showing results for: {display_name}")

        # Display Embedded OpenStreetMap
        zoom_level = 0.05
        map_url = f"https://www.openstreetmap.org/export/embed.html?bbox={lon-zoom_level},{lat-zoom_level},{lon+zoom_level},{lat+zoom_level}&layer=mapnik&marker={lat},{lon}"
        st.components.v1.iframe(map_url, height=400)

        # --- DYNAMICALLY GENERATE SEARCH LINK ---
        st.markdown("#### **Find Local Support**")
        # Create a precise search query
        search_term = f"mental health crisis support near {display_name}"
        # URL-encode the search term to handle spaces and special characters
        encoded_search = urllib.parse.quote_plus(search_term)
        search_url = f"https://www.google.com/search?q={encoded_search}"

        st.markdown(f"""
        <a href="{search_url}" target="_blank" class="emergency_button" style="display: block; text-align: center;">
            🔍 Search for local crisis centers
        </a>
        """, unsafe_allow_html=True)
        st.info("Click the button above to search for support centers in your area. Results will open in a new tab.")

    # --- 5. Global Resources (Always Visible as a fallback) ---
    with st.expander("View Global Crisis Hotlines", expanded=True):
        for resource in GLOBAL_RESOURCES:
            st.markdown(
                f"**{resource['name']}**: {resource['desc']} [Visit Website]({resource['url']})")
