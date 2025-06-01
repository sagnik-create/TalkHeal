import streamlit as st
from core.utils import get_current_time, get_ai_response

def render_chat_interface():
    """Renders the main chat message display area in a single scrollable container."""
    
    if st.session_state.active_conversation >= 0:
        active_convo = st.session_state.conversations[st.session_state.active_conversation]
        
        # Build the entire chat content as one HTML string
        chat_html = '<div class="chat-container">'
        
        # Show welcome message if no messages exist
        if not active_convo["messages"]:
            chat_html += f"""
            <div class="welcome-message">
                <strong>Hello! I'm PeacePulse, your mental health companion.</strong><br>
                I'm here to listen, support, and help guide you toward the resources you need. How are you feeling today? 😊
                <span class="message-time">{get_current_time()}</span>
            </div>
            """
        
        # Add all messages to the HTML string
        for msg in active_convo["messages"]:
            if msg["sender"] == "user":
                chat_html += f"""
                <div class="user-message">
                    {msg["message"]}
                    <span class="message-time">{msg["time"]}</span>
                </div>
                """
            else:
                chat_html += f"""
                <div class="bot-message">
                    {msg["message"]}
                    <span class="message-time">{msg["time"]}</span>
                </div>
                """
        
        # Close the chat container
        chat_html += '</div>'
        
        # Render the entire chat as one HTML block
        st.markdown(chat_html, unsafe_allow_html=True)

def handle_chat_input(model):
    """Handles the user input for the chat and generates AI responses."""
    
    # Create a form for chat input
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input(
                "Share your thoughts...", 
                key="message_input", 
                label_visibility="collapsed",
                placeholder="Type your message here..."
            )
        
        with col2:
            send_pressed = st.form_submit_button("Send", use_container_width=True)
    
    # Process the input when send is pressed
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
                title = user_input[:30] + "..." if len(user_input) > 30 else user_input
                active_convo["title"] = title
            
            # Generate AI response with spinner
            with st.spinner("PeacePulse is thinking..."):
                try:
                    ai_response = get_ai_response(user_input.strip(), model)
                    
                    # Add AI response
                    active_convo["messages"].append({
                        "sender": "bot", 
                        "message": ai_response, 
                        "time": get_current_time()
                    })
                    
                except Exception as e:
                    # Handle errors gracefully
                    active_convo["messages"].append({
                        "sender": "bot", 
                        "message": "I apologize, but I'm having trouble responding right now. Please try again in a moment.", 
                        "time": get_current_time()
                    })
            
            # Rerun to refresh the interface
            st.rerun()