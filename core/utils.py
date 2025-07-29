from datetime import datetime, timedelta, timezone
import streamlit as st
import re
import json
import os
import requests

def get_current_time():
    """Returns the user's local time formatted as HH:MM AM/PM."""
    tz_offset = st.context.timezone_offset

    if tz_offset is None:
        # Default to UTC if timezone is not available (e.g., on Streamlit Cloud)
        now = datetime.now()
    else:
        now_utc = datetime.now(timezone.utc)
        now = now_utc + timedelta(minutes=-tz_offset)

    return now.strftime("%I:%M %p").lstrip("0")
   

def clean_ai_response(response_text):
    if not response_text:
        return response_text
    response_text = re.sub(r'<[^>]+>', '', response_text)
    response_text = re.sub(r'\s+', ' ', response_text).strip()
    response_text = response_text.replace('&nbsp;', ' ')
    response_text = response_text.replace('&lt;', '<')
    response_text = response_text.replace('&gt;', '>')
    response_text = response_text.replace('&amp;', '&')
    
    return response_text

def get_ai_response(user_message, model):
    if model is None:
        return "I'm sorry, I can't connect right now. Please check the API configuration."

    mental_health_prompt = f"""
    You are a compassionate mental health support chatbot named TalkHeal. Your role is to:
    1. Provide empathetic, supportive responses
    2. Encourage professional help when needed
    3. Never diagnose or provide medical advice
    4. Be warm, understanding, and non-judgmental
    5. Ask follow-up questions to better understand the user's situation
    6. Provide coping strategies and resources when appropriate
    7. Not assume that the user is always in overwhelming states. Sometimes he/she might also be in joyful or curious moods and ask questions not related to mental health
    
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

#Implementing IP Based Isolation
def get_user_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "unknown_ip"

#Saving and loading to/from JSON File
def get_memory_file():
    ip = get_user_ip()
    os.makedirs("data", exist_ok=True)
    return f"data/conversations_{ip}.json"



