import streamlit as st
import base64
import time
from datetime import datetime
import random
import google.generativeai as genai

# Configure Gemini (with your API key)
genai.configure(api_key="AIzaSyBeulOMD_D6_AUVdf1MKG6wnjxQ_gaSYsw")
model = genai.GenerativeModel('gemini-2.0-flash')

# --- Set page configuration ---
st.set_page_config(
    page_title="PeacePulse",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
    /* Main app background and text */
    .stApp {
        background-color: #f0f2f5;
        color: #111111;
    }
    
    /* Sidebar styling */
    [data-testid=stSidebar] {
        background-color: #f7f7f7;
        padding: 1rem;
        border-right: 1px solid #e0e0e0;
    }
    
    /* Header styling */
    .header {
        display: flex;
        align-items: center;
        background-color: #ffffff;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Chat container */
    .chat-container {
        background-color: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        height: 500px;
        overflow-y: auto;
    }
    
    /* Message bubbles */
    .user-message {
        background-color: #e1f5fe;
        padding: 0.8rem;
        border-radius: 15px 15px 0 15px;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-left: auto;
        color: #333;
    }
    
    .bot-message {
        background-color: #f5f5f5;
        padding: 0.8rem;
        border-radius: 15px 15px 15px 0;
        margin: 0.5rem 0;
        max-width: 80%;
        color: #333;
    }
    
    /* Input box */
    .chat-input {
        border-radius: 20px !important;
        border: 1px solid #e0e0e0 !important;
        padding: 0.5rem 1rem !important;
    }
    
    /* Feature cards */
    .feature-card {
        background-color: white;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Button styling */
    .stButton button {
        border-radius: 20px;
        padding: 0.3rem 1rem;
        background-color: #3498db;
        color: white;
        border: none;
        font-weight: 500;
    }
    
    .stButton button:hover {
        background-color: #2980b9;
    }
    
    /* Message metadata */
    .message-time {
        font-size: 0.7rem;
        color: #888;
        margin-top: 0.2rem;
        text-align: right;
    }
    
    /* Conversation history styling */
    .convo-item {
        padding: 0.7rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        background-color: white;
        cursor: pointer;
        transition: background-color 0.2s;
        border-left: 3px solid transparent;
    }
    
    .convo-item:hover {
        background-color: #e8f4f8;
        border-left: 3px solid #3498db;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Additional right panel styling */
    .right-panel {
        background-color: white;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Disorder list */
    .disorder-item {
        padding: 0.5rem;
        border-bottom: 1px solid #f0f0f0;
    }
    
    /* Help button */
    .help-button {
        background-color: #e74c3c;
        color: white;
        padding: 1rem;
        text-align: center;
        border-radius: 10px;
        font-weight: bold;
        cursor: pointer;
        margin: 1rem 0;
    }
    
    /* Video thumbnail */
    .video-thumbnail {
        position: relative;
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 1rem;
    }
    
    .play-button {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: rgba(255,255,255,0.7);
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "conversations" not in st.session_state:
    st.session_state.conversations = [
        {"title": "Hello there!", "date": "Today", "messages": []},
        {"title": "I've been feeling overwhelmed lately. Can you provide tips on...", "date": "Today", "messages": []},
        {"title": "I'm curious about therapy options. What types are available...", "date": "Today", "messages": []},
        {"title": "I've been struggling with sleep issues. Any suggestions or...", "date": "December, 28, 2023", "messages": []},
        {"title": "I'm looking for online support groups for individuals dealing...", "date": "December, 28, 2023", "messages": []},
        {"title": "I'm a parent concerned about my child's mental health. How can I...", "date": "November, 11, 2023", "messages": []},
        {"title": "I think I might have symptoms of ADHD. Can you provide...", "date": "November, 11, 2023", "messages": []},
        {"title": "Hi, chat.", "date": "November, 11, 2023", "messages": []}
    ]

if "active_conversation" not in st.session_state:
    st.session_state.active_conversation = 0

if "mental_disorders" not in st.session_state:
    st.session_state.mental_disorders = [
        "Depression",
        "Anxiety Disorders",
        "Bipolar Disorder",
        "Schizophrenia",
        "Obsessive-Compulsive Disorder (OCD)"
    ]

# Helper Functions
def get_current_time():
    return datetime.now().strftime("%I:%M %p")

def create_new_conversation(initial_message=None):
    new_convo = {
        "title": initial_message[:30] + "..." if initial_message and len(initial_message) > 30 else "New Conversation",
        "date": "Today",
        "messages": []
    }
    if initial_message:
        new_convo["messages"].append({"sender": "user", "message": initial_message, "time": get_current_time()})
    
    st.session_state.conversations.insert(0, new_convo)
    st.session_state.active_conversation = 0
    return 0

# Layout: Top Navigation
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
with col1:
    st.markdown('<div style="text-align: center; font-weight: bold;">Home</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div style="text-align: center;">Chat</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div style="text-align: center;">Activities</div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div style="text-align: center;">Resources</div>', unsafe_allow_html=True)
with col5:
    st.markdown('<div style="text-align: right;">👤</div>', unsafe_allow_html=True)

st.markdown("---")

# Main Layout: 3 columns
sidebar_col, main_col, right_col = st.columns([1, 2, 1])

# Sidebar: Conversation History
with sidebar_col:
    st.markdown("### Today")
    
    # Display recent conversations
    for i, convo in enumerate(st.session_state.conversations):
        if i > 0 and convo["date"] != st.session_state.conversations[i-1]["date"]:
            st.markdown(f"### {convo['date']}")
        
        is_active = i == st.session_state.active_conversation
        background = "#e8f4f8" if is_active else "white"
        border = "3px solid #3498db" if is_active else "3px solid transparent"
        
        # Create clickable conversation item
        if st.markdown(f"""
        <div class="convo-item" style="background-color: {background}; border-left: {border};" onclick="alert('Clicked')">
            {convo["title"]}
        </div>
        """, unsafe_allow_html=True):
            st.session_state.active_conversation = i
    
    # New conversation button
    if st.button("New Request", key="new_request"):
        create_new_conversation()

# Main Chat Area
with main_col:
    st.markdown("<h2>AI Mental Chat Assistant</h2>", unsafe_allow_html=True)
    st.markdown("<p>Let's explore your thoughts together and guide you towards the right professional assistance.</p>", unsafe_allow_html=True)
    
    st.markdown("### Today")
    
    # Display chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Initial greeting message if no messages
    active_convo = st.session_state.conversations[st.session_state.active_conversation]
    if not active_convo["messages"]:
        st.markdown(f"""
        <div class="bot-message">
            Let's explore your thoughts together and guide you towards the right professional assistance 😊
            <div class="message-time">{get_current_time()}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display existing messages
    for msg in active_convo["messages"]:
        if msg["sender"] == "user":
            st.markdown(f"""
            <div class="user-message">
                {msg["message"]}
                <div class="message-time">{msg["time"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="bot-message">
                {msg["message"]}
                <div class="message-time">{msg["time"]}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    chat_col1, chat_col2 = st.columns([4, 1])
    
    with chat_col1:
        user_input = st.text_input("Write your request...", key="user_message", label_visibility="collapsed")
    
    with chat_col2:
        send_pressed = st.button("Send", key="send_button")
    
    if send_pressed and user_input:
        # Add user message
        current_time = get_current_time()
        active_convo = st.session_state.conversations[st.session_state.active_conversation]
        active_convo["messages"].append({"sender": "user", "message": user_input, "time": current_time})
        
        # Update conversation title if it's the first message
        if len(active_convo["messages"]) == 1:
            active_convo["title"] = user_input[:30] + "..." if len(user_input) > 30 else user_input
        
        # Generate AI response
        try:
            response = model.generate_content(user_input).text
        except:
            response = "I'm here to listen and help. Could you share more about what you're experiencing so I can better understand how to support you?"
        
        # Add AI response
        active_convo["messages"].append({"sender": "bot", "message": response, "time": get_current_time()})
        
        # Force refresh
        st.experimental_rerun()

# Right Column: Features
with right_col:
    # First feature card - Video
    st.markdown("""
    <div class="video-thumbnail" style="background-color: #333; height: 150px; display: flex; justify-content: center; align-items: center; color: white;">
        <div class="play-button">▶</div>
        <div style="position: absolute; bottom: 10px; left: 10px; right: 10px; color: white;">
            <div style="font-weight: bold;">10 technics to overcome stress</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Mental disorders list
    st.markdown("""
    <div class="right-panel">
        <h4>Here is a short list of some common mental disorders:</h4>
    """, unsafe_allow_html=True)
    
    for disorder in st.session_state.mental_disorders:
        st.markdown(f"""
        <div class="disorder-item">{disorder}</div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Help button
    st.markdown("""
    <div class="help-button">
        I need Help!
    </div>
    """, unsafe_allow_html=True)
    
    # Meditation video
    st.markdown("""
    <div class="video-thumbnail" style="background-color: #333; height: 150px; display: flex; justify-content: center; align-items: center; color: white;">
        <div class="play-button">▶</div>
        <div style="position: absolute; bottom: 10px; left: 10px; right: 10px; color: white;">
            <div style="font-weight: bold;">Meditation</div>
            <div style="font-size: 0.8rem;">Calm Your Mind, Heal Your Soul: Embrace the Power of Meditation.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Location-Based Centers Section
    with st.expander("📍 Location-Based Centers"):
        st.markdown("<h4>Find Mental Health Centers Near You</h4>", unsafe_allow_html=True)
        location_input = st.text_input("Enter your city or location", key="location_input")
        if st.button("📌 Search Nearby Centers", key="search_centers"):
            if location_input:
                st.success(f"Mental health centers found in {location_input}:")
                st.markdown(f"""
                • Center for Mental Wellness - {location_input}
                • {location_input} Psychological Services
                • Mindful Health Clinic - {location_input}
                """)
                map_url = f"https://www.google.com/maps/search/Mental+Hospitals+and+trauma+care+centres+in+{location_input.replace(' ', '+')}"
                st.markdown(f"[View on Google Maps]({map_url})")

    # Professionals Section
    with st.expander("👩‍⚕️ Mental Health Professionals"):
        st.markdown("<h4>Connect with Specialists</h4>", unsafe_allow_html=True)
        
        # Sample professionals list
        professionals = [
            {"name": "Dr. Mezel Agnes", "specialty": "Anxiety, Depression", "contact": "mezelidoctor@gmail.com"},
            {"name": "Dr. Sarah Johnson", "specialty": "Trauma, PTSD", "contact": "drsarah@mentalhealthclinic.com"},
            {"name": "Dr. James Wilson", "specialty": "Addiction, Substance Abuse", "contact": "drwilson@recoverycentre.org"}
        ]
        
        for prof in professionals:
            st.markdown(f"""
            <div style="padding: 10px; border-bottom: 1px solid #eee;">
                <b>{prof['name']}</b><br>
                Specialties: {prof['specialty']}<br>
                Contact: <a href="mailto:{prof['contact']}">{prof['contact']}</a>
            </div>
            """, unsafe_allow_html=True)
    
    # Issues Section
    with st.expander("💬 Common Issues"):
        st.markdown("<h4>Common Mental Health Concerns</h4>", unsafe_allow_html=True)
        issues = ["Anxiety", "Depression", "Stress", "Sleep Problems", "Relationship Issues", "Self-Esteem", "Trauma", "Addiction"]
        
        issue_input = st.text_input("Search for specific issues", key="issue_search")
        filtered_issues = [issue for issue in issues if issue_input.lower() in issue.lower()] if issue_input else issues
        
        for issue in filtered_issues:
            st.markdown(f"""
            <div style="padding: 8px; margin: 5px; background-color: #f1f1f1; border-radius: 5px; display: inline-block;">
                {issue}
            </div>
            """, unsafe_allow_html=True)
    
    # Developer Info
    with st.expander("👨‍💻 Developer Info"):
        st.markdown("""
        <div style="text-align: center;">
            <h4>Developed By:</h4>
            <p><b>Eccentric Explorer</b><br>
            <i>"It's absolutely okay not to be okay :)"</i>
            </p>
            <p>📅 Date: May 03, 2025</p>
        </div>
        """, unsafe_allow_html=True)