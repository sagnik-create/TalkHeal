# header.py:
import streamlit as st

def render_header():
    """Renders the main header of the application."""
    
    # Use st.container to create a content block
    # This container will receive the 'main-header' CSS class
    with st.container(border=False): # border=False removes Streamlit's default container border
        st.markdown("""
        <div class="main-header-content">
            <h1>PeacePulse</h1>
            <p>Your Mental Health Companion 💙</p>
        </div>
        """, unsafe_allow_html=True)

        # Now, place the expander directly inside this Streamlit container.
        # It will inherit the styling or positioning from the parent container.
        with st.expander("📍 Find Help Nearby"):
            # Ensure unique keys, as discussed before.
            location_input = st.text_input("Enter your city", key="header_location_search_2")
            if st.button("🔍 Search Centers", key="header_search_nearby_2"):
                if location_input:
                    # Using a more robust Google Maps search URL
                    search_url = f"https://www.google.com/maps/search/mental+health+centers+near+{location_input.replace(' ', '+')}"
                    st.markdown(f"[🗺️ View Mental Health Centers Near {location_input}]({search_url})")
                else:
                    st.warning("Please enter a city name")

    # To apply the 'main-header' CSS to this entire block, you'll need to modify your CSS.
    # We'll use the data-testid property that Streamlit assigns to containers.
    # Find the data-testid for the container:
    # Open browser dev tools (F12), inspect the main-header area, and find the div
    # that Streamlit generates for st.container. It will have a data-testid like
    # "stVerticalBlock" or similar, followed by a hash.
    # Let's assume for this example it's "stVerticalBlock".
    st.markdown(
        """
        <style>
        /* Apply main-header styles to the Streamlit container that holds the content */
        [data-testid="stVerticalBlock"] > div:first-child > div:first-child { /* This targets the very first container rendered. Adjust selector if needed. */
            text-align: center; 
            padding: 32px 24px;
            background: var(--surface); /* Use your CSS variables */
            color: white;
            border-radius: var(--radius-lg);
            margin-bottom: 24px;
            box-shadow: 0 8px 32px var(--shadow-lg);
            border: 1px solid var(--border-light);
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(10px);
        }

        /* Ensure the gradient line at the top */
        [data-testid="stVerticalBlock"] > div:first-child > div:first-child::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        }

        /* Styles for the h1 and p inside the main header */
        .main-header-content h1 {
            margin: 0 0 8px 0;
            font-size: 2.5em;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .main-header-content p {
            margin: 0;
            font-size: 1.2em;
            color: rgba(255, 255, 255, 0.9);
            font-weight: 500;
        }

        /* Adjust expander styling if needed to fit within this new header box */
        /* For example, if you want the expander itself to have a different background */
        [data-testid="stVerticalBlock"] > div:first-child > div:first-child [data-testid="stExpander"] > div:first-child {
            background: rgba(255, 255, 255, 0.1); /* Slightly different background for expander within header */
            border-radius: var(--radius);
            margin-top: 15px; /* Space between header text and expander */
            padding: 10px; /* Adjust padding as needed */
            border: 1px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(5px);
        }
        </style>
        """, unsafe_allow_html=True
    )