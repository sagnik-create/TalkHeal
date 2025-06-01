import streamlit as st
import webbrowser
from datetime import datetime
from core.utils import create_new_conversation

# Emergency contacts and resources
emergency_resources = {
    "Crisis Hotlines": [
        "National Suicide Prevention Lifeline: 988",
        "Crisis Text Line: Text HOME to 741741",
        "SAMHSA National Helpline: 1-800-662-4357"
    ],
    "International": [
        "India: 9152987821 (AASRA)",
        "UK: 116 123 (Samaritans)",
        "Australia: 13 11 14 (Lifeline)"
    ]
}

# Define a broader set of resources with more details for filtering
mental_health_resources_full = {
    "Depression & Mood Disorders": {
        "description": "Information on understanding and coping with depression, persistent depressive disorder, and other mood-related challenges.",
        "links": [
            {"label": "NIMH - Depression", "url": "https://www.nimh.nih.gov/health/topics/depression"},
            {"label": "Mayo Clinic - Depression", "url": "https://www.mayoclinic.org/diseases-conditions/depression/symptoms-causes/syc-20356007"}
        ]
    },
    "Anxiety & Panic Disorders": {
        "description": "Guidance on managing generalized anxiety, social anxiety, panic attacks, and phobias.",
        "links": [
            {"label": "ADAA - Anxiety & Depression", "url": "https://adaa.org/"},
            {"label": "NIMH - Anxiety Disorders", "url": "https://www.nimh.nih.gov/health/topics/anxiety-disorders"}
        ]
    },
    "Bipolar Disorder": {
        "description": "Understanding the complexities of bipolar disorder, including mood swings and treatment options.",
        "links": [
            {"label": "NIMH - Bipolar Disorder", "url": "https://www.nimh.nih.gov/health/topics/bipolar-disorder"}
        ]
    },
    "PTSD & Trauma": {
        "description": "Resources for individuals experiencing post-traumatic stress disorder and other trauma-related conditions.",
        "links": [
            {"label": "PTSD: National Center", "url": "https://www.ptsd.va.gov/"}
        ]
    },
    "OCD & Related Disorders": {
        "description": "Support and information for obsessive-compulsive disorder, body dysmorphic disorder, and hoarding disorder.",
        "links": [
            {"label": "IOCDF - OCD", "url": "https://iocdf.org/"}
        ]
    },
    "Coping Skills & Self-Care": {
        "description": "Practical strategies and techniques for stress management, emotional regulation, and daily well-being.",
        "links": [
            {"label": "HelpGuide - Stress Management", "url": "https://www.helpguide.org/articles/stress/stress-management.htm"}
        ]
    },
    "Therapy & Treatment Options": {
        "description": "Overview of various therapeutic approaches, including CBT, DBT, and finding a therapist.",
        "links": [
            {"label": "APA - Finding a Therapist", "url": "https://www.apa.org/helpcenter/choose-therapist"}
        ]
    }
}


def render_sidebar():
    """Renders the left and right sidebars."""
    with st.sidebar:
        # --- 1. Conversations & New Chat (with Quick Start Prompts) ---
        st.markdown("### 💬 Conversations")

        # Initialize state for quick start prompts visibility
        if "show_quick_start_prompts" not in st.session_state:
            st.session_state.show_quick_start_prompts = False

        if st.button("➕ New Chat", key="new_chat", use_container_width=True):
            create_new_conversation()
            st.session_state.show_quick_start_prompts = True # Show prompts after new chat
            st.rerun()

        # Display quick start prompts if enabled
        if st.session_state.show_quick_start_prompts:
            st.markdown("---")
            st.markdown("**Start with a common topic:**")
            quick_prompts = [
                "Feeling overwhelmed",
                "Need to vent about my day",
                "How to manage stress?",
                "Tell me about anxiety"
            ]
            
            # Use columns for a more compact layout of quick prompts
            qp_cols = st.columns(2)
            for i, prompt in enumerate(quick_prompts):
                with qp_cols[i % 2]: # Distribute buttons across 2 columns
                    if st.button(f"✨ {prompt}", key=f"qp_{i}", use_container_width=True):
                        # This sets a temporary value that can be read by chat_interface
                        st.session_state.pre_filled_chat_input = prompt
                        st.session_state.show_quick_start_prompts = False # Hide after selection
                        st.rerun() # Rerun to update the main chat input

            st.markdown("---") # Separator after quick prompts


        # Display conversation history with visual timeline elements
        st.markdown("### Your Chat History")
        if st.session_state.conversations:
            # Add a search bar for conversations
            convo_search = st.text_input("Search chats...", key="convo_search", placeholder="Type to search...", label_visibility="collapsed")
            
            filtered_conversations = [
                convo for convo in st.session_state.conversations 
                if convo_search.lower() in convo['title'].lower()
            ]
            
            if not filtered_conversations:
                st.info("No matching conversations found.")

            for i, convo in enumerate(filtered_conversations):
                # Using a dummy column to mimic a timeline dot/line if desired with CSS
                # For direct Streamlit, we focus on styling the button itself
                is_active = i == st.session_state.active_conversation
                button_style_icon = "🟢" if is_active else "📝"
                
                # Apply custom class for timeline effect via CSS
                btn_css_class = "timeline-active-convo" if is_active else "timeline-convo"

                # Streamlit button needs to be wrapped in HTML to apply direct class
                # This is a bit of a hack, consider custom components for cleaner HTML/JS bridge
                button_html = f"""
                    <div class="{btn_css_class}">
                        <button class="stButton" style="width: 100%;" key="convo_html_{i}" 
                            onclick="window.parent.postMessage({{
                                type: 'streamlit:setComponentValue',
                                key: 'convo_native_{i}',
                                value: true
                            }}, '*')"
                        >
                            {button_style_icon} {convo['title'][:22]}...
                            <br><small style="font-size:0.7em; opacity:0.7;">Started: {convo['date']}</small>
                        </button>
                    </div>
                """
                # For simplicity and direct Streamlit interaction, let's use st.button with type
                # and apply global CSS for 'primary' button on active conversation.
                if st.button(
                    f"{button_style_icon} {convo['title'][:22]}...",
                    key=f"convo_{i}",
                    help=f"Started: {convo['date']}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary" # This triggers the active conversation CSS
                ):
                    st.session_state.active_conversation = i
                    st.rerun()
        else:
            st.info("No conversations yet. Start a new chat!")
        
        st.markdown("---") # Separator before emergency help

        # --- 2. Emergency Help Button ---
        st.markdown("""
        <div class="emergency-button" onclick="window.open('https://www.mentalhealth.gov/get-help/immediate-help', '_blank')">
            🚨 Emergency Help
        </div>
        """, unsafe_allow_html=True)

        st.markdown("") # Add a little space

        # --- 3. Dynamic Mood Tracker & Micro-Journal ---
        with st.expander("🧠 Mental Health Check"):
            st.markdown("**How are you feeling today?**")
            
            mood_options_map = {
                "😔 Very Low": "very_low",
                "😐 Low": "low",
                "😊 Okay": "okay",
                "😄 Good": "good",
                "🌟 Great": "great"
            }
            mood_labels = list(mood_options_map.keys())

            # Use st.radio for mood selection, styled horizontally
            selected_mood_label = st.radio(
                "Mood Scale",
                options=mood_labels,
                index=mood_labels.index("😊 Okay") if "😊 Okay" in mood_labels else 2, # Default to Okay
                key="mood_selector_radio",
                horizontal=True,
                label_visibility="collapsed"
            )
            
            st.session_state.current_mood_val = mood_options_map[selected_mood_label]

            # Conditional Journal Prompt based on selected mood
            if st.session_state.current_mood_val:
                st.markdown("") # Small space
                journal_prompt_text = {
                    "very_low": "What's weighing on your mind today?",
                    "low": "What are your thoughts right now?",
                    "okay": "Anything specific on your mind today?",
                    "good": "What made you feel good today?",
                    "great": "What's making you shine today?"
                }.get(st.session_state.current_mood_val, "Reflect on your mood:")

                # Initialize journal entry for the current session
                if "mood_journal_entry" not in st.session_state:
                    st.session_state.mood_journal_entry = ""

                st.text_area(
                    f"✏️ {journal_prompt_text}",
                    key="mood_journal_area",
                    value=st.session_state.mood_journal_entry,
                    height=70
                )
                
                tips_for_mood = {
                    "very_low": "Remember, it's okay not to be okay. Consider connecting with a professional.",
                    "low": "Even small steps help. Try a brief mindful moment or gentle activity.",
                    "okay": "Keep nurturing your well-being. What's one thing you can do to maintain this?",
                    "good": "That's wonderful! Savor this feeling and perhaps share your positivity.",
                    "great": "Fantastic! How can you carry this energy forward into your day?"
                }.get(st.session_state.current_mood_val, "A general tip for your mood.")

                st.markdown("") # Small space
                if st.button("Get Tip & Save Entry", key="save_mood_entry", use_container_width=True):
                    st.success(tips_for_mood)
                    # Here you would typically save this to a persistent store (database/file)
                    # For this no-backend scenario, we'll just acknowledge.
                    st.info(f"Your mood entry for '{selected_mood_label}' has been noted for this session.")
                    st.session_state.mood_journal_entry = "" # Clear after "saving"
                    st.session_state.current_mood_val = None # Reset mood selection visually
                    st.rerun() # Rerun to clear inputs and reset state

        # --- 4. Resource Hub with Categories & Search ---
        with st.expander("📚 Resources & Knowledge Base"):
            st.markdown("**Explore topics or search for help:**")
            
            resource_search_query = st.text_input("Search resources...", key="resource_search", placeholder="e.g., 'anxiety tips', 'therapy'", label_visibility="collapsed")
            
            # Filter resources based on search query
            filtered_topics = [
                topic for topic in mental_health_resources_full
                if resource_search_query.lower() in topic.lower() or \
                   any(resource_search_query.lower() in link['label'].lower() for link in mental_health_resources_full[topic]['links']) or \
                   resource_search_query.lower() in mental_health_resources_full[topic]['description'].lower()
            ]

            if resource_search_query and not filtered_topics:
                st.info("No resources found matching your search.")
            
            # Display topics using tabs or expanders
            if not resource_search_query: # Show tabs only if no search query
                resource_tabs = st.tabs(list(mental_health_resources_full.keys()))
                
                for i, tab_title in enumerate(mental_health_resources_full.keys()):
                    with resource_tabs[i]:
                        topic_data = mental_health_resources_full[tab_title]
                        st.markdown(f"**{tab_title}**")
                        st.info(topic_data['description'])
                        for link in topic_data['links']:
                            st.markdown(f"• [{link['label']}]({link['url']})")
                        st.markdown("---") # Separator within tabs
            else: # Show filtered results as expanders if there's a search query
                for topic in filtered_topics:
                    with st.expander(f"📚 {topic}"):
                        topic_data = mental_health_resources_full[topic]
                        st.info(topic_data['description'])
                        for link in topic_data['links']:
                            st.markdown(f"• [{link['label']}]({link['url']})")
                        st.markdown("---")

        # Location-Based Centers (remains the same)
        with st.expander("📍 Find Help Nearby"):
            location_input = st.text_input("Enter your city", key="location_search")
            if st.button("🔍 Search Centers", key="search_nearby"):
                if location_input:
                    # Using a more robust Google Maps search URL
                    search_url = f"https://www.google.com/maps/search/mental+health+centers+near+{location_input.replace(' ', '+')}"
                    st.markdown(f"[🗺️ View Mental Health Centers Near {location_input}]({search_url})")
                else:
                    st.warning("Please enter a city name")

        # Crisis Resources (remains the same)
        with st.expander("☎️ Crisis Support"):
            st.markdown("**24/7 Crisis Hotlines:**")
            for category, numbers in emergency_resources.items():
                st.markdown(f"**{category}:**")
                for number in numbers:
                    st.markdown(f"• {number}")

        # About Section (remains the same)
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