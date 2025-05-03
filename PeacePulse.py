import streamlit as st
from PIL import Image
import base64
import time

# --- Set page configuration ---
st.set_page_config(page_title="PeacePulse", layout="wide")

# --- Set background from image file ---
def set_bg_from_local(img_path):
    with open(img_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# 🖼️ Replace this with the correct path to your image
set_bg_from_local("PeacePulseLogo.png")

# --- Title / Heading ---
st.markdown("<h1 style='text-align: center; color: black;'>Your Personal AI-based Mental Health Assistant :)</h1>", unsafe_allow_html=True)

# --- Issue Section ---
st.subheader("💬 What's your Issue ^-*?")
issue_input = st.text_input("Describe your issue here")

if st.button("🔍 Search for Help Resources"):
    if issue_input:
        search_term = issue_input.lower().replace(" ", "-")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"[🧭 HelpGuide](https://www.helpguide.org/?s={search_term})", unsafe_allow_html=True)
        with col2:
            st.markdown(f"[🧪 NIMH](https://www.nimh.nih.gov/search-nimh?q={search_term})", unsafe_allow_html=True)
        with col3:
            st.markdown(f"[🧠 Mind UK](https://www.mind.org.uk/search-results/?q={search_term})", unsafe_allow_html=True)

# --- Location-based Care Centres ---
st.subheader("📍 Where Do You Stay Friend?")
location_input = st.text_input("Enter your city or location")

if st.button("📌 Search Care Centres Near You"):
    if location_input:
        location_url = f"https://www.google.com/maps/search/Mental+Hospitals+and+trauma+care+centres+in+{location_input.replace(' ', '-')}/"
        st.markdown(f"[🗺️ View Nearby Centers on Google Maps]({location_url})", unsafe_allow_html=True)

# --- Professionals Help ---
st.subheader("👩‍⚕️ Some Specialists Who Can Help You :)")
if st.button("🔍 Find Mental Health Professionals"):
    st.markdown("[🌐 GoodTherapy Therapist Search](https://www.goodtherapy.org/therapists/search)", unsafe_allow_html=True)

# --- Developer Info & Date ---
st.markdown("---")
st.markdown("### 👨‍💻 Developed By:")
st.markdown("**The Quantum Tech Mystifiers**  \n_“It's absolutely okay not to be okay :)”_", unsafe_allow_html=True)

st.markdown(f"📅 **Date:** {time.strftime('%d/%m/%y')}")

# --- Footer spacing ---
st.markdown("<br><br>", unsafe_allow_html=True)