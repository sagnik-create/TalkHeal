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
    /* Chat container styling */
    .chat-container {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        min-height: 500px;
        max-height: 600px;
        overflow-y: auto;
        border: 1px solid #e0e0e0;
    }
    
    /* User message styling */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 5px 18px;
        margin: 10px 0 10px auto;
        max-width: 80%;
        word-wrap: break-word;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    /* Bot message styling */
    .bot-message {
        background: #f8f9fa;
        color: #333;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 5px;
        margin: 10px auto 10px 0;
        max-width: 80%;
        word-wrap: break-word;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Welcome message styling */
    .welcome-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 15px;
        margin: 20px auto;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }
    
    /* Message time styling */
    .message-time {
        font-size: 0.75em;
        opacity: 0.7;
        margin-top: 5px;
        text-align: right;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 20px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 3px 15px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.2em;
        font-weight: 600;
    }
    
    .main-header p {
        margin: 5px 0 0 0;
        font-size: 1.1em;
        opacity: 0.9;
    }
    
    /* Emergency button styling */
    .emergency-button {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 3px 10px rgba(255,65,108,0.3);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .emergency-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255,65,108,0.4);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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
    <div class="main-header">
        <h1>PeacePulse</h1>
        <p>Your Mental Health Companion 💙</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Ensure we have at least one conversation
    if not st.session_state.conversations:
        create_new_conversation()
    
    # Create chat container
    chat_container = st.container()
    
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        if st.session_state.active_conversation >= 0:
            active_convo = st.session_state.conversations[st.session_state.active_conversation]
            
            if not active_convo["messages"]:
                st.markdown(f"""
                <div class="welcome-message">
                    <strong>Hello! I'm PeacePulse, your mental health companion.</strong><br>
                    I'm here to listen, support, and help guide you toward the resources you need. How are you feeling today? 😊
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
    <div class="emergency-button">
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