import streamlit as st

def render_header():
    with st.container():
        st.markdown("""
        <div class="main-header">
            <h1>PeacePulse</h1>
            <p>Your Mental Health Companion 💙</p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("📍 Find Help Nearby"):
            location_input = st.text_input("Enter your city", key="header_location_search")
            if st.button("🔍 Search Centers", key="header_search_nearby"):
                if location_input:
                    search_url = f"https://www.google.com/maps/search/mental+health+centers+near+{location_input.replace(' ', '+')}"
                    st.markdown(f"[🗺️ View Mental Health Centers Near {location_input}]({search_url})")
                else:
                    st.warning("Please enter a city name")