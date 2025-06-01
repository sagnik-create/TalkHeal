from datetime import datetime
import streamlit as st
import re

def get_current_time():
    """Returns the current time formatted as HH:MM AM/PM."""
    now = datetime.now()
    # Format: 2:30 PM (without leading zero for hours)
    return now.strftime("%-I:%M %p") if hasattr(now, 'strftime') else now.strftime("%I:%M %p").lstrip('0')

def create_new_conversation(initial_message=None):
    """
    Creates a new conversation in the session state.
    Optionally adds an initial message to the conversation.
    Returns the index of the newly created conversation.
    """
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

def clean_ai_response(response_text):
    """
    Cleans the AI response by removing any HTML tags and unwanted formatting.
    """
    if not response_text:
        return response_text
    
    # Remove HTML tags
    response_text = re.sub(r'<[^>]+>', '', response_text)
    
    # Remove extra whitespace and newlines
    response_text = re.sub(r'\s+', ' ', response_text).strip()
    
    # Remove any remaining HTML entities
    response_text = response_text.replace('&nbsp;', ' ')
    response_text = response_text.replace('&lt;', '<')
    response_text = response_text.replace('&gt;', '>')
    response_text = response_text.replace('&amp;', '&')
    
    return response_text

def get_ai_response(user_message, model):
    """
    Generates an AI response using the configured Gemini model,
    with a prompt tailored for mental health support.
    """
    if model is None:
        return "I'm sorry, I can't connect right now. Please check the API configuration."

    mental_health_prompt = f"""
    You are a compassionate mental health support chatbot named PeacePulse. Your role is to:
    1. Provide empathetic, supportive responses
    2. Encourage professional help when needed
    3. Never diagnose or provide medical advice
    4. Be warm, understanding, and non-judgmental
    5. Ask follow-up questions to better understand the user's situation
    6. Provide coping strategies and resources when appropriate
    
    IMPORTANT: Respond with PLAIN TEXT ONLY. Do not include any HTML tags, markdown formatting, or special characters. Just provide a natural, conversational response.
    
    User message: {user_message}
    
    Respond in a caring, supportive manner (keep response under 150 words):
    """
    
    try:
        response = model.generate_content(mental_health_prompt)
        # Clean the response to remove any HTML or unwanted formatting
        cleaned_response = clean_ai_response(response.text)
        return cleaned_response
    except Exception as e:
        return "I'm here to listen and support you. Sometimes I have trouble connecting, but I want you to know that your feelings are valid and you're not alone. Would you like to share more about what you're experiencing?"