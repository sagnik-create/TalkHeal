import streamlit as st
from geopy.geocoders import Nominatim
from .sidebar import LOCAL_RESOURCES, GLOBAL_RESOURCES


def render_emergency_page():
    """Displays the full-screen emergency resources page using manual location search."""

    # --- 1. Interactive Elements ---
    if st.button("← Back to Chat"):
        st.session_state.show_emergency_page = False
        if 'location_info' in st.session_state:
            del st.session_state['location_info']  # Clear location on exit
        st.rerun()

    # --- 2. Static Header ---
    st.markdown("""
    <div class="main-header">
        <h1>Help is Available</h1>
        <div class="stAlert stInfo">If you are in immediate danger, please call your local emergency number (e.g., 911) immediately.</div>
    </div>
    """, unsafe_allow_html=True)

    # --- 3. Manual Search Logic ---
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

    # --- 4. Build and Render HTML Output ---
    if 'location_info' in st.session_state and st.session_state.location_info:
        info = st.session_state.location_info
        lat = float(info['lat'])
        lon = float(info['lon'])
        display_name = info.get('display_name', 'your selected location')

        # Build the OpenStreetMap URL
        zoom_level = 0.05
        map_url = f"https://www.openstreetmap.org/export/embed.html?bbox={lon-zoom_level},{lat-zoom_level},{lon+zoom_level},{lat+zoom_level}&layer=mapnik&marker={lat},{lon}"

        # Start building the HTML string
        html_output = f'<div class="stAlert stSuccess">Showing results for: {display_name}</div>'
        html_output += f'<iframe src="{map_url}" width="100%" height="400" style="border:1px solid #ccc; border-radius: 12px; margin-top: 16px;"></iframe>'

        # Add Local Resources to HTML
        if 'address' in info and 'country_code' in info['address']:
            country_code = info['address']['country_code'].upper()
            if country_code in LOCAL_RESOURCES:
                resource = LOCAL_RESOURCES[country_code]
                html_output += f"<h4><strong>{resource['name']}</strong></h4>"
                html_output += f"<p>📞 <strong>Contact:</strong> {resource['contact']}</p>"
                html_output += f'<p>🌐 <strong>Website:</strong> <a href="{resource["url"]}" target="_blank">{resource["url"]}</a></p>'
            else:
                html_output += '<div class="stAlert stInfo" style="margin-top: 16px;">We don\'t have specific resources for your country yet, but global help is always available below.</div>'
        else:
            html_output += '<div class="stAlert stWarning" style="margin-top: 16px;">Could not determine a country code from the location. Showing global resources.</div>'

        # Add Global Resources to HTML using <details> tag to mimic an expander
        html_output += """
        <details open style="margin-top: 24px; padding: 16px; border: 1px solid #ccc; border-radius: 12px;">
            <summary style="font-weight: 600; cursor: pointer;">View Global Crisis Hotlines</summary>
            <div style="margin-top: 12px;">
        """
        for resource in GLOBAL_RESOURCES:
            html_output += f'<p><strong>{resource["name"]}:</strong> {resource["desc"]} <a href="{resource["url"]}" target="_blank">Visit Website</a></p>'

        html_output += "</div></details>"

        # Render the final HTML block
        st.markdown(html_output, unsafe_allow_html=True)
