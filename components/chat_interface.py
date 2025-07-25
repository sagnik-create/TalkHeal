import streamlit as st
from core.db import get_messages, add_message
from core.utils import get_current_time, get_ai_response

def render_chat_interface(model):
    chat_id = st.session_state.get("active_chat_id")
    if not chat_id:
        st.info("Start a new chat to begin.")
        return

    messages = get_messages(chat_id)
    if not messages:
        st.markdown("""
        <div class="welcome-message">
            <strong>Hello! I'm TalkHeal, your mental health companion</strong><br>
            How are you feeling today? You can write it down below or for a fresh start click on "➕ New Chat" 😊
        </div>
        """, unsafe_allow_html=True)

    for msg in messages:
        if msg["sender"] == "user":
            st.markdown(f"""
            <div class="user-message">
                {msg["message"]}
                <div class="message-time">{msg["timestamp"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="bot-message">
                {msg["message"]}
                <div class="message-time">{msg["timestamp"]}</div>
            </div>
            """, unsafe_allow_html=True)

    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Share your thoughts...", key="message_input", label_visibility="collapsed")
        send_pressed = st.form_submit_button("Send")
    if send_pressed and user_input.strip():
        add_message(chat_id, "user", user_input.strip())
        with st.spinner("TalkHeal is thinking..."):
            context = "\n".join([f"{m['sender'].capitalize()}: {m['message']}" for m in get_messages(chat_id)])
            prompt = context + f"\nUser: {user_input.strip()}\nBot:"
            ai_response = get_ai_response(prompt, model)
            add_message(chat_id, "bot", ai_response)
        st.rerun()