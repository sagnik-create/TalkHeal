def handle_chat_input(model, system_prompt):   
    if "pre_filled_chat_input" not in st.session_state:
        st.session_state.pre_filled_chat_input = ""
    initial_chat_value = st.session_state.pre_filled_chat_input
    st.session_state.pre_filled_chat_input = "" 

    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input(
                "Share your thoughts...", 
                key="message_input", 
                label_visibility="collapsed",
                placeholder="Type your message here...",
                value=initial_chat_value
            )
        
        with col2:
            send_pressed = st.form_submit_button("Send", use_container_width=True)
    
    if (send_pressed or st.session_state.get('send_chat_message', False)) and user_input.strip():
        if 'send_chat_message' in st.session_state:
            st.session_state.send_chat_message = False

        if st.session_state.active_conversation >= 0:
            current_time = get_current_time()
            active_convo = st.session_state.conversations[st.session_state.active_conversation]
            active_convo["messages"].append({
                "sender": "user", 
                "message": user_input.strip(), 
                "time": current_time
            })
            save_conversations(st.session_state.conversations)
            if len(active_convo["messages"]) == 1:
                title = user_input[:30] + "..." if len(user_input) > 30 else user_input
                active_convo["title"] = title
            with st.spinner("TalkHeal is thinking..."):
                try:
                    def format_memory_for_prompt(convo_history, max_turns=10):
                        context = ""
                        for msg in convo_history[-max_turns*2:]:
                            sender = "User" if msg["sender"] == "user" else "Bot"
                            context += f"{sender}: {msg['message']}\n"
                        return context

                    context = format_memory_for_prompt(active_convo["messages"])
                    
                    response = model.generate_content([
                        {"role": "system", "parts": [system_prompt]},
                        {"role": "user", "parts": [user_input.strip()]}
                    ])

                    ai_response = response.text
                    
                    active_convo["messages"].append({
                        "sender": "bot", 
                        "message": ai_response, 
                        "time": get_current_time()
                    })
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    active_convo["messages"].append({
                        "sender": "bot", 
                        "message": "I apologise, but I'm having trouble responding right now. Please try again in a moment.", 
                        "time": get_current_time()
                    })
                    save_conversations(st.session_state.conversations)
            st.rerun()
