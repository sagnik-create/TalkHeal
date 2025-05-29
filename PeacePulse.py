import streamlit as st
import base64
import time
from datetime import datetime
import random
import google.generativeai as genai
import webbrowser

# Configure Gemini (replace with your API key)
try:
    genai.configure(api_key="AIzaSyBeulOMD_D6_AUVdf1MKG6wnjxQ_gaSYsw")
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error("Failed to configure Gemini API. Please check your API key.")

# --- Set page configuration ---
st.set_page_config(
    page_title="PeacePulse - Mental Health Support",
    page_icon="💙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Enhanced Custom CSS ---
st.markdown("""
<style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #2c3e50;
    }
    
    /* Sidebar styling */
    [data-testid=stSidebar] {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-right: none;
        box-shadow: 2px 0 20px rgba(0,0,0,0.1);
    }
    
    /* Main content container */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    
    /* Header styling */
    .app-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .app-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .app-subtitle {
        font-size: 1.2rem;
        color: #7f8c8d;
        font-weight: 400;
    }
    
    /* Chat container */
    .chat-container {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        height: 400px;
        overflow-y: auto;
        border: 1px solid rgba(102, 126, 234, 0.2);
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Message bubbles */
    .user-message {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0;
        max-width: 75%;
        margin-left: auto;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        animation: slideInRight 0.3s ease-out;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        color: #2c3e50;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem 0;
        max-width: 75%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        animation: slideInLeft 0.3s ease-out;
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        padding: 0.8rem 1.5rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Feature cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(102, 126, 234, 0.2);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        border-color: #667eea;
    }
    
    /* Emergency button */
    .emergency-button {
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        color: white;
        padding: 1rem;
        text-align: center;
        border-radius: 15px;
        font-weight: bold;
        cursor: pointer;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3);
        transition: all 0.3s ease;
    }
    
    .emergency-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(231, 76, 60, 0.4);
    }
    
    /* Conversation items */
    .convo-item {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        background: rgba(255, 255, 255, 0.8);
        cursor: pointer;
        transition: all 0.3s ease;
        border: 1px solid transparent;
    }
    
    .convo-item:hover {
        background: rgba(102, 126, 234, 0.1);
        border-color: #667eea;
        transform: translateX(5px);
    }
    
    .convo-item.active {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
    }
    
    /* Message time */
    .message-time {
        font-size: 0.75rem;
        opacity: 0.7;
        margin-top: 0.5rem;
        text-align: right;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(102, 126, 234, 0.1);
        border-radius: 10px;
        font-weight: 600;
    }
    
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "conversations" not in st.session_state:
    st.session_state.conversations = []

if "active_conversation" not in st.session_state:
    st.session_state.active_conversation = -1

if "mental_disorders" not in st.session_state:
    st.session_state.mental_disorders = [
        "Depression & Mood Disorders",
        "Anxiety & Panic Disorders", 
        "Bipolar Disorder",
        "PTSD & Trauma",
        "OCD & Related Disorders",
        "Eating Disorders",
        "Substance Use Disorders",
        "ADHD & Neurodevelopmental",
        "Personality Disorders",
        "Sleep Disorders"
    ]

# Helper Functions
def get_current_time():
    return datetime.now().strftime("%I:%M %p")

def create_new_conversation(initial_message=None):
    new_convo = {
        "id": len(st.session_state.conversations),
        "title": initial_message[:30] + "..." if initial_message and len(initial_message) > 30 else "New Conversation",
        "date": datetime.now().strftime("%B %d, %Y"),
        "messages": []
    }
    
    if initial_message:
        new_convo["messages"].append({
            "sender": "user", 
            "message": initial_message, 
            "time": get_current_time()
        })
    
    st.session_state.conversations.insert(0, new_convo)
    st.session_state.active_conversation = 0
    return 0

def get_ai_response(user_message):
    """Generate AI response with mental health context"""
    mental_health_prompt = f"""
    You are a compassionate mental health support chatbot named PeacePulse. Your role is to:
    1. Provide empathetic, supportive responses
    2. Encourage professional help when needed
    3. Never diagnose or provide medical advice
    4. Be warm, understanding, and non-judgmental
    5. Ask follow-up questions to better understand the user's situation
    6. Provide coping strategies and resources when appropriate
    
    User message: {user_message}
    
    Respond in a caring, supportive manner (keep response under 150 words):
    """
    
    try:
        response = model.generate_content(mental_health_prompt)
        return response.text
    except Exception as e:
        return "I'm here to listen and support you. Sometimes I have trouble connecting, but I want you to know that your feelings are valid and you're not alone. Would you like to share more about what you're experiencing?"

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

# Main Layout
col1, col2, col3 = st.columns([2, 6, 2])

# Left Sidebar: Conversation History
with col1:
    st.markdown("### 💬 Conversations")
    
    # New conversation button
    if st.button("➕ New Chat", key="new_chat", use_container_width=True):
        create_new_conversation()
        st.rerun()
    
    st.markdown("---")
    
    # Display conversation history
    if st.session_state.conversations:
        for i, convo in enumerate(st.session_state.conversations):
            active_class = "active" if i == st.session_state.active_conversation else ""
            
            if st.button(
                f"📝 {convo['title'][:25]}...", 
                key=f"convo_{i}",
                help=f"Started: {convo['date']}",
                use_container_width=True
            ):
                st.session_state.active_conversation = i
                st.rerun()
    else:
        st.info("No conversations yet. Start a new chat!")

# Main Chat Area
with col2:
    # Header
    st.markdown("""
    <div class="app-header">
        <div class="app-title">PeacePulse</div>
        <div class="app-subtitle">Your Mental Health Companion 💙</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Ensure we have at least one conversation
    if not st.session_state.conversations:
        create_new_conversation()
    
    # Display chat messages
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if st.session_state.active_conversation >= 0:
        active_convo = st.session_state.conversations[st.session_state.active_conversation]
        
        if not active_convo["messages"]:
            st.markdown(f"""
            <div class="bot-message">
                Hello! I'm PeacePulse, your mental health companion. I'm here to listen, support, and help guide you toward the resources you need. How are you feeling today? 😊
                <div class="message-time">{get_current_time()}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Display conversation messages
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
    
    # Chat input area
    st.markdown("---")
    
    # Use a form to handle input properly
    with st.form(key="chat_form", clear_on_submit=True):
        input_col, send_col = st.columns([5, 1])
        
        with input_col:
            user_input = st.text_input(
                "Share your thoughts...", 
                key="message_input", 
                label_visibility="collapsed",
                placeholder="Type your message here..."
            )
        
        with send_col:
            send_pressed = st.form_submit_button("Send", use_container_width=True)
    
    # Handle message sending
    if send_pressed and user_input.strip():
        if st.session_state.active_conversation >= 0:
            current_time = get_current_time()
            active_convo = st.session_state.conversations[st.session_state.active_conversation]
            
            # Add user message
            active_convo["messages"].append({
                "sender": "user", 
                "message": user_input.strip(), 
                "time": current_time
            })
            
            # Update conversation title if it's the first message
            if len(active_convo["messages"]) == 1:
                active_convo["title"] = user_input[:30] + "..." if len(user_input) > 30 else user_input
            
            # Generate and add AI response
            with st.spinner("PeacePulse is thinking..."):
                ai_response = get_ai_response(user_input.strip())
            
            active_convo["messages"].append({
                "sender": "bot", 
                "message": ai_response, 
                "time": get_current_time()
            })
            
            # Refresh the page
            st.rerun()

# Right Sidebar: Resources and Tools
with col3:
    # Emergency Help Button
    st.markdown("""
    <div class="emergency-button" onclick="alert('In case of emergency, please call 911 or your local emergency services immediately.')">
        🚨 Emergency Help
    </div>
    """, unsafe_allow_html=True)
    
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
                search_url = f"https://www.google.com/maps/search/mental+health+centers+{location_input.replace(' ', '+')}"
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

# Auto-scroll chat to bottom (JavaScript injection)
st.markdown("""
<script>
function scrollToBottom() {
    var chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}
setTimeout(scrollToBottom, 100);
</script>
""", unsafe_allow_html=True)