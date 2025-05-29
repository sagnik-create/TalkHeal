import streamlit as st
from core.utils import get_current_time, get_ai_response

def render_chat_interface():
    """Renders the main chat message display area."""
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

def handle_chat_input(model):
    """Handles the user input for the chat and generates AI responses."""
    st.markdown("---")

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
                ai_response = get_ai_response(user_input.strip(), model)
            
            active_convo["messages"].append({
                "sender": "bot", 
                "message": ai_response, 
                "time": get_current_time()
            })
            
            # Refresh the page
            st.rerun()