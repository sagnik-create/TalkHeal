import streamlit as st


def render_header():
    with st.container():
        st.markdown("""
        <div class="main-header">
            <h1>TalkHeal</h1>
            <p>Your Mental Health Companion 💙</p>
        </div>
        """, unsafe_allow_html=True)
        ## Commented out this part of the header because the 'emergency button' functionality is quite similar, hence causing redundancy. ##

        # with st.expander("📍 Find Help Nearby"):
        #     location_input = st.text_input("Enter your city", key="header_location_search")
        #     if st.button("🔍 Search Centers", key="header_search_nearby"):
        #         if location_input:
        #             search_url = f"https://www.google.com/maps/search/mental+health+centers+{location_input.replace(' ', '+')}"
        #             st.markdown(f'<a href="{search_url}" target="_blank">🗺️ View Mental Health Centers Near {location_input}</a>', unsafe_allow_html=True)
        #             st.success("Opening search results in a new tab...")
        #         else:
        #             st.warning("Please enter a city name")
