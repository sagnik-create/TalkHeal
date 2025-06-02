import streamlit as st
from core.utils import get_current_time, get_ai_response

def render_chat_interface():
    """Renders the main chat message display area directly without any wrapper container."""
    
    if st.session_state.active_conversation >= 0:
        active_convo = st.session_state.conversations[st.session_state.active_conversation]
        
        # Show welcome message if no messages exist
        if not active_convo["messages"]:
            st.markdown(f"""
            <div class="welcome-message">
                <strong>Hello! I'm TalkHeal, your mental health companion.</strong><br>
                I'm here to listen, support, and help guide you toward the resources you need. How are you feeling today? 😊
                <div class="message-time">{get_current_time()}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Render all messages directly without any wrapper container
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

def handle_chat_input(model):
    """Handles the user input for the chat and generates AI responses."""
    
    # Initialize pre-filled input if not present
    if "pre_filled_chat_input" not in st.session_state:
        st.session_state.pre_filled_chat_input = ""
    
    # Use the pre-filled value if available, then clear it
    initial_chat_value = st.session_state.pre_filled_chat_input
    st.session_state.pre_filled_chat_input = "" # Clear it immediately after reading

    # Create a form for chat input
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input(
                "Share your thoughts...", 
                key="message_input", 
                label_visibility="collapsed",
                placeholder="Type your message here...",
                value=initial_chat_value # Set the initial value here
            )
        
        with col2:
            send_pressed = st.form_submit_button("Send", use_container_width=True)
    
    # Process the input when send is pressed or if triggered by a sidebar button
    if (send_pressed or st.session_state.get('send_chat_message', False)) and user_input.strip():
        # Reset the flag after processing
        if 'send_chat_message' in st.session_state:
            st.session_state.send_chat_message = False

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
            with st.spinner("TalkHeal is thinking..."):
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
                    st.error(f"An error occurred: {e}") # For debugging
                    active_convo["messages"].append({
                        "sender": "bot", 
                        "message": "I apologize, but I'm having trouble responding right now. Please try again in a moment.", 
                        "time": get_current_time()
                    })
            
            # Rerun to refresh the interface
            st.rerun()