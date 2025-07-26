import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from core.utils import get_current_time, get_ai_response
from core.db import get_messages, add_message

# Inject JS to get user's local time zone
def set_user_time_in_session():
    if "user_time_offset" not in st.session_state:
        components.html("""
            <script>
            const offset = new Date().getTimezoneOffset(); 
            const time = new Date().toLocaleString();      
            const data = {offset: offset, time: time};
            window.parent.postMessage({type: 'USER_TIME', data: data}, '*');
            </script>
        """, height=0)

        st.markdown("""
        <script>
        window.addEventListener("message", (event) => {
            if (event.data.type === "USER_TIME") {
                const payload = JSON.stringify(event.data.data);
                fetch("/", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: payload
                }).then(() => location.reload());
            }
        });
        </script>
        """, unsafe_allow_html=True)

set_user_time_in_session()

# Display chat messages
def render_chat_interface(model, system_prompt):
    chat_id = st.session_state.get("active_chat_id")
    if not chat_id:
        st.info("Start a new chat to begin.")
        return

    messages = get_messages(chat_id)
    for msg in messages:
        st.write(f"{msg['sender']}: {msg['message']}")

    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Your message")
        send_pressed = st.form_submit_button("Send")
    if send_pressed and user_input.strip():
        add_message(chat_id, "user", user_input.strip())
        ai_response = get_ai_response(user_input, model)
        add_message(chat_id, "bot", ai_response)
        st.rerun()
