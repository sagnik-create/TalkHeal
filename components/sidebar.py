import streamlit as st
import webbrowser
from datetime import datetime
from core.utils import create_new_conversation

# Emergency contacts and resources
emergency_resources = { "Crisis Hotlines": [ "National Suicide Prevention Lifeline: 988", "Crisis Text Line: Text HOME to 741741", "SAMHSA National Helpline: 1-800-662-4357"],
"International": [ "India: 9152987821 (AASRA)","UK: 116 123 (Samaritans)","Australia: 13 11 14 (Lifeline)"]

}

def render_sidebar():
    """Renders the left and right sidebars."""
    with st.sidebar:
        # The content that belongs together under 'Conversations'
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True) # Changed class name for clarity
        st.markdown("### 💬 Conversations")

        # New conversation button
        if st.button("➕ New Chat", key="new_chat", use_container_width=True):
            create_new_conversation()
            st.rerun()

        st.markdown("---")

        # Display conversation history
# In sidebar.py, update the conversation history section:

        # Display conversation history
        if st.session_state.conversations:
            for i, convo in enumerate(st.session_state.conversations):
                button_style = "🟢" if i == st.session_state.active_conversation else "📝"
                
                # Use kind="primary" for active conversation to apply special styling
                if st.button(
                    f"{button_style} {convo['title'][:22]}...",
                    key=f"convo_{i}",
                    help=f"Started: {convo['date']}",
                    use_container_width=True,
                    type="primary" if i == st.session_state.active_conversation else "secondary"
                ):
                    st.session_state.active_conversation = i
                    st.rerun()
        else:
            st.info("No conversations yet. Start a new chat!")
        st.markdown('</div>', unsafe_allow_html=True) # Close the conversations section

        # Emergency Help Button and other resources will be in separate sections
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True) # New section for emergency button
        st.markdown("""
        <div class="emergency-button" onclick="window.open('https://www.mentalhealth.gov/get-help/immediate-help', '_blank')">
            🚨 Emergency Help
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True) # Close emergency button section

        # The rest of your expanders can stay as they are, or also be wrapped in sidebar-section if desired
        # Quick Assessment
        with st.expander("🧠 Mental Health Check"):
            st.markdown("**How are you feeling today?**")
            mood = st.select_slider(
                "Mood Scale",
                options=["😔 Very Low", "😐 Low", "😊 Okay", "😄 Good", "🌟 Great"],
                value="😊 Okay",
                label_visibility="collapsed"
            )

            if st.button("Get Personalized Tips", key="mood_tips"):
                tips = {
                    "😔 Very Low": "Consider reaching out to a mental health professional. You don't have to go through this alone.",
                    "😐 Low": "Try some self-care activities like a short walk, listening to music, or calling a friend.",
                    "😊 Okay": "Keep maintaining healthy habits and stay connected with supportive people.",
                    "😄 Good": "Great! Consider helping others or engaging in activities you enjoy.",
                    "🌟 Great": "Wonderful! Share your positive energy and remember this feeling for tough days."
                }
                st.success(tips[mood])

        # Mental Health Resources
        with st.expander("📚 Resources"):
            st.markdown("**Common Mental Health Topics:**")
            for disorder in st.session_state.mental_disorders:
                if st.button(f"ℹ️ {disorder}", key=f"info_{disorder}", use_container_width=True):
                    st.info(f"Learn more about {disorder}. Consider speaking with a mental health professional for personalized guidance.")

        # Location-Based Centers
        with st.expander("📍 Find Help Nearby"):
            location_input = st.text_input("Enter your city", key="location_search")
            if st.button("🔍 Search Centers", key="search_nearby"):
                if location_input:
                    search_url = f"https://www.google.com/maps/search/mental+health+centers+near+{location_input.replace(' ', '+')}"
                    st.markdown(f"[🗺️ View Mental Health Centers Near {location_input}]({search_url})")
                else:
                    st.warning("Please enter a city name")

        # Crisis Resources
        with st.expander("☎️ Crisis Support"):
            st.markdown("**24/7 Crisis Hotlines:**")
            for category, numbers in emergency_resources.items():
                st.markdown(f"**{category}:**")
                for number in numbers:
                    st.markdown(f"• {number}")

        # About Section
        with st.expander("ℹ️ About PeacePulse"):
            st.markdown("""
            **PeacePulse** is your compassionate mental health companion, designed to provide:

            • 24/7 emotional support
            • Resource guidance
            • Crisis intervention
            • Professional referrals

            **Remember:** This is not a substitute for professional mental health care.

            ---

            **Created with ❤️ by Eccentric Explorer**

            *"It's absolutely okay not to be okay :)"*

            📅 Enhanced Version - May 2025
            """)