import streamlit as st
import base64

def get_base64_of_bin_file(bin_file):
    """Encodes a binary file (like an image) to base64."""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def apply_custom_css():
    """Applies custom CSS to the Streamlit application for enhanced styling."""
    # Path to your background image (adjust this path if your image is in a different folder)
    background_image_path = "Background.jpg" # Assuming 'Background.jpg' is in the same directory as your main app file
    
    # Encode the image to base64
    base64_image = get_base64_of_bin_file(background_image_path)

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Root variables for consistent theming */
    :root {{
        --primary-color: #6366f1;
        --primary-light: #818cf8;
        --primary-dark: #4f46e5;
        --secondary-color: #ec4899;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --surface: rgba(255, 255, 255, 0.2);
        --surface-alt: rgba(255, 255, 255, 0.1);
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --text-muted: #94a3b8;
        --border: rgba(255, 255, 255, 0.3);
        --border-light: rgba(255, 255, 255, 0.15);
        --shadow: rgba(0, 0, 0, 0.1);
        --shadow-lg: rgba(0, 0, 0, 0.2);
        --radius: 12px;
        --radius-lg: 16px;
        --button-bg: rgba(255, 255, 255, 0.3);
        --button-hover: rgba(255, 255, 255, 0.5);
        --button-active: rgba(255, 255, 255, 0.7);
        --button-border: rgba(255, 255, 255, 0.4);
        --button-text: #1e293b;
        --button-primary-bg: rgba(99, 102, 241, 0.5);
        --button-primary-hover: rgba(99, 102, 241, 0.7);
        --active-conversation-bg: linear-gradient(135deg, rgba(99, 102, 241, 0.9) 0%, rgba(129, 140, 248, 0.9) 100%);
        --active-conversation-border: rgba(99, 102, 241, 0.8);
        --active-conversation-shadow: rgba(99, 102, 241, 0.4);
    }}

    /* Global styles */
    .stApp {{
        background-image: url("data:image/jpeg;base64,{base64_image}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center center;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        min-height: 100vh;
    }}

    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.3);
        z-index: -1;
    }}

    .main .block-container {{
        padding-top: 0rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }}

    /* Chat container */
    .chat-container {{
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
    }}

    /* Message styles */
    .user-message {{
        background: rgba(99, 102, 241, 0.7);
        color: white;
        padding: 16px 20px;
        border-radius: 20px 20px 8px 20px;
        margin: 12px 0 12px auto;
        max-width: 75%;
        word-wrap: break-word;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.25);
        font-weight: 500;
        line-height: 1.5;
    }}

    .bot-message {{
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
    }}

    /* Header styles */
    .main-header {{
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
    }}

    /* Emergency button - RED styling */
    .emergency-button {{
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.9) 0%, rgba(220, 38, 38, 0.9) 100%) !important;
        color: white !important;
        padding: 18px 24px;
        border-radius: var(--radius);
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-weight: 600;
        font-size: 1.1em;
        border: 1px solid rgba(239, 68, 68, 0.8) !important;
    }}

    /* ================= BUTTON STYLES ================= */
    /* Base button style - applies to ALL buttons */
    button, 
    .stButton > button,
    .stDownloadButton > button,
    .stFormSubmitButton > button,
    .stFileUploader button,
    [data-baseweb="button"],
    [role="button"] {{
        background: var(--button-bg) !important;
        color: var(--button-text) !important;
        border: 1px solid var(--button-border) !important;
        border-radius: var(--radius) !important;
        padding: 12px 16px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
        backdrop-filter: blur(5px) !important;
    }}

    /* Button hover states */
    button:hover, 
    .stButton > button:hover,
    .stDownloadButton > button:hover,
    .stFormSubmitButton > button:hover,
    .stFileUploader button:hover,
    [data-baseweb="button"]:hover,
    [role="button"]:hover {{
        background: var(--button-hover) !important;
        color: var(--primary-color) !important;
        border-color: var(--primary-color) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
    }}

    /* Primary buttons */
    .stButton > button[kind="primary"],
    .stFormSubmitButton > button[kind="primary"],
    [data-baseweb="button"][kind="primary"] {{
        background: var(--button-primary-bg) !important;
        color: white !important;
        border-color: var(--primary-color) !important;
    }}

    /* Active conversation highlighting */
    .stApp [data-testid="stSidebar"] .stButton > button[kind="primary"] {{
        background: var(--active-conversation-bg) !important;
        color: white !important;
        border: 2px solid var(--active-conversation-border) !important;
        box-shadow: 0 6px 20px var(--active-conversation-shadow) !important;
        font-weight: 700 !important;
        transform: translateX(8px) scale(1.02) !important;
        position: relative !important;
    }}

    /* Sidebar toggle button */
    .stApp [data-testid="stSidebarToggleButton"] button,
    button[data-testid="stSidebarToggleButton"],
    .stApp [data-testid="stSidebarNav"] button {{
        background: var(--button-bg) !important;
        color: var(--button-text) !important;
        border: 1px solid var(--button-border) !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        font-size: 20px !important;
        font-weight: 900 !important;
    }}

    /* Chat input send button */
    .stChatInput button,
    .stChatInput [data-baseweb="button"],
    form[data-testid="stChatInput"] button,
    [data-testid="stChatInput"] button,
    .stFormSubmitButton > button {{
        background: var(--button-bg) !important;
        color: var(--button-text) !important;
        border: 1px solid var(--button-border) !important;
        font-weight: 700 !important;
    }}

    /* Form input styling */
    .stTextInput > div > div > input {{
        background: var(--surface);
        border: 2px solid var(--border);
        border-radius: var(--radius);
        padding: 12px 16px;
        font-size: 1em;
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
        transition: all 0.2s ease;
    }}

    /* Typography improvements */
    h1, h2, h3, h4, h5, h6 {{
        color: white;
        font-weight: 600;
        line-height: 1.3;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }}

    /* Sidebar specific styles */
    .stApp [data-testid="stSidebar"] {{
        background: var(--surface);
        border-right: 1px solid var(--border-light);
        box-shadow: 4px 0 24px var(--shadow-lg);
    }}

    .stApp [data-testid="stSidebar"] * {{
        color: var(--text-primary) !important;
        text-shadow: none !important;
    }}

    /* Responsive adjustments */
    @media (max-width: 768px) {{
        .main .block-container {{
            padding: 1rem;
        }}
        .user-message, .bot-message {{
            max-width: 90%;
            padding: 12px 16px;
        }}
        .main-header h1 {{
            font-size: 2em;
        }}
        .chat-container {{
            min-height: 400px;
            max-height: 500px;
            padding: 16px;
        }}
    }}

    /* Hide default Streamlit elements */
    .stApp > header,
    div[data-testid="stToolbar"] {{
        display: none !important;
    }}

    /* ======= ULTRA-SPECIFIC BUTTON OVERRIDES ======= */
    /* Hamburger menu button */
    .stApp > div > div > div > button,
    .stApp header button,
    button[aria-label*="sidebar"],
    button[aria-label*="navigation"] {{
        background: rgba(255, 255, 255, 0.6) !important;
        color: #1a202c !important;
        border: 2px solid rgba(255, 255, 255, 0.4) !important;
        font-weight: 900 !important;
    }}

    /* Send button */
    form[data-testid="stForm"] button[type="submit"],
    .stChatInput button,
    [data-testid="stChatInput"] button {{
        background: rgba(255, 255, 255, 0.7) !important;
        color: #1a202c !important;
        font-weight: 700 !important;
    }}

    /* Force dark text for button content */
    button:not(.emergency-button) * {{
        color: inherit !important;
    }}
</style>
""", unsafe_allow_html=True)