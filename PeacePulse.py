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

# --- Enhanced Custom CSS with consistent theme ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root variables for consistent theming */
    :root {
        --primary-color: #6366f1;
        --primary-light: #818cf8;
        --primary-dark: #4f46e5;
        --secondary-color: #ec4899;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --background: #f8fafc;
        --surface: #ffffff;
        --surface-alt: #f1f5f9;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --text-muted: #94a3b8;
        --border: #e2e8f0;
        --border-light: #f1f5f9;
        --shadow: rgba(15, 23, 42, 0.08);
        --shadow-lg: rgba(15, 23, 42, 0.15);
        --radius: 12px;
        --radius-lg: 16px;
    }
    
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        min-height: 100vh;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Chat container with improved styling */
    .chat-container {
        background: var(--surface);
        border-radius: var(--radius-lg);
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 4px 24px var(--shadow-lg);
        min-height: 500px;
        max-height: 600px;
        overflow-y: auto;
        border: 1px solid var(--border-light);
        scroll-behavior: smooth;
        position: relative;
    }
    
    .chat-container::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: var(--surface-alt);
        border-radius: 3px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: var(--text-muted);
        border-radius: 3px;
    }
    
    .chat-container::-webkit-scrollbar-thumb:hover {
        background: var(--text-secondary);
    }
    
    /* User message with better contrast */
    .user-message {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
        color: white;
        padding: 16px 20px;
        border-radius: 20px 20px 8px 20px;
        margin: 12px 0 12px auto;
        max-width: 75%;
        word-wrap: break-word;
        box-shadow: 0 3px 12px rgba(99, 102, 241, 0.25);
        font-weight: 500;
        line-height: 1.5;
        position: relative;
    }
    
    /* Bot message with improved readability */
    .bot-message {
        background: var(--surface-alt);
        color: var(--text-primary);
        padding: 16px 20px;
        border-radius: 20px 20px 20px 8px;
        margin: 12px auto 12px 0;
        max-width: 75%;
        word-wrap: break-word;
        border: 1px solid var(--border);
        box-shadow: 0 2px 8px var(--shadow);
        line-height: 1.6;
        font-weight: 400;
    }
    
    /* Welcome message */
    .welcome-message {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        padding: 24px;
        border-radius: var(--radius-lg);
        margin: 24px auto;
        text-align: center;
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.3);
        font-weight: 500;
        line-height: 1.6;
    }
    
    /* Message time styling */
    .message-time {
        font-size: 0.75em;
        opacity: 0.8;
        margin-top: 8px;
        text-align: right;
        font-weight: 400;
    }
    
    /* Enhanced header */
    .main-header {
        text-align: center;
        padding: 32px 24px;
        background: var(--surface);
        color: var(--text-primary);
        border-radius: var(--radius-lg);
        margin-bottom: 24px;
        box-shadow: 0 8px 32px var(--shadow-lg);
        border: 1px solid var(--border-light);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
    }
    
    .main-header h1 {
        margin: 0 0 8px 0;
        font-size: 2.5em;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .main-header p {
        margin: 0;
        font-size: 1.2em;
        color: var(--text-secondary);
        font-weight: 500;
    }
    
    /* Emergency button with better accessibility */
    .emergency-button {
        background: linear-gradient(135deg, var(--danger-color) 0%, #dc2626 100%);
        color: white;
        padding: 18px 24px;
        border-radius: var(--radius);
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 16px rgba(239, 68, 68, 0.3);
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-weight: 600;
        font-size: 1.1em;
        border: none;
    }
    
    .emergency-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(239, 68, 68, 0.4);
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
    }
    
    /* Sidebar styling */
    .sidebar-content {
        background: var(--surface);
        border-radius: var(--radius-lg);
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 16px var(--shadow);
        border: 1px solid var(--border-light);
    }
    
    /* Button improvements */
    .stButton > button {
        background: var(--surface);
        color: var(--text-primary);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 12px 16px;
        font-weight: 500;
        transition: all 0.2s ease;
        width: 100%;
        font-family: 'Inter', sans-serif;
    }
    
    .stButton > button:hover {
        background: var(--surface-alt);
        border-color: var(--primary-color);
        color: var(--primary-color);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px var(--shadow);
    }
    
    /* Form input styling */
    .stTextInput > div > div > input {
        background: var(--surface);
        border: 2px solid var(--border);
        border-radius: var(--radius);
        padding: 12px 16px;
        font-size: 1em;
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        outline: none;
    }
    
    /* Select slider improvements */
    .stSelectSlider > div > div {
        background: var(--surface-alt);
        border-radius: var(--radius);
        padding: 8px;
    }
    
    /* Expander styling */
    .streamlit-expander {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        margin-bottom: 12px;
        box-shadow: 0 2px 8px var(--shadow);
        color: #000000;
    }
    
    .streamlit-expander > summary {
        background: var(--surface-alt);
        color: #ffffff;
        font-weight: 1600;
        padding: 16px;
        border-radius: var(--radius);
    }
    
    /* Info and success message styling */
    .stInfo, .stSuccess, .stWarning {
        border-radius: var(--radius);
        border: none;
        font-weight: 500;
    }
    
    .stInfo {
        background: rgba(99, 102, 241, 0.1);
        color: #000000;
    }
    
    .stSuccess {
        background: rgba(16, 185, 129, 0.1);
        color: #047857;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.1);
        color: #92400e;
    }
    
    /* Typography improvements */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary);
        font-weight: 600;
        line-height: 1.3;
    }
    
    p {
        color: var(--text-secondary);
        line-height: 1.6;
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-color: var(--primary-color) !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        
        .user-message, .bot-message {
            max-width: 90%;
            padding: 12px 16px;
        }
        
        .main-header h1 {
            font-size: 2em;
        }
        
        .chat-container {
            min-height: 400px;
            max-height: 500px;
            padding: 16px;
        }
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
col1, col2, col3 = st.columns([2.5, 6, 2.5])

# Left Sidebar: Conversation History
with col1:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown("### 💬 Conversations")
    
    # New conversation button
    if st.button("➕ New Chat", key="new_chat", use_container_width=True):
        create_new_conversation()
        st.rerun()
    
    st.markdown("---")
    
    # Display conversation history
    if st.session_state.conversations:
        for i, convo in enumerate(st.session_state.conversations):
            button_style = "🟢" if i == st.session_state.active_conversation else "📝"
            
            if st.button(
                f"{button_style} {convo['title'][:22]}...", 
                key=f"convo_{i}",
                help=f"Started: {convo['date']}",
                use_container_width=True
            ):
                st.session_state.active_conversation = i
                st.rerun()
    else:
        st.info("No conversations yet. Start a new chat!")
    
    st.markdown('</div>', unsafe_allow_html=True)

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
        html = '<div class="chat-container">'

        if st.session_state.active_conversation >= 0:
            active_convo = st.session_state.conversations[st.session_state.active_conversation]

            if not active_convo["messages"]:
                html += f"""
                <div class="welcome-message">
                    <strong>Hello! I'm PeacePulse, your mental health companion.</strong><br>
                    I'm here to listen, support, and help guide you toward the resources you need. How are you feeling today? 😊
                    <div class="message-time">{get_current_time()}</div>
                </div>
                """
            
            for msg in active_convo["messages"]:
                if msg["sender"] == "user":
                    html += f"""
                    <div class="user-message">
                        {msg["message"]}
                        <div class="message-time">{msg["time"]}</div>
                    </div>
                    """
                else:
                    html += f"""
                    <div class="bot-message">
                        {msg["message"]}
                        <div class="message-time">{msg["time"]}</div>
                    </div>
                    """

        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

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
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    
    # Emergency Help Button
    st.markdown("""
    <div class="emergency-button">
        🚨 Emergency Help
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
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