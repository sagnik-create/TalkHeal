import streamlit as st

def render_header():
    # Use a Streamlit-native container
    with st.container():
        # Give a CSS targetable HTML marker
        st.markdown('<div class="main-header">', unsafe_allow_html=True)
        
        st.markdown("## PeacePulse")
        st.markdown("Your Mental Health Companion 💙")

        with st.expander("📍 Find Help Nearby"):
            location_input = st.text_input("Enter your city", key="header_location_search")
            if st.button("🔍 Search Centers", key="header_search_nearby"):
                if location_input:
                    search_url = f"https://www.google.com/maps/search/mental+health+centers+near+{location_input.replace(' ', '+')}"
                    st.markdown(f"[🗺️ View Mental Health Centers Near {location_input}]({search_url})")
                else:
                    st.warning("Please enter a city name")
        
        st.markdown("</div>", unsafe_allow_html=True)
